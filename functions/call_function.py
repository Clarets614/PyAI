from google import genai
from google.genai import types
from functions.get_file_contents import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python import run_python

available_functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python": run_python, 
    }

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_args = dict(function_call_part.args)
    function_args["working_directory"] = "./calculator"
    
    if function_call_part.name not in available_functions:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                    name= function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    function_result = available_functions[function_call_part.name](**function_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ]
    )

