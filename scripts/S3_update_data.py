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
#print(previous.info())
#print(previous.tail())

# find most recent cam pictures on EC2
base_path = "visionary/data/raw/"

cam_list = []
for (dirpath, dirnames, filenames) in os.walk(base_path):
    cam_list.extend(dirnames)
    break

cam_paths = [base_path + cam + "/*" for cam in cam_list]

most_recent_files = [ccf.latest_image(path) for path in cam_paths]
filtered = list(filter(None, most_recent_files))
#print(filtered)

# run newest images through car counting model
new_counts = [ccf.yolo_counts_dict(image) for image in filtered] # time limiting step

# make new counts into a dataframe
new_df = pd.DataFrame(new_counts)

# format datetime for new images
date_format ='%d-%m-%Y-%H-%M'
new_df['date_time'] = pd.to_datetime(new_df['date_time'], format = date_format)
new_df = new_df.drop(['file_name'], 1)

# add new data too historical dataframe
all_data = pd.concat([previous, new_df])
all_data = all_data.dropna(axis=0, how= 'any')
all_data.drop_duplicates(inplace = True)
#print(all_data.info())
#print(all_data.tail())

# over write datafile in S3
s3_resource = boto3.resource('s3')
csv_buffer = io.StringIO()
all_data.to_csv(csv_buffer, index=False)
s3_resource.Object(bucket, 'data/processed/just_yolo.csv').put(Body=csv_buffer.getvalue())
