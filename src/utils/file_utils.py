# File handling utilities

import os
import shutil
import json
import yaml

def read_json(file_path):
    """
    Read a JSON file
    :param file_path: Path to the JSON file
    :return: Parsed JSON data
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(data, file_path):
    """
    Write data to a JSON file
    :param data: Data to write
    :param file_path: Path to the JSON file
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def read_yaml(file_path):
    """
    Read a YAML file
    :param file_path: Path to the YAML file
    :return: Parsed YAML data
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def write_yaml(data, file_path):
    """
    Write data to a YAML file
    :param data: Data to write
    :param file_path: Path to the YAML file
    """
    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file, default_flow_style=False)

def ensure_dir(directory):
    """
    Ensure that a directory exists
    :param directory: Directory path
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def delete_dir(directory):
    """
    Delete a directory
    :param directory: Directory path
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)
