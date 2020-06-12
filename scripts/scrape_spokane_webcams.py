#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 12:24:29 2020

@author: cmfmiller
"""


import scrape_spokane_functions as ssf

spokane_webcams = "https://www.spokanecounty.org/4214/Trailhead-Web-Cams"

ssf.retrieve_webcam_images(spokane_webcams, "visionary/data/raw/")

