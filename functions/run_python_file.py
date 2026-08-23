import os
import subprocess as sp


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        absolute_working_directory: str = os.path.abspath(working_directory)
        target_file_path: str = os.path.normpath(
            os.path.join(absolute_working_directory, file_path)
        )

        # Check if target file is in the working_directory
        valid_target_file: bool = (
            os.path.commonpath([absolute_working_directory, target_file_path])
            == absolute_working_directory
        )

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        return run_file(target_file_path, args)

    except Exception as e:
        return f"Error: '{e}'"


def run_file(file_path: str, args: list[str] | None = None) -> str:
    command: list[str] = ["python", file_path]
    output: str = ""

    if args is not None:
        command.extend(args)

    try:
        result: sp.CompletedProcess[str] = sp.run(
            command, capture_output=True, text=True, timeout=30, check=True
        )

        output += f"Process exited with code {result.returncode}\n"

        if result.stderr == "" and result.stdout == "":
            output += "No output produced"

        output += f"STDOUT: {result.stdout}\n"
        output += f"STDERR: {result.stderr}\n"

        return output

    except sp.TimeoutExpired:
        return "Error: The command took too long and timed out."

    except sp.CalledProcessError as e:
        return f"Error: '{e}'"

    except Exception as e:
        return f"Error: executing Python file: {e}"
