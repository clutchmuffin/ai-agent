import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:

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
            return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

        if not os.path.isfile(target_file_path):
            return f"Error: File not found or is not a regular file: '{file_path}'"

        return read_file(target_file_path)

    except Exception as e:
        return f"Error: '{e}'"


def read_file(file_path: str) -> str:

    try:
        with open(file_path, "r") as f:
            file_content: str = f.read(MAX_CHARS)
            if f.read(1):
                file_content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content

    except Exception as e:
        return f"Error: '{e}'"
