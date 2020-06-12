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

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

current_data = pd.read_csv("visionary/data/processed/just_yolo.csv", parse_dates=['date_time'], date_parser=dateparse)

print(current_data.info())

