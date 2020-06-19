# import packages
import boto3
import io
import car_counting_functions as ccf
import glob
import pandas as pd
import os

# file and bucket names
bucket = 'visionarybucket'
data_file = "data/processed/just_yolo.csv"

# access S3 bucket
cred = boto3.Session().get_credentials()
ACCESS_KEY = cred.access_key
SECRET_KEY = cred.secret_key
SESSION_TOKEN = cred.token  ## optional

s3client = boto3.client('s3',
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = SECRET_KEY,
    aws_session_token = SESSION_TOKEN)

# read in historical data file to data frame from S3 bucket
response = s3client.get_object(Bucket = bucket, Key = data_file)
body = response["Body"].read()
previous = pd.read_csv(io.BytesIO(body))
print(len(previous))
print(previous.tail(50))
