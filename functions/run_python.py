import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
     name="run_python_file",
    description="Execute Python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to run file from, relative to the working directory.",
            ),
            "arguments": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python file.",
                items=types.Schema(types.Type.STRING),
                )
        },
    ),
    )

def run_python_file(working_directory, file_path):
    if os.path.isabs(file_path):
         new_path = file_path
    else:
         new_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_dir = os.path.abspath(working_directory)
    common_path = os.path.commonpath([abs_dir, new_path])
    if abs_dir != common_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(new_path):
         return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
         return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(["python", file_path], timeout=30, capture_output=True, cwd=working_directory, text=True)
        output_string = ""
        if result.stdout:
            output_string += f'STDOUT:{result.stdout}'
        if result.stderr:
            output_string += f'STDERR:{result.stderr}'
        if result.returncode != 0:
            output_string += f'Process exited with code {result.returncode}'
        if not result.stdout and not result.stderr:
            output_string += "No output produced"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return output_string