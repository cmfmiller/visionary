import boto3
import os
import datetime
import pytz

bucket = "visionarybucket"
# open S3 session
# access S3 bucket
cred = boto3.Session().get_credentials()
ACCESS_KEY = cred.access_key
SECRET_KEY = cred.secret_key
SESSION_TOKEN = cred.token  ## optional

session = boto3.Session(
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = SECRET_KEY,
    aws_session_token = SESSION_TOKEN)

s3 = session.resource('s3')

# get current time
utc_now = pytz.utc.localize(datetime.datetime.utcnow())
pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
today = pst_now.strftime("%m_%d_%Y")


## set source and destination folders
# get list of webcam names
ec2_base = "visionary/data/raw/"

cam_list = []
for (dirpath, dirnames, filenames) in os.walk(ec2_base):
    cam_list.extend(dirnames)
    break
# define paths to raw data folders
s3_old_base = "data/raw/"
old_folder_keys = [s3_old_base + cam + "/" for cam in cam_list]

# define paths to archive data folders
s3_new_base = "data/archive/"
new_folder_keys = [s3_new_base + "weekof_" + today + "/" + cam  for cam in cam_list] 

# filter    
def archive_folder(bucket_name, old_folder_key, new_folder_key):
    bucket = s3.Bucket(bucket_name)
    for object in bucket.objects.filter(Prefix = old_folder_key):     
        src_key = object.key
        if not src_key.endswith('/'):
            file_name = src_key.split('/')[-1]
            dest_file_key = new_folder_key + '/' + file_name
            copy_source = bucket_name + '/' + src_key         
            s3.Object(bucket_name, dest_file_key).copy_from(CopySource = copy_source)
            s3.Object(bucket_name, src_key).delete()

for old, new in zip(old_folder_keys, new_folder_keys):
    archive_folder(bucket, old, new)

# Copy object A as object B
#s3_resource.Object(“bucket_name”, “newpath/to/object_B.txt”).copy_from(
# CopySource=”path/to/your/object_A.txt”)

# Delete the former object A
#s3_resource.Object(“bucket_name”, “path/to/your/object_A.txt”).delete()
