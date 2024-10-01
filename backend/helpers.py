"""
Author : Peter Kramar
Email : peter@ked.tech
This module contains helper functions for importing and exporting activity data.
"""


import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError




def upload_image_to_s3(image_file, image_id):
    client = boto3.client('s3', region_name='eu-central-1')   
    client.upload_fileobj(image_file, 'jskramar.materials', image_id, ExtraArgs={'ContentType': 'image/jpg', 'ContentDisposition': 'inline'})
    return f"Image uploaded successfully to S3 bucket."


def get_secret_value(secret_id : str) -> str:
    "Retrieves the secret value from AWS Secrets Manager."
    secrets_manager = boto3.client('secretsmanager', region_name='eu-central-1')
    try:
        response = secrets_manager.get_secret_value(SecretId=secret_id)
        return json.loads(response['SecretString'])
    except (BotoCoreError, ClientError) as error: # pylint: disable=broad-except, unused-variable
        pass


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
            print(f"Activity exported to data/output.json.")
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return e
    
def append_activity_data_to_dataset(data):
    "Appends activity data to a JSON dataset."
    file_path = 'data/dataset.json'
    try:
        with open(file_path, 'r') as file:
            dataset = json.load(file)
            dataset.append(data)
        with open(file_path, 'w') as file:
            json.dump(dataset, file, indent=4)
            print(f"Activity appended to data/dataset.json.")
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return e