import boto3
import os
import requests
import scrape_spokane_functions as ssf

import car_counting_functions as ccf
import glob
import os
import matplotlib as plt
import pandas as pd

# cam picutres"
base_path = "visionary/data/raw/"
all_csv_path = "visionary/data/processed/just_yolo.csv"

#def latest_image(cam_path):
#   list_of_files = glob.glob(cam_path) # * means all if need specific format then *.csv
#   latest_file = max(list_of_files, key=os.path.getctime)
#   return latest_file


cam_list = []
for (dirpath, dirnames, filenames) in os.walk(base_path):
    cam_list.extend(dirnames)
    break

cam_paths = [base_path + cam + "/*" for cam in cam_list]
#print(cam_paths)

most_recent_files = [ccf.latest_image(path) for path in cam_paths]
#print(most_recent_files)

new_counts = [ccf.yolo_counts_dict(image) for image in most_recent_files] # time limiting step
new_df = pd.DataFrame(new_counts)
#print(new_df)

# format datetime
date_format ='%d-%m-%Y-%H-%M'
new_df['date_time'] = pd.to_datetime(new_df['date_time'], format = date_format)
new_df = new_df.drop(['file_name'], 1)
#print(new_df)

previous = pd.read_csv(all_csv_path)
print(len(previous))
print(len(new_df))

all_data = pd.concat([previous, new_df])
all_data.dropna(axis=0, how= 'any')
print(len(all_data))

all_data.to_csv(all_csv_path)

#most_recent_image = [ccf.show_image_detection(path) for path in most_recent_files]

#most_recent_count = [ccf.car_count(path) for path in most_recent_files]
#print(most_recent_count)

#spokane_webcams = "https://www.spokanecounty.org/4214/Trailhead-Web-Cams")
