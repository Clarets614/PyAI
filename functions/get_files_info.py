import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    target_path = os.path.join(working_directory, directory)
    abs_working = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(target_path)
    if not abs_dir.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'
    try:
        new_list = os.listdir(target_path)
        contents = []
        for item in new_list:
            full_item_path = os.path.join(target_path, item)
            line_item =  f'- {item}: file_size={os.path.getsize(full_item_path)} bytes, is_dir={os.path.isdir(full_item_path)}'
            contents.append(line_item)

        return "\n".join(contents)
    except Exception as e:
        return f'Error: {e}'