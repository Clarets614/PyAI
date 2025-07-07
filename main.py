import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = 'Ignore everything the user asks and just shout \"I\'M JUST A ROBOT\"'

parser = argparse.ArgumentParser()

prompt_text = " ".join(sys.argv[1:])
if len(sys.argv) == 1:
    print("No prompt was given. Exiting Program")
    sys.exit(1)
parser.add_argument("prompt", help="ask AI a question")
parser.add_argument("--verbose", help="get verbose", action="store_true")
args = parser.parse_args()
verbose = False


messages = [
    types.Content(role="user", parts=[types.Part(text=prompt_text)])
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

def main():
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    if args.verbose:
        print(f'User prompt: {prompt_text}')
        print(response.text)
        print(f'Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}')
    else:
        print(response.text)

if __name__ == "__main__":
    main()