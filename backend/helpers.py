"""
Author : Peter Kramar
Email : peter@ked.tech
This module contains helper functions for importing and exporting activity data.
"""


import json


def import_activity_data():
    "Imports activity data from a JSON file."
    file_path = 'data/input.json'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print(data)
            print(f"Input Data imported successfully from {file_path}.")
            if len(data) == 0:
                raise Exception(f"{file_path} is empty.")
            elif len(data) > 1:
                raise Exception(f"{file_path} contains more than one activity.")
            return data[0]
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return e

def export_activity_data(data):
    "Exports activity data to a JSON file."
    file_path = 'data/output.json'
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return e