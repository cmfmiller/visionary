import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time
#import scrape_spokane_functions as ssf
import car_counting_functions as ccf
import glob
import os
import matplotlib.pyplot as plt
import datetime
#import plotly.express as px

# is today a weekend?
weekday, weekend = (0,1,2,3,4) , (6,5)
today_is_we = datetime.datetime.today().weekday() in weekend


dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

current_data = pd.read_csv("visionary/data/processed/just_yolo.csv", parse_dates=['date_time'], date_parser=dateparse)

indexed = current_data.set_index( "date_time")

hourly = indexed.groupby(['Parking_lot']).resample('H').mean()
#print(hourly.info())
#print(hourly.head())

hourly = hourly.reset_index()
hourly['day_of_week'] = hourly['date_time'].dt.day_name()
#print(hourly.head())

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekends = ["Saturday", "Sunday"]

hourly["is_weekend"] = hourly.day_of_week.apply(lambda x: True if x in weekends else False)
#print(hourly.head())

hourly = hourly.set_index("date_time")

weekday_vs_weekend = hourly.groupby(['Parking_lot', 'is_weekend', hourly.index.hour]).mean()

weekday_vs_weekend = weekday_vs_weekend.reset_index()

weekday_vs_weekend["yolo_pct"] = weekday_vs_weekend["yolo_car_count"].rank(pct=True)

#print(weekday_vs_weekend.info())


def latest_image(folder_path):
    list_of_files = glob.glob(folder_path) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


image_folder = "visionary/data/raw/"    
cam_list = []
for (dirpath, dirnames, filenames) in os.walk(image_folder):
    cam_list.extend(dirnames)
    break
    
cam_paths = [image_folder + cam + "/*" for cam in cam_list]
    
new_image_paths = [latest_image(path) for path in cam_paths]

new_image_dict = {cam:image for cam, image in zip(cam_list, new_image_paths)}
    


"""
# Trailhead Tracks
Live updates and forcasts of parking availability at Spokane County Trailheads
"""

"""
## Antoine Peak West Trailhead (Antoine Peak Conservation Area)
"""
just_ant = current_data[current_data.Parking_lot == "AntoineW"]
just_ant["yolo_pct"] = just_ant["yolo_car_count"].rank(pct=True)
ant_current = just_ant[just_ant["date_time"] == max(just_ant.date_time)]

labels = ["now"]
x = np.arange(len(ant_current.date_time))  # the label locations
width = 0.9

fig, ax = plt.subplots(figsize=(10, 1))
rects = ax.barh(labels, ant_current.yolo_pct, width)

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('')
ax.set_title('Current Popularity')
plt.xlim(0,1)

fig.tight_layout()
st.pyplot()

#st.image(new_image_dict["AntoineW"])
#pics = {
#    "Cat": "https://cdn.pixabay.com/photo/2016/09/24/22/20/cat-1692702_960_720.jpg",
#    "Puppy": "https://cdn.pixabay.com/photo/2019/03/15/19/19/puppy-4057786_960_720.jpg",
#    "Sci-fi city": "https://storage.needpix.com/rsynced_images/science-fiction-2971848_1280.jpg"
#}
#pic = st.selectbox("Picture choices", list(pics.keys()), 0)
#st.image(pics[pic], use_column_width=True, caption=pics[pic])

wd_ant = weekday_vs_weekend[(weekday_vs_weekend["is_weekend"] ==  today_is_we) & (weekday_vs_weekend["Parking_lot"] == "AntoineW")]
#print(wd_Glen.info())
#print(wd_Glen.head())

labels = list(wd_ant.date_time)
x = np.arange(len(wd_ant.date_time))  # the label locations
width = 0.9

fig, ax = plt.subplots()
rects = ax.bar(x, wd_ant.yolo_pct, width)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('')
ax.set_title('Popular Times Today')
ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.ylim(top =1)
fig.tight_layout()

st.pyplot()

