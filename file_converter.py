# file_converter.py
import argparse
import json
import yaml
import xml.etree.ElementTree as ET
from jsonschema import validate, ValidationError

def parse_arguments():
    parser = argparse.ArgumentParser(description="Konwerter plików")
    parser.add_argument("input_file", help="Ścieżka do pliku wejściowego")
    parser.add_argument("output_file", help="Ścieżka do pliku wyjściowego")
    parser.add_argument("input_format", choices=["xml", "json", "yml"], help="Format pliku wejściowego")
    parser.add_argument("output_format", choices=["xml", "json", "yml"], help="Format pliku wyjściowego")
    return parser.parse_args()

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            },
            "required": ["name", "age"]
        }
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            print(f"Validation error: {e.message}")
            return None
        return data

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            },
            "required": ["name", "age"]
        }
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            print(f"Validation error: {e.message}")
            return None
        return data

def load_xml(file_path):
       tree = ET.parse(file_path)
       root = tree.getroot()
       if not root.find("name") or not root.find("age"):
           print("Validation error: Required elements not found")
           return None
       return root

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

def save_xml(data, file_path):
       tree = ET.ElementTree(data)
       tree.write(file_path)

if __name__ == "__main__":
    args = parse_arguments()
    print(args)
