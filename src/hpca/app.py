import os
import anthropic
import gradio as gr
from dotenv import load_dotenv
import asyncio
from hpca.config import AgentConfig


# Load the Anthropic API key from the environment variable
load_dotenv()
client = anthropic.Anthropic()
config = AgentConfig(directory_path=os.environ.get("AGENT_CONFIG_DIR", "agent-config"))


def format_messages(messages):
    formatted_messages = []
    for message in messages:
        if message["role"] == "user":
            formatted_messages.append({"role": "user", "content": message["content"]})
        elif message["role"] == "assistant":
            formatted_messages.append({"role": "assistant", "content": message["content"]})
    return formatted_messages


def predict(history):
    with client.messages.stream(
        model=config.model,
        max_tokens=config.max_tokens,
        temperature=0,
        system=config.system_prompt,
        messages=format_messages(history)
    ) as stream:
        for event in stream:
            if event.type == "text":
                messages = history.copy()
                msg = {
                    "role": "assistant",
                    "content": event.snapshot
                }
                messages.append(msg)
                yield messages
    yield messages


def append_example_message(x: gr.SelectData, history):
    if x.value["text"] is not None:
        history.append({"role": "user", "content": x.value["text"]})
    return history


with gr.Blocks() as demo:
    gr.Markdown(config.app_title)
    gr.Markdown(config.app_instructions)

    chatbot = gr.Chatbot(
        examples=config.examples,
        type='messages',
    )
    msg = gr.Textbox(placeholder="Type your question here...", scale=4)
    submit = gr.Button("Submit", variant="primary")

    def user(user_message, history):
        return "", history + [{"role": "user", "content": user_message}]

    def bot(history):
        for item in predict(history):
            yield item

    chatbot.example_select

    msg.submit(user, [msg, chatbot], [msg, chatbot]).then(
        bot, [chatbot], [chatbot]
    )
    submit.click(user, [msg, chatbot], [msg, chatbot]).then(
        bot, [chatbot], [chatbot]
    )
    chatbot.example_select(append_example_message, [chatbot], [chatbot]).then(
        bot, [chatbot], [chatbot], api_name="respond")


def main():
    demo.launch()


if __name__ == "__main__":
    main()
