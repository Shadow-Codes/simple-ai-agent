from google.genai import types

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    working_dir = "./calculator"

    functions = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    try:
        function_called = function_call_part.name
        func_args = {"working_directory": working_dir, **function_call_part.args}

        if function_called not in functions:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_called,
                        response={"error": f"Unknown function: {function_called}"},
                    )
                ],
            )

        function_result = functions[function_called](**func_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_called, response={"result": function_result}
                )
            ],
        )
    except Exception as e:
        print(e)
