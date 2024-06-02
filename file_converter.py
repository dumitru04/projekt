import argparse
import json
import yaml
import xml.etree.ElementTree as ET
from jsonschema import validate, ValidationError
import asyncio
from PyQt5 import QtWidgets, QtCore
import sys

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
    data = {child.tag: child.text for child in root}
    if not data.get("name") or not data.get("age"):
        print("Validation error: Required elements not found")
        return None
    return data

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

def save_xml(data, file_path):
    root = ET.Element("root")
    for key, value in data.items():
        child = ET.Element(key)
        child.text = str(value)
        root.append(child)
    tree = ET.ElementTree(root)
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

        self.helpButton = QtWidgets.QPushButton('Help', self)
        self.helpButton.move(100, 100)
        self.helpButton.clicked.connect(self.show_help)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('File Converter')
        self.show()

    def convert(self):
        input_file = self.inputFileEdit.text()
        output_file = self.outputFileEdit.text()
        loop = asyncio.get_event_loop()
        input_format = self.get_format(input_file)
        output_format = self.get_format(output_file)
        data = loop.run_until_complete(load_file_async(input_file, input_format))
        if data:
            loop.run_until_complete(save_file_async(data, output_file, output_format))

    def get_format(self, file_path):
        if file_path.endswith(".json"):
            return "json"
        elif file_path.endswith(".yml") or file_path.endswith(".yaml"):
            return "yml"
        elif file_path.endswith(".xml"):
            return "xml"
        else:
            raise ValueError("Unsupported file format")

    def show_help(self):
        help_text = (
            "Instrukcja obsługi:\n\n"
            "1. Wprowadź pełną ścieżkę do pliku wejściowego w polu 'Input File'.\n"
            "2. Wprowadź pełną ścieżkę do pliku wyjściowego w polu 'Output File'.\n"
            "3. Upewnij się, że rozszerzenie pliku wejściowego i wyjściowego jest poprawne i obsługiwane.\n"
            "4. Kliknij przycisk 'Convert', aby przeprowadzić konwersję.\n\n"
            "Obsługiwane formaty:\n"
            "- .json\n"
            "- .yml / .yaml\n"
            "- .xml\n\n"
            "Przykład:\n"
            "Input File: C:\\Users\\Username\\Documents\\input.json\n"
            "Output File: C:\\Users\\Username\\Documents\\output.xml"
        )
        QtWidgets.QMessageBox.information(self, "Help", help_text)

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = ConverterApp()
    sys.exit(app.exec_())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = parse_arguments()
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(load_file_async(args.input_file, args.input_format))
        if data:
            loop.run_until_complete(save_file_async(data, args.output_file, args.output_format))
    else:
        main()
