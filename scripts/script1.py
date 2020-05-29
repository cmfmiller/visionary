#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 21:27:16 2020

@author: cmfmiller
"""


# standard packages
import numpy as np
import pandas as pd
import scipy as sp 

# Web scraping tools
import requests
import requests_cache

# create cache for requested html code to limit repeat requests
requests_cache.install_cache("rashy")

url = "https://dermnetnz.org/topics/varicella-images/"
response = requests.get()