import os

def write_file(working_directory, file_path, content):
    
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_dir = os.path.abspath(working_directory)
    common_path = os.path.commonpath([abs_dir, full_path])
    try:
        if abs_dir != common_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {e}'
    
    try:
        if not os.path.exists(full_path):
            new_path = os.path.dirname(full_path)
            os.makedirs(new_path, exist_ok=True)
    except Exception as e:
        return f'Error: {e}'
    
    try:
        with open(full_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: {e}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
