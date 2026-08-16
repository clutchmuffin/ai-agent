import os, argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

messages = [
    {
        "role": "user",
        "content": args.user_prompt,
    }
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages
)

if response.usage is None:
    raise RuntimeError("Failed API request")

tokens_sent = response.usage.prompt_tokens
tokens_received = response.usage.completion_tokens

print(f"Prompt tokens: {tokens_sent}")
print(f"Response tokens: {tokens_received}")
print(response.choices[0].message.content)
