import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from config import DEFAULT_MODEL, MAX_ITERATIONS
from functions.call_function import available_functions, call_function
from prompts import system_prompt


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


def call_llm(
    client: OpenAI, messages: list[dict], model: str = DEFAULT_MODEL
) -> ChatCompletion:
    response: ChatCompletion = client.chat.completions.create(
        model=model,
        messages=messages,
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

    # Build the conversation history
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # Main agent loop
    for i in range(MAX_ITERATIONS):
        response = call_llm(client, messages)

        if args.verbose and i == 0:
            print_verbose(args, response)

        message: ChatCompletionMessage = response.choices[0].message
        messages.append(message)

        # If no tool calls, we got the final response
        if message.tool_calls is None:
            print(message.content)
            return

        # Execute each tool call and collect tool messages
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)

            content = result_message.get("content", "")
            if not content:
                raise RuntimeError(
                    f"Tool call {tool_call.id} for function {tool_call.function.name} "
                    "returned an empty content field."
                )

            if args.verbose:
                print(f"-> {content}")

            # Append tool result to list of messages so far
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": content,
                }
            )

    print(
        f"Error: reached maximum number of iterations ({MAX_ITERATIONS}) "
        "without a final response from the model."
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
