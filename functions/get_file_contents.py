import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents from a given path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to read files from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    target_path = os.path.join(working_directory, file_path)
    abs_working = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(target_path)
    if not abs_dir.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if os.path.getsize(target_path) > 10000:
        trunc_message = '[...File "{file_path}" truncated at 10000 characters]'
    else:
        trunc_message = ""
    try:
        MAX_CHARS = 10000
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        return f'{file_content_string} {trunc_message}'
    except Exception as e:
        return f'Error: {e}'