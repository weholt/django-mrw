import re
import os


def extract_code_blocks(content):
    """
    Extract code blocks from the content using # filename: and # endof as delimiters.

    Args:
        content (str): The content from which to extract code blocks.

    Yields:
        str: Code block text.
    """
    code_block_pattern = r"# filename: (.*?)# endof"
    matches = re.findall(code_block_pattern, content, re.DOTALL)

    for match in matches:
        yield match.strip()


def parse_chat(content, app_name, root_folder):
    """
    Parse the content received from the chat to extract code blocks and map them to filenames.

    Args:
        content (str): The content received from the chat.
        app_name (str): The name of the Django app.
        root_folder (str): The root folder of the Django project.

    Returns:
        dict: A dictionary with file paths as keys and file contents as values.
    """
    parsed_data = {}

    for block in extract_code_blocks(content):
        lines = block.splitlines()
        if not len(lines) > 1:
            continue
        filename = lines[0].strip()
        file_path = os.path.join(root_folder, app_name, filename)
        file_content = "\n".join(lines[1:])
        parsed_data[file_path] = file_content
    return parsed_data
