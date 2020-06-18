import boto3
import os
import glob
import car_counting_functions as ccf


# S3 bucket
bucket='visionarybucket'
# EC2 folder path
ec2_folder = "visionary/data/raw/"

# Access S3 bucket
cred = boto3.Session().get_credentials()
ACCESS_KEY = cred.access_key
SECRET_KEY = cred.secret_key
SESSION_TOKEN = cred.token  ## optional

s3client = boto3.client('s3',
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = SECRET_KEY,
    aws_session_token = SESSION_TOKEN)

# find most recent webcam images on EC2
cam_list = []
for (dirpath, dirnames, filenames) in os.walk(ec2_folder):
    cam_list.extend(dirnames)
    break

cam_paths = [ec2_folder + cam + "/*" for cam in cam_list]

most_recent_files = [ccf.latest_image(path) for path in cam_paths]

# create S3 file paths for files
s3_file_paths = [path.split("visionary/")[-1] for path in most_recent_files] 

# save new images to s3
s3_resource = boto3.resource('s3')

for image, path in zip(most_recent_files, s3_file_paths): 
    s3_resource.Bucket(bucket).upload_file(Filename = image , Key = path)

# delete files from EC2
for image in most_recent_files:
    os.remove(image)
