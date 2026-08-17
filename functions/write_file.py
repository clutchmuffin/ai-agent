import os


def write_file(working_directory: str, file_path: str, content: str) -> str:

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
            return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"

        if os.path.isdir(target_file_path):
            return f"Error: Cannot write to '{file_path}' as it is a directory"

        parent_directory: str = os.path.dirname(target_file_path)
        os.makedirs(parent_directory, exist_ok=True)
        with open(target_file_path, "w") as f:
            _ = f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: '{e}'"
