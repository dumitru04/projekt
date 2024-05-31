# file_converter.py
import argparse
import json
import yaml
import xml.etree.ElementTree as ET
from jsonschema import validate, ValidationError
from PyQt5 import QtWidgets
import sys
import asyncio

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

async def load_file_async(file_path, format):
       if format == "json":
           return load_json(file_path)
       elif format == "yml":
           return load_yaml(file_path)
       elif format == "xml":
           return load_xml(file_path)

async def save_file_async(data, file_path, format):
       if format == "json":
           save_json(data, file_path)
       elif format == "yml":
           save_yaml(data, file_path)
       elif format == "xml":
           save_xml(data, file_path)

class ConverterApp(QtWidgets.QWidget):
       def __init__(self):
           super().__init__()
           self.initUI()

       def initUI(self):
           self.inputFileLabel = QtWidgets.QLabel('Input File:', self)
           self.inputFileLabel.move(20, 20)
           self.inputFileEdit = QtWidgets.QLineEdit(self)
           self.inputFileEdit.move(100, 20)

           self.outputFileLabel = QtWidgets.QLabel('Output File:', self)
           self.outputFileLabel.move(20, 60)
           self.outputFileEdit = QtWidgets.QLineEdit(self)
           self.outputFileEdit.move(100, 60)

           self.convertButton = QtWidgets.QPushButton('Convert', self)
           self.convertButton.move(20, 100)
           self.convertButton.clicked.connect(self.convert)

           self.setGeometry(300, 300, 300, 150)
           self.setWindowTitle('File Converter')
           self.show()

       def convert(self):
           input_file = self.inputFileEdit.text()
           output_file = self.outputFileEdit.text()

def main():
       app = QtWidgets.QApplication(sys.argv)
       ex = ConverterApp()
       sys.exit(app.exec_())

if __name__ == "__main__":
    args = parse_arguments()
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(load_file_async(args.input_file, args.input_format))
    if data:
        loop.run_until_complete(save_file_async(data, args.output_file, args.output_format))
