import sys
import io
import re
import json
import gradio as gr
from swarm import Swarm
from autonomous_agent import microservices_agent
from cooperate_agents import assistant_agent

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
        gr.Markdown("# 微服务组合仿真Agent")
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(type="messages")
                msg = gr.Textbox(submit_btn=True)
                clear = gr.Button("清除对话")
            with gr.Column(scale=1):
                log_output = gr.Textbox(label="工具调用 & 调试信息", lines=20)

        msg.submit(respond, [msg, chatbot, log_output], [msg, chatbot, log_output])
        clear.click(reset_agent, None, [msg, chatbot, log_output], queue=False)

    demo.queue()
    demo.launch()

# 使用示例
if __name__ == "__main__":
    # run_demo_with_gradio(microservices_agent, debug=True)
    run_demo_with_gradio(assistant_agent, debug=True)
