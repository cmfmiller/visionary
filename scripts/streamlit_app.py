import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time
#import scrape_spokane_functions as ssf
#import car_counting_functions as ccf
import glob
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import datetime
#import plotly.express as px
import pytz
import boto3
import io
from PIL import Image 

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
dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
current_data = pd.read_csv(io.BytesIO(body), parse_dates=['date_time'], date_parser=dateparse)
#print(current_data.info())

# is today a weekend?
weekday, weekend = (0,1,2,3,4) , (6,5)
today_is_we = datetime.datetime.today().weekday() in weekend

# current hour
utc_now = pytz.utc.localize(datetime.datetime.utcnow())
pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
hour = int (pst_now.strftime("%H"))

# read in data
#dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
#current_data = pd.read_csv("visionary/data/processed/just_yolo.csv", parse_dates=['date_time'], date_parser=dateparse)

# calculate poplular times based on most recent data
indexed = current_data.set_index( "date_time")

hourly = indexed.groupby(['Parking_lot']).resample('H').mean()
hourly = hourly.reset_index()
hourly['day_of_week'] = hourly['date_time'].dt.day_name()

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekends = ["Saturday", "Sunday"]

hourly["is_weekend"] = hourly.day_of_week.apply(lambda x: True if x in weekends else False)
hourly = hourly.set_index("date_time")
weekday_vs_weekend = hourly.groupby(['Parking_lot', 'is_weekend', hourly.index.hour]).mean()
weekday_vs_weekend = weekday_vs_weekend.reset_index()

# calculate percentile of the car counts by parking lot, excluding zeros for summary data and all data
weekday_vs_weekend["yolo_car_count"]  = weekday_vs_weekend["yolo_car_count"].replace(0, np.nan)
dist =  weekday_vs_weekend.groupby('Parking_lot').yolo_car_count.transform('max')
weekday_vs_weekend["yolo_pct"]= weekday_vs_weekend.yolo_car_count.div(dist)*100
#weekday_vs_weekend["yolo_pct"] = weekday_vs_weekend.groupby(["Parking_lot"]).yolo_car_count.rank(pct=True)
weekday_vs_weekend["yolo_pct"] = weekday_vs_weekend["yolo_pct"].replace(np.nan, 0)

current_data["yolo_car_count"] = current_data["yolo_car_count"].replace(0, np.nan)
dist_all =  current_data.groupby('Parking_lot').yolo_car_count.transform('max')
current_data["yolo_pct"]= current_data.yolo_car_count.div(dist)*100
#current_data["yolo_pct"] = current_data.groupby(["Parking_lot"]).yolo_car_count.rank(pct=True)
current_data["yolo_pct"] = current_data["yolo_pct"].replace(np.nan, 0)

# find most recent webcam images

def get_latest_file_name(bucket_name,file_path):
    """
    Return the latest file name in an S3 bucket folder.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (folder  name).
    """
    try:
        get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
        objs = s3client.list_objects_v2(Bucket=bucket_name, Prefix= file_path)['Contents']
        last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][-1]
    except:
        last_added = None
    
    return last_added

ec2_image_folder = "visionary/data/raw/"
cam_list = []
for (dirpath, dirnames, filenames) in os.walk(ec2_image_folder):
    cam_list.extend(dirnames)
    break

s3_folders = [ec2_image_folder.split("visionary/")[-1] + cam + "/" for cam in cam_list]    
new_image_paths = [get_latest_file_name(bucket, folder) for folder in s3_folders]
new_image_dict = {webcam:path for webcam, path in zip(cam_list, new_image_paths)}

#ploting functions
def show_webcam(bucket_name, image_path):
    try:
        s3 = boto3.resource('s3')
        s3bucket = s3.Bucket(bucket_name)
        image_object = s3bucket.Object(image_path)
        image = mpimg.imread(io.BytesIO(image_object.get()['Body'].read()), 'jpg')
    
        fig, ax = plt.subplots()
        ax.axis('off')
        ax.imshow(image)
        fig.tight_layout()

        st.pyplot()
    except:
        st.text("Webcam down")

