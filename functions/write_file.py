import os

from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_dir_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # check if file path is outside working directory
    if not abs_file_path.startswith(abs_working_dir_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes given content to the file at given file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, description="File location to write content."
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="Actual content to write."
            ),
        },
    ),
)
