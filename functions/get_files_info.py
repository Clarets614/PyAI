import os

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