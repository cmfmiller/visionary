import boto3
import numpy as np
import pandas as pd
import io

bucket='visionarybucket'

cred = boto3.Session().get_credentials()
ACCESS_KEY = cred.access_key
SECRET_KEY = cred.secret_key
SESSION_TOKEN = cred.token  ## optional

s3client = boto3.client('s3',
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = SECRET_KEY,
    aws_session_token = SESSION_TOKEN)

s3_resource = boto3.resource('s3')

newest_





s3_resource.Bucket(bucket).upload_file(
    Filename= "visionary/data/processed/just_yolo.csv" , Key = "data/just_yolo.csv")
