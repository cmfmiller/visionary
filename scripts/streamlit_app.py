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

"""
# Trailhead Tracker
Live updates and forcasts of parking availability at Spokane County Trailheads
"""

"""
## Antoine Peak West Trailhead (Antoine Peak Conservation Area)
"""

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

fig.tight_layout()

st.pyplot()

"""
## Iller Creek Trailhead (Dishman Hills - Iller Creek Unit)
"""
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
