import sys
import io
import re
import json
import gradio as gr
from swarm import Swarm
from UAV_agents import assistant_agent

import folium
# ... existing imports ...

DEMO_INPUT = """目前有哪些已注册的微服务？

我希望利用已注册的微服务进行组合，以构建一个无人机app。该app主要包含两个功能：1.用户首先通过无人机控制服务和路径规划服务得到无人机飞行路线，再利用控制无人机仿真环境中按照规划后的路径进行飞行 2.仿真环境中无人机的实时视频画面会存储在数据库中，并被用于目标识别以检测火灾，检测的结果会被存储在数据库中，如果识别到火灾则发出警告.

我们假定用户在调用无人机控制服务时输入的起始坐标为(31.3385, 121.5020)，终点坐标为(31.3389, 121.5025)，设定的途经点为(31.3384, 121.5019), (31.3387, 121.5018)和 (31.3384, 121.5023)

请你根据以上的微服务组合逻辑，使用mardown的mermaid语法画出框架图，框架图中的节点应该是微服务的名称。
"""

RESULT_MERMAID = r"""# Result
```graph TD
    A[无人机控制微服务] --> B[无人机路径规划微服务]
    B --> C[无人机飞行模拟微服务]
    C --> D[无人机飞行视频存储微服务]
    C --> E[火灾检测微服务]
    E --> F[火灾检测保存微服务]
    F --> G{如果发现火灾}
    G --> |是| H[发出警告]
    G --> |否| I[继续监控]
```
"""

DESIGN_IMG = r"https://lhcos-84055-1317429791.cos.ap-shanghai.myqcloud.com/Agent演示/uav微服务.png"

RESULT_IMG = r"https://lhcos-84055-1317429791.cos.ap-shanghai.myqcloud.com/Agent演示/uav_result.png"

