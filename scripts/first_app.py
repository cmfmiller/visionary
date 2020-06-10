#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 13:51:26 2020

@author: cmfmiller
"""


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
import matplotlib as plt



"""
# Trailhead Tracker
Occupancy of Spokane County Trailheads
"""

# cam picutres"
base_path = "/Users/cmfmiller/Dropbox/Insight/visionary/data/raw/"
cams = ["AntoineW", "Glenrose", "IllerCreek", "StevensCreek"]
cam_paths = [base_path + cam + "/*" for cam in cams]

def latest_image(cam_path):
   list_of_files = glob.glob(cam_path) # * means all if need specific format then *.csv
   latest_file = max(list_of_files, key=os.path.getctime)
   return latest_file


most_recent_files = [latest_image(path) for path in cam_paths]

most_recent_image = [ccf.show_image_detection(path) for path in most_recent_files]

most_recent_count = [ccf.car_count(path) for path in most_recent_files]

max_occupancy = [40, 17, 20, 20]
current_vacancy = [occ - count for occ, count in zip(max_occupancy, most_recent_count)]
by_lot = [[occ, vac] for occ, vac in zip(most_recent_count, current_vacancy)]


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = ["Occupied", "Vacant"]
explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

"""
## Antoine Peak West Trailhead (Antoine Peak Conservation Area)
"""
fig1, ax1 = plt.pyplot.subplots()
ax1.pie(by_lot[0], explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot()

st.image(most_recent_image[0], use_column_width = True)

"""
## Glenrose Trailhead (Dishman Hills - Glenrose Unit)

"""
fig2, ax2 = plt.pyplot.subplots()
ax2.pie(by_lot[1], explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot()

st.image(most_recent_image[1], use_column_width = True)

"""
## Iller Creek Trailhead (Dishman Hills - Iller Creek Unit)
"""
fig3, ax3 = plt.pyplot.subplots()
ax3.pie(by_lot[2], explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot()

st.image(most_recent_image[2], use_column_width = True)

"""
## Stevens Creek Trailhead (Dishman Hills - Iller Creek Unit)

"""
fig4, ax4 = plt.pyplot.subplots()
ax4.pie(by_lot[3], explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot()

st.image(most_recent_image[3], use_column_width = True)



