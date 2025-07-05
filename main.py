import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


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
    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        )

        if flag == "--verbose":
            print(f"User prompt: {prompt}")
            print(response.text)
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            print(response.text)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
