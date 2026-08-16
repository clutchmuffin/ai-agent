import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        if not os.path.isdir(directory):
            return f"Error: '{directory}' is not a directory"

        absolute_working_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(absolute_working_directory, directory))

        # Check if target directory is in the working_directory
        valid_target_directory = os.path.commonpath([
            absolute_working_directory, target_directory
        ]) == absolute_working_directory

        if not valid_target_directory:
            return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
        else:
            return f"Success: '{directory} is within the working directory'"
    
    except Exception as e:
        return f"Error: '{e}'"