def plot_popular_times(df, hour):
    labels = list(df.date_time)
    x = np.arange(len(df.date_time))  # the label locations
    y = df.yolo_pct
    width = 0.8

    fig, ax = plt.subplots()
    mask1 = y < 50
    mask2 = (y >= 50) & (y < 75)
    mask3 = y >= 75
    now_mask = x == hour

    plt.bar(x[now_mask], y[now_mask] + .01, width = 1.1)
    plt.bar(x[mask1], y[mask1], color = "#508104", width = width)
    plt.bar(x[mask2], y[mask2], color = "#f3b800", width = width)
    plt.bar(x[mask3], y[mask3], color = '#b64201', width = width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    #ax.set_ylabel('')
    ax.set_title('Popular Times Today')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    plt.ylim(top = 100)

    fig.tight_layout()

    st.pyplot()

def plot_current(df):
    labels = ["now"]
    x = np.arange(len(df.date_time))  # the label locations
    y = float(df.yolo_pct)

    mask1 = y < 50
    mask2 = (y >= 50) & (y < 75)
    mask3 = y >= 75

    fig, ax = plt.subplots(figsize=(10, 1))
    if mask1:
        plt.barh(labels, y, color = "#508104")
    if mask2:
        plt.barh(labels, y, color = "#f3b800")
    if mask3:
        plt.barh(labels, y, color = '#b64201')

    ax.set_title('Current Popularity')
    plt.xlim(0,100)

    fig.tight_layout()

    st.pyplot()

"""
# Trailheads-Up
Live updates and forecasts of trailhead popularity
"""

#View_webcams = st.sidebar.checkbox("View Webcams")
#View_popular_times = st.sidebar.checkbox("View Popular Times")

"""
## Antoine Peak West Trailhead (Antoine Peak Conservation Area)
"""
# most rendent car count for antoine W
just_ant = current_data[current_data.Parking_lot == "AntoineW"]
ant_current = just_ant[just_ant.date_time == max(just_ant.date_time)]

plot_current(ant_current)

if st.checkbox("Antoine Peak West Webcam"):
    show_webcam(bucket, new_image_dict["AntoineW"])
#st.image(new_image_dict["AntoineW"], use_column_width = True)

#if View_webcams:
#    st.image(new_image_dict["AntoineW"])

# find polular times for Antoine W based on weekend vs weekday
wd_ant = weekday_vs_weekend[(weekday_vs_weekend["is_weekend"] ==  today_is_we) & (weekday_vs_weekend["Parking_lot"] == "AntoineW")]

# plot popular times, highlighting current hour
if st.checkbox("Antoine Peak West Popular Times"):
    plot_popular_times(wd_ant, hour)

#if View_popular_times:
#    plot_popular_times(wd_ant, hour)


"""
## Stevens Creek Trailhead (Dishman Hills - Iller Creek Unit)
"""
#st.text("Stevens Creek Webcam is under repair. Be back soon!")
just_ste = current_data[current_data.Parking_lot == "StevensCreek"]
ste_current = just_ste[just_ste["date_time"] == max(just_ste.date_time)]

plot_current(ste_current)

if st.checkbox("Stevens Creek Webcam"):
    #st.text("webcam down")
    show_webcam(bucket, new_image_dict["StevensCreek"])   
    #st.image(new_image_dict["StevensCreek"],use_column_width = True)

#if View_webcams:
#    st.image(new_image_dict["StevensCreek"])

wd_ste = weekday_vs_weekend[(weekday_vs_weekend["is_weekend"] ==  today_is_we) & (weekday_vs_weekend["Parking_lot"] == "StevensCreek")]

if st.checkbox("Stevens Creek Popular Times"):
    plot_popular_times(wd_ste, hour)

#if View_popular_times:
#    plot_popular_times(wd_ste, hour)

"""
## Iller Creek Trailhead (Dishman Hills - Iller Creek Unit)
"""
just_ill = current_data[current_data.Parking_lot == "IllerCreek"]
ill_current = just_ill[just_ill["date_time"] == max(just_ill.date_time)]

plot_current(ill_current)

if st.checkbox("Iller Creek Webcam"):
    show_webcam(bucket, new_image_dict["IllerCreek"])    
#st.image(new_image_dict["IllerCreek"], use_column_width = True )

#if View_webcams:
#    st.image(new_image_dict["IllerCreek"])

wd_ill = weekday_vs_weekend[(weekday_vs_weekend["is_weekend"] ==  today_is_we) & (weekday_vs_weekend["Parking_lot"] == "IllerCreek")]

if st.checkbox("Iller Creek Popular Times"):
    plot_popular_times(wd_ill, hour)

#if View_popular_times:
#    plot_popular_times(wd_ill, hour)

"""
## Glenrose Trailhead (Dishman Hills - Glenrose Unit)
"""

just_glen = current_data[current_data.Parking_lot == "Glenrose"]
glen_current = just_glen[just_glen["date_time"] == max(just_glen.date_time)]

plot_current(glen_current)

if st.checkbox("Glenrose Webcam"):
    show_webcam(bucket, new_image_dict["Glenrose"])
    #st.image(new_image_dict["Glenrose"], use_column_width = True )

#if View_webcams:
#    st.image(new_image_dict["Glenrose"])

wd_Glen = weekday_vs_weekend[(weekday_vs_weekend["is_weekend"] ==  today_is_we) & (weekday_vs_weekend["Parking_lot"] == "Glenrose")]

if st.checkbox("Glenrose Popular Times"):
    plot_popular_times(wd_Glen, hour)

#if View_popular_times:
#    plot_popular_times(wd_Glen, hour)

"""
## Slavin Conservation Area Trailhead
"""

just_slv = current_data[current_data.Parking_lot == "Slavin"]
slv_current = just_slv[just_slv["date_time"] == max(just_slv.date_time)]

plot_current(slv_current)

if st.checkbox("Slavin Creek Webcam"):
    show_webcam(bucket, new_image_dict["Slavin"])
    #st.image(new_image_dict["Slavin"], use_column_width = True)

#if View_webcams:
#    st.image(new_image_dict["Slavin"])

wd_slv = weekday_vs_weekend[(weekday_vs_weekend["is_weekend"] ==  today_is_we) & (weekday_vs_weekend["Parking_lot"] == "Slavin")]

if st.checkbox("Slavin Chreek Popular Times"):
    plot_popular_times(wd_slv, hour)

#if View_popular_times:
#    plot_popular_times(wd_slv, hour)
