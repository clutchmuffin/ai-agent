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
            # return f"Success: '{directory} is within the working directory'"
            return file_information_builder(target_directory)
    
    except Exception as e:
        return f"Error: '{e}'"

def file_information_builder(directory: str) -> str:
    contents = ""

    try:
        files_in_directory = os.listdir(directory)
        for file in files_in_directory:
            file_name = file
            file_path = directory + "/" + file
            file_size = os.path.getsize(file_path)
            is_file_dir = os.path.isdir(file_path)

            contents += f"- {file_name}: file_size={file_size}, is_dir={is_file_dir}\n"

        return contents

    except Exception as e:
        return f"Error: '{e}'"
