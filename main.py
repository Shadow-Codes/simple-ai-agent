import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    # checks for prompt before making API call
    if len(sys.argv) < 2:
        print("You need to enter a prompt")
        sys.exit(1)

    if len(sys.argv) == 3:
        generate_content(client, sys.argv[1], sys.argv[2])
    else:
        generate_content(client, sys.argv[1])


def generate_content(client, prompt, flag=""):
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if response.function_calls:
            for call in response.function_calls:
                func_name = call.name
                func_args = call.args if call.args else {"directory": "."}
                print(f"Calling function: {func_name}({func_args})")
        else:
            if flag == "--verbose":
                print(f"User prompt: {prompt}")
                print(response.text)
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )
            else:
                print(response.text)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
