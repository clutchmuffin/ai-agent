import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from functions.call_function import available_functions
from prompts import system_prompt

DEFAULT_MODEL = "openrouter/free"


def load_api_key() -> str:
    _ = load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the environment")
    return api_key


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    _ = parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    return parser.parse_args()


def create_client() -> OpenAI:
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=load_api_key(),
    )


def chat(
    client: OpenAI, user_prompt: str, model: str = DEFAULT_MODEL
) -> ChatCompletion:
    response: ChatCompletion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        tools=available_functions,
    )
    if response.usage is None:
        raise RuntimeError("Failed API request")
    return response


def print_verbose(args: argparse.Namespace, response: ChatCompletion) -> None:
    print(f"User prompt: {args.user_prompt}")
    if response.usage is not None:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")


def main() -> None:
    args = parse_args()
    client = create_client()
    response = chat(client, args.user_prompt)

    if args.verbose:
        print_verbose(args, response)

    message: ChatCompletionMessage = response.choices[0].message
    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
