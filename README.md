# ai-agent

A minimal AI coding agent that uses an LLM (via OpenRouter) to autonomously plan and execute file operations in a sandboxed working directory.

## How it works

You pass a prompt to the CLI, and the agent runs a loop:

1. Send the conversation to the model with the available function schemas.
2. If the model requests tool calls, execute them and feed the results back.
3. Repeat until the model produces a final answer (or the iteration limit is reached).

All file operations are confined to a fixed working directory (`./calculator`), which is injected into every tool call for security.

## Available tools

| Tool | Description |
| --- | --- |
| `get_files_info` | Lists files in a directory with size and directory status |
| `get_file_content` | Reads a file (truncated at 10,000 characters) |
| `write_file` | Writes content to a file |
| `run_python_file` | Runs a `.py` file as a subprocess (30s timeout) |

## Setup

Create a `.env` file in the project root with your OpenRouter API key:

```sh
echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env
uv sync
```

## Usage

```sh
uv run python main.py "Explain the code in calculator/main.py"
```

Options:

- `-v, --verbose` — print the user prompt, token usage, and each tool call in detail

## Configuration

| Setting | Default | Description |
| --- | --- | --- |
| `OPENROUTER_API_KEY` | — | API key for OpenRouter (required) |
| `DEFAULT_MODEL` | `openrouter/free` | Model to use for the agent |
| `MAX_ITERATIONS` | `20` | Max agent loop iterations before giving up |
| `MAX_CHARS` | `10000` | Max characters read per file |