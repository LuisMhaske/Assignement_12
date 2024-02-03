import csv
import json
import pickle
import os
import sys

class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        raise NotImplementedError("Subclasses must implement the read method.")

    def save(self, data):
        raise NotImplementedError("Subclasses must implement the save method.")

class CSVReader(FileReader):
    def read(self):
        with open(self.file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            return [row for row in reader]

    def save(self, data):
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

class JSONReader(FileReader):
    def read(self):
        with open(self.file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {self.file_path}")
                return None

    def save(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=2)

class PickleReader(FileReader):
    def read(self):
        with open(self.file_path, 'rb') as file:
            return pickle.load(file)

    def save(self, data):
        with open(self.file_path, 'wb') as file:
            pickle.dump(data, file)

def modify_file(source_file, destination_file, changes):
    _, source_ext = os.path.splitext(source_file)
    _, dest_ext = os.path.splitext(destination_file)
    source_ext, dest_ext = source_ext.lower(), dest_ext.lower()

    valid_extensions = {'.csv', '.json', '.pickle'}

    if source_ext not in valid_extensions or dest_ext not in valid_extensions:
        print("Unsupported file type.")
        return

    if source_ext == '.csv':
        reader = CSVReader(source_file)
    elif source_ext == '.json':
        reader = JSONReader(source_file)
    elif source_ext == '.pickle':
        reader = PickleReader(source_file)

    file_data = reader.read()

    if file_data is None:
        return  # Exit if there's an issue reading the file

    for change in changes:
        try:
            col, row, value = map(str.strip, change.split(','))
            col, row = int(col), int(row)
            file_data[row][col] = value
        except ValueError:
            print(f"Invalid change format: {change}")

    reader.save(file_data)
    print(f"File successfully modified and saved to {destination_file}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python reader.py source_file destination_file change1 change2 ...")
    else:
        source_file = sys.argv[1]
        destination_file = sys.argv[2]
        changes = sys.argv[3:]

        if not os.path.isfile(source_file):
            print(f"Error: Source file '{source_file}' not found.")
            files_in_directory = [f for f in os.listdir('.') if os.path.isfile(f)]
            print("Files in the current directory:")
            for file in files_in_directory:
                print(file)
        else:
            modify_file(source_file, destination_file, changes)
