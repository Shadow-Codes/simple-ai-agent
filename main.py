import os
import sys

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# creates gemini developer API client
client = genai.Client(api_key=api_key)

# checks for prompt before making API call
if len(sys.argv) < 2:
    print("You need to enter a prompt")
    sys.exit(1)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=sys.argv[1],
)

metadata = response.usage_metadata

print(response.text)
print(f"Prompt tokens: {metadata.prompt_token_count}")
print(f"Response tokens: {metadata.candidates_token_count}")
