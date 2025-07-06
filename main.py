import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function

MAX_RUNS = 20


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

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    run_no = 1

    while run_no <= MAX_RUNS:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            verbose = flag == "--verbose"

            if response.function_calls:
                for call in response.function_calls:
                    result = call_function(call, verbose)

                    if not result.parts[0].function_response.response:
                        raise Exception("Function call failed")
                    else:
                        messages.append(result)
                        if verbose:
                            print(f"-> {result.parts[0].function_response.response}")
            else:
                print(response.text)
                # break out of loop agent is done
                break

            run_no += 1
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
