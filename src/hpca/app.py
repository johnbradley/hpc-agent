import anthropic
import gradio as gr
from dotenv import load_dotenv
import asyncio

APP_TITLE = "RCC Helper 🧐"
APP_INSTRUCTIONS = "Ask me anything about the Research Computing Center (RCC)."
MODEL = "claude-3-5-sonnet-20241022"
MAX_TOKENS = 1000
SYSTEM_PROMPT = """
You are a helpful assistant that answers questions about the Research Computing Center (RCC).
RCC is a Slurm based Linux system with OpenOnDemand and globus.
Provide clear, concise, and accurate information about HPC resources, computing services, and documentation.
If you don't know something, say so rather than making up information.
Prefer slurm commands over other commands.
Here are some important RCC resources to refer to when answering questions:


- https://slurm.schedmd.com/sbatch.html - Help on the sbatch command
- https://slurm.schedmd.com/srun.html - Help on the srun command

When answering questions, refer to these resources for accurate and up-to-date information.

"""
EXAMPLES = [
    {"text":"how to run background job"},
    {"text":"how to build a container"},
    {"text":"how to create a conda environment with pytorch"},
]


# Load the Anthropic API key from the environment variable
load_dotenv()
client = anthropic.Anthropic()


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
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=0,
        system=SYSTEM_PROMPT,
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
    gr.Markdown(APP_TITLE)
    gr.Markdown(APP_INSTRUCTIONS)

    chatbot = gr.Chatbot(
        examples=EXAMPLES,
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
