"""
Author : Peter Kramar
Email : peter@ked.tech
This module contains helper functions for importing and exporting activity data.
"""


import os
import shutil
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import logging
from logging.handlers import RotatingFileHandler
import logging


def setup_logger():
    "Returns a singleton logger instance."
    logger = logging.getLogger('job_logger')
    if not logger.hasHandlers():
        handler = RotatingFileHandler('data/logs/job.log', maxBytes=10000, backupCount=10)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False
    return logger


def rename_log_file_to_activity_id(logger, activity_id):
    """
    Rename the log file to include the activity ID at the end of the job run.
    """
    temp_log_file = 'data/logs/job.log'
    new_log_file = f'data/logs/job_{activity_id}.log'
    if os.path.exists(temp_log_file):
        shutil.move(temp_log_file, new_log_file)
        logger.info(f"Log file renamed to {new_log_file}")
    else:
        logger.error(f"Temporary log file {temp_log_file} does not exist")

def upload_log_file_to_s3(activity_id):
    logger = setup_logger()
    client = boto3.client('s3', region_name='eu-central-1')
    log_file = f'data/logs/job_{activity_id}.log'
    key = f'job_{activity_id}.log'
    client.upload_file(log_file, 'lottie.logs', key)
    logger.info(f"Log file uploaded to S3 bucket with key: {key}")
    logger.info(f"Visit 'https://s3.eu-central-1.amazonaws.com/lottie.logs/{key}'")
    # open the log file in the code editor
    os.system(f"code {log_file}")
    return f"Log file uploaded successfully to S3 bucket."

def upload_image_to_s3(image_file, image_id):
    logger = setup_logger()
    client = boto3.client('s3', region_name='eu-central-1')   
    client.upload_fileobj(image_file, 'jskramar.materials', image_id, ExtraArgs={'ContentType': 'image/jpg', 'ContentDisposition': 'inline'})
    logger.info(f"Image uploaded to S3 bucket with key: {image_id}")
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
    logger = setup_logger()
    file_path = 'data/input.json'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            logger.info(f"Activity data imported from {file_path}")
            if len(data) == 0:
                raise Exception(f"{file_path} is empty.")
            elif len(data) > 1:
                raise Exception(f"{file_path} contains more than one activity.")
            return data[0]
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return e


def export_activity_data(data):
    "Exports activity data to a JSON file."
    logger = setup_logger()
    file_path = 'data/output.json'
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            logger.info(f"Activity data exported to {file_path}")
    except Exception as e:
        logger.error(f"Error writing {file_path}: {e}")
        return e
    

def append_activity_data_to_dataset(data):
    "Appends activity data to a JSON dataset."
    logger = setup_logger()
    file_path = 'data/history.json'
    try:
        with open(file_path, 'r') as file:
            dataset = json.load(file)
            dataset.append(data)
        with open(file_path, 'w') as file:
            json.dump(dataset, file, indent=4)
            logger.info(f"Activity data appended to {file_path}")
    except Exception as e:
        logger.error(f"Error writing to {file_path}: {e}")
        return e