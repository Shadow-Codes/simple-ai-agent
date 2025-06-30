import os


def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    combined_path = os.path.join(working_directory, directory) 

    if not os.path.abspath(combined_path).startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(combined_path):
        return f'Error: "{directory}" is not a directory'

    contents = os.listdir(combined_path)
    return_str = []

    try:
        for item in contents:
            item_path = os.path.join(combined_path, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            return_str.append(f"- {item}: file_size={size}, is_dir={is_dir}")

        return "\n".join(return_str)
    except Exception as e:
        return f"Error: {e}"
