import json
import gradio as gr
from swarm import Swarm
from autonomous_agent import microservices_agent

def run_demo_with_gradio(starting_agent, context_variables=None, debug=False):
    client = Swarm()
    messages = []
    agent = starting_agent

    def respond(message, history):
        nonlocal agent, messages
        messages.append({"role": "user", "content": message})
        
        response_chunks = []
        log_content = []
        
        # 首先yield用户的消息
        yield [[message, None]], gr.update()
        
        for chunk in client.run(
            agent=agent,
            messages=messages,
            context_variables=context_variables or {},
            stream=True,
            debug=debug,
        ):
            if "content" in chunk and chunk["content"] is not None:
                response_chunks.append(chunk["content"])
                yield [[message, "".join(response_chunks)]], gr.update()
            
            if "tool_calls" in chunk and chunk["tool_calls"] is not None:
                for tool_call in chunk["tool_calls"]:
                    f = tool_call["function"]
                    name, args = f["name"], f["arguments"]
                    log_content.append(f"工具调用: {name}({args})")
            
            if debug and "debug" in chunk:
                log_content.append(f"调试信息: {chunk['debug']}")
            
            if log_content:
                yield [[message, "".join(response_chunks)]], gr.update(value="\n".join(log_content))

        messages.extend([{"role": "assistant", "content": "".join(response_chunks)}])
        agent = chunk.get("agent", agent)

    with gr.Blocks() as demo:
        gr.Markdown("# Swarm Agent Demo")
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot()
                msg = gr.Textbox()
                clear = gr.Button("清除对话")
            with gr.Column(scale=1):
                log_output = gr.Textbox(label="工具调用 & 调试信息", lines=20)

        msg.submit(respond, [msg, chatbot], [chatbot, log_output])
        clear.click(lambda: None, None, chatbot, queue=False)

    demo.queue()
    demo.launch()

# 使用示例
if __name__ == "__main__":
    run_demo_with_gradio(microservices_agent, debug=False)
