import os
import json

SYSTEM_PROMPT_FILENAME = "systemprompt.txt"


def read_file(directory, filename):
    """
    Read the content of a file in the specified directory.

    Args:
        directory (str): The directory where the file is located.
        filename (str): The name of the file to read.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist in the specified directory.
    """
    file_path = os.path.join(directory, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")

    with open(file_path, "r") as file:
        return file.read()


def read_json_file(directory, filename):
    """
    Reads and parses a JSON file from a specified directory.
    Args:
        directory (str): The directory path where the JSON file is located.
        filename (str): The name of the JSON file to read.
    Returns:
        dict: The parsed JSON content as a Python dictionary.
    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    file_path = os.path.join(directory, filename)
    with open(file_path, "r") as file:
        return json.load(file)


class AgentConfig(object):
    def __init__(self, directory_path):
        """
        Initialize a ConfigReader to read configuration files from a directory.

        Args:
            directory_path (str, optional): Path to the directory containing configuration files.
                                          Defaults to None.

        Raises:
            FileNotFoundError: If the systemprompt.txt file doesn't exist.
        """
        if not directory_path:
            raise ValueError("Directory path cannot be None")
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found at {directory_path}")
        self.system_prompt = read_file(directory_path, SYSTEM_PROMPT_FILENAME)
        settings = read_json_file(directory_path, "settings.json")
        self.app_title = settings.get("app_title", "Claude Chatbot")
        self.app_instructions = settings.get("app_instructions", "Ask me anything!")
        self.model = settings.get("model", "claude-1")
        self.max_tokens = settings.get("max_tokens", 1000)
        self.examples = settings.get("examples", [])
