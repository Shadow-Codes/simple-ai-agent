import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path):
    abs_working_dir_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir_path, file_path))

    if not abs_file_path.startswith(abs_working_dir_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found'

    file_name, extension = os.path.splitext(file_path)

    if extension.lower() != ".py":
        return f'Error: "{file_path}" is not a python file.'

    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            cwd=abs_working_dir_path,
            text=True,
            timeout=30,
        )
        output = []

        if not result.stdout and not result.stderr:
            return "No output produced."
        if result.stdout:
            output.append(f"STDOUT: {result.stdout.strip()}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr.strip()}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Checks for python file at given file path, and runs it. Returns output and errors produced.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to check and run python file.",
            ),
        },
    ),
)