"""
## Iller Creek Trailhead (Dishman Hills - Iller Creek Unit)
"""
just_ill = current_data[current_data.Parking_lot == "IllerCreek"]
just_ill["yolo_pct"] = just_ill["yolo_car_count"].rank(pct=True)
ill_current = just_ill[just_ill["date_time"] == max(just_ill.date_time)]

labels = ["now"]
x = np.arange(len(ill_current.date_time))  # the label locations
width = 0.9

fig, ax = plt.subplots(figsize=(10, 1))
rects = ax.barh(labels, ill_current.yolo_pct, width)

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('')
ax.set_title('Current Popularity')
plt.xlim(0,1)

fig.tight_layout()
st.pyplot()

wd_ill = weekday_vs_weekend[(weekday_vs_weekend["is_weekend"] ==  today_is_we) & (weekday_vs_weekend["Parking_lot"] == "IllerCreek")]
#print(wd_Glen.info())
#print(wd_Glen.head())

labels = list(wd_ill.date_time)
x = np.arange(len(wd_ill.date_time))  # the label locations
width = 0.9

fig, ax = plt.subplots()
rects = ax.bar(x, wd_ill.yolo_pct, width)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('')
ax.set_title('Popular Times Today')
ax.set_xticks(x)
ax.set_xticklabels(labels)

fig.tight_layout()

st.pyplot()

"""
## Glenrose Trailhead (Dishman Hills - Glenrose Unit)
"""
just_glen = current_data[current_data.Parking_lot == "Glenrose"]
just_glen["yolo_pct"] = just_glen["yolo_car_count"].rank(pct=True)
glen_current = just_glen[just_glen["date_time"] == max(just_glen.date_time)]

labels = ["now"]
x = np.arange(len(glen_current.date_time))  # the label locations
width = 0.9

fig, ax = plt.subplots(figsize=(10, 1))
rects = ax.barh(labels, glen_current.yolo_pct, width)

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('')
ax.set_title('Current Popularity')
plt.xlim(0,1)

fig.tight_layout()
st.pyplot()


wd_Glen = weekday_vs_weekend[(weekday_vs_weekend["is_weekend"] ==  today_is_we) & (weekday_vs_weekend["Parking_lot"] == "Glenrose")]
#print(wd_Glen.info())
#print(wd_Glen.head())

labels = list(wd_Glen.date_time)
x = np.arange(len(wd_Glen.date_time))  # the label locations
width = 0.9

fig, ax = plt.subplots()
rects = ax.bar(x, wd_Glen.yolo_pct, width)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('')
ax.set_title('Popular Times Today')
ax.set_xticks(x)
ax.set_xticklabels(labels)

fig.tight_layout()

st.pyplot()

"""
## Slavin Conservation Area Trailhead
"""
just_slv = current_data[current_data.Parking_lot == "Slavin"]
just_slv["yolo_pct"] = just_slv["yolo_car_count"].rank(pct=True)
slv_current = just_slv[just_slv["date_time"] == max(just_slv.date_time)]

labels = ["now"]
x = np.arange(len(slv_current.date_time))  # the label locations
width = 0.9

fig, ax = plt.subplots(figsize=(10, 1))
rects = ax.barh(labels, slv_current.yolo_pct, width)

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('')
ax.set_title('Current Popularity')
plt.xlim(0,1)

fig.tight_layout()
st.pyplot()


wd_slav = weekday_vs_weekend[(weekday_vs_weekend["is_weekend"] == today_is_we) & (weekday_vs_weekend["Parking_lot"] == "Slavin")]
#print(wd_Glen.info())
#print(wd_Glen.head())

labels = list(wd_slav.date_time)
x = np.arange(len(wd_slav.date_time))  # the label locations
width = 0.9

fig, ax = plt.subplots()
rects = ax.bar(x, wd_slav.yolo_pct, width)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('')
ax.set_title('Popular Times Today')
ax.set_xticks(x)
ax.set_xticklabels(labels)

fig.tight_layout()

st.pyplot()
