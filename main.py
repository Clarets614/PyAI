import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_contents import schema_get_file_content
from functions.run_python import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

parser = argparse.ArgumentParser()

prompt_text = " ".join(sys.argv[1:])
if len(sys.argv) == 1:
    print("No prompt was given. Exiting Program")
    sys.exit(1)
parser.add_argument("prompt", help="ask AI a question")
parser.add_argument("--verbose", help="get verbose", action="store_true")
args = parser.parse_args()
verbose = False

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
    ]
)

def main():
    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt_text)])
    ]

    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
        ),
    )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    output = None
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        output = response.text
        if args.verbose:
            print(f'User prompt: {prompt_text}')
            print(output)
            print(f'Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}')
        else:
            print(output)

if __name__ == "__main__":
    main()