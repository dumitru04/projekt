# file_converter.py
import argparse
import json
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
        # Przykładowa weryfikacja schematu
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

if __name__ == "__main__":
    args = parse_arguments()
    print(args)
