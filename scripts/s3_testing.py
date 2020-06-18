import boto3
import numpy as np
import pandas as pd
import io

bucket='visionarybucket'

cred = boto3.Session().get_credentials()
ACCESS_KEY = cred.access_key
SECRET_KEY = cred.secret_key
SESSION_TOKEN = cred.token  ## optional

#print(ACCESS_KEY)
#print(SECRET_KEY)

s3client = boto3.client('s3',
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = SECRET_KEY,
    aws_session_token = SESSION_TOKEN)

#print(s3client.list_buckets())

s3_resource = boto3.resource('s3')

#s3_resource.Bucket(bucket).upload_file(
#    Filename= "visionary/data/processed/just_yolo.csv" , Key = "data/just_yolo.csv")

response = s3client.get_object(Bucket=bucket, Key= "data/processed/just_yolo.csv")
body = response["Body"].read()
current = pd.read_csv(io.BytesIO(body))

print(current.head())

csv_buffer = io.StringIO()
current.to_csv(csv_buffer)
s3_resource.Object(bucket, 'data/processed/just_yolo.csv').put(Body=csv_buffer.getvalue())


def get_latest_file_name(bucket_name,file_path):
    """
    Return the latest file name in an S3 bucket folder.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (folder  name).
    """
    #s3_client = boto3.client('s3')
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    paginator = s3client.get_paginator( "list_objects" )
    page_iterator = paginator.paginate(Bucket = bucket_name, Prefix = file_path)
    for page in page_iterator:
        if "Contents" in page:
            last_added = [obj['Key'] for obj in sorted( page["Contents"], key=get_last_modified)][-1]
    return last_added

#latest_filename = get_latest_file_name(bucket_name=bucket, file_path = 'data/raw/Glenrose/')

#print(latest_filename)