def generate_map_with_path(start, end, waypoints):
    # 创建地图，中心点为起始点
    m = folium.Map(
        location=start,
        zoom_start=18,
        tiles='OpenStreetMap'
    )
    
    # 计算最短路径
    shortest_path, shortest_distance = [
        [31.3385, 121.5020], 
        [31.3387, 121.5018], 
        [31.3384, 121.5019], 
        [31.3384, 121.5023], 
        [31.3389, 121.5025]
    ], 160.67
    
    # 在地图上绘制路径
    folium.PolyLine(locations=shortest_path, color='blue').add_to(m)
    
    # 添加起始点和终止点标记
    folium.Marker(location=start, popup="起始点", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(location=end, popup="终止点", icon=folium.Icon(color='red')).add_to(m)
    
    # 添加途经点标记
    for waypoint in waypoints:
        folium.Marker(location=waypoint, popup="途经点", icon=folium.Icon(color='orange')).add_to(m)
    
    map_html = m._repr_html_()
    return map_html

def parse_points(points_str):
    """解析输入的坐标字符串为列表"""
    points = []
    for point_str in points_str.split('\n'):
        lat, lon = map(float, point_str.split(','))
        points.append((lat, lon))
    return points

def ansi_filter(string):
    string = string.replace("\033[97m", "") 
    string = string.replace("\033[90m", "")
    string = string.replace("\033[0m", "\n")

    return string

def run_demo_with_gradio(starting_agent, context_variables=None, debug=False):
    client = Swarm()
    messages = []
    agent = starting_agent

    def reset_agent():
        nonlocal agent, messages
        agent = starting_agent
        messages = []
        # 返回空列表来清除chatbot的对话历史
        return None, [], None

    def respond(message, history, log_output):
        nonlocal agent, messages

        # 创建一个StringIO对象来捕获输出
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            # history是前端聊天窗口的历史信息，messages是访问llm api的对话历史
            history.append({"role": "user", "content": message})
            messages.append({"role": "user", "content": message})
            
            response_chunks = []
            log_content = []
            
            # 首先yield用户的消息,即聊天窗口显示刚刚用户的输入，
            # 并且log_output为空，同时清除输入框的内容
            yield ["", history, log_output]

            response = client.run(
                agent=agent,
                messages=messages,
                context_variables=context_variables or {},
                stream=True,
                debug=debug,
            )

            content = ""
            last_sender = ""

            for chunk in response:
                if "sender" in chunk:
                    last_sender = chunk["sender"]

                if "content" in chunk and chunk["content"] is not None:
                    if not content and last_sender:
                        # 对话窗口中新建一条助手消息
                        history.append({"role":"assistant", "content":f"<span style='color:blue;'>{last_sender}:</span>"})
                        last_sender = ""
                    
                    # 流式更新content
                    content += chunk["content"]
                    # 流式更新对话窗口
                    history[-1]['content'] += chunk["content"]
                    # 在yield之前更新log_output
                    log_output = ansi_filter(sys.stdout.getvalue())
                    yield ["", history, log_output]
                
                if "tool_calls" in chunk and chunk["tool_calls"] is not None:
                    for tool_call in chunk["tool_calls"]:
                        f = tool_call["function"]
                        name = f["name"]
                        if not name:
                            continue

                        # 对话窗口中新建一条助手消息
                        history.append({"role":"assistant", "content":""})
                        history[-1]['content'] += f"<span style='color:blue;'>{last_sender}:</span> <span style='color:purple;'>{name}</span>()\n"
                        
                        # 在yield之前更新log_output
                        log_output = ansi_filter(sys.stdout.getvalue())
                        yield ["", history, log_output]
                
                # if debug and "debug" in chunk:
                #     log_content.append(f"调试信息: {chunk['debug']}")

                if "delim" in chunk and chunk["delim"] == "end" and content:
                    history[-1]['content'] += "\n"  # End of response message
                    content = ""

                if "response" in chunk:
                    break
                
                # if log_content:
                #     yield [[message, "".join(response_chunks)]], gr.update(value="\n".join(log_content))
            
            messages.extend(chunk["response"].messages)
            agent = chunk["response"].agent
        
        finally:
            # 恢复原始stdout
            sys.stdout = old_stdout

    with gr.Blocks() as demo:
        gr.Markdown("# 微服务组合仿真Agent——无人机demo")
        with gr.Row():
            with gr.Column(scale=1):
                # 添加地图显示功能
                gr.Interface(
                    fn=lambda start, end, waypoints: generate_map_with_path(
                        parse_points(start)[0],
                        parse_points(end)[0],
                        parse_points(waypoints)
                    ),
                    inputs=[
                        gr.Textbox(label="起点 (格式: lat,lon)", value="31.3385, 121.5020"),
                        gr.Textbox(label="终点 (格式: lat,lon)", value="31.3389, 121.5025"),
                        gr.Textbox(label="途经点 (格式: 每行一个点，lat,lon)", value="31.3384, 121.5019\n31.3387, 121.5018\n31.3384, 121.5023")
                    ],
                    outputs=gr.HTML(),
                    cache_examples=False,
                    flagging_mode="never",  # 禁用标记按钮
                    clear_btn=None   # 禁用清除按钮
                )
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(type="messages")
                msg = gr.Textbox(submit_btn=True)
                clear = gr.Button("清除对话")
            with gr.Column(scale=1):  
                log_output = gr.Textbox(label="工具调用 & 调试信息", lines=25)
        with gr.Row():
            gr.Textbox(label="示例输入", value=DEMO_INPUT)
        gr.Markdown("# 设计")
        gr.Image(DESIGN_IMG)
        gr.Markdown(RESULT_MERMAID)
        gr.Image(RESULT_IMG)

        msg.submit(respond, [msg, chatbot, log_output], [msg, chatbot, log_output])
        clear.click(reset_agent, None, [msg, chatbot, log_output], queue=False)

    demo.queue()
    demo.launch()

# 使用示例
if __name__ == "__main__":
    # run_demo_with_gradio(microservices_agent, debug=True)
    run_demo_with_gradio(assistant_agent, debug=True)
