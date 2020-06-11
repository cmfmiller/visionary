#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 12:20:49 2020

@author: cmfmiller
"""

# Web scraping tools
import lxml.html as lx
import requests
import datetime
import pytz


# get most updated photos from spokane county parks department website
def get_webcam_links(url):
    response = requests.get(url)
    response.raise_for_status()
    # parse response to html
    html = lx.fromstring(response.text)
    html.make_links_absolute(url)    

    # count the number of pages with images
    image_links = html.xpath("//img[contains(@class, 'fr-dii')]/@src")
    return image_links

def dict_of_links(url):
    response = requests.get(url)
    response.raise_for_status()
    # parse response to html
    html = lx.fromstring(response.text)
    html.make_links_absolute(url)    

    # count the number of pages with images
    image_links = html.xpath("//img[contains(@class, 'fr-dii')]/@src")
    
    cam_names = [url.split("/")[-2] for url in image_links]
    
    link_dictionary = {cam_names[i]: image_links[i] for i in range(len(cam_names))}
    return link_dictionary
    

# save image to file
def save_image(image_link, file_path):
    with open(file_path, 'wb') as handle:
        response = requests.get(image_link, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

# wrapper function to retrieve and save web cam images
def retrieve_webcam_images(url, base_file_path = "../data/raw/"):
    # scrape website for most recent webcam images
    image_links = get_webcam_links(url)
    
    # get names of the parking lot
    cam_names = [url.split("/")[-2] for url in image_links]
    
    # get current time
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    dt_string = pst_now.strftime("%d-%m-%Y-%H-%M") 
    
    # generate file paths
    file_paths = []
    for cam in cam_names:
        path = base_file_path + cam + '/' + dt_string + ".jpeg"
        file_paths.append(path)
        
    # save images to file
    for img, file in zip(image_links, file_paths):
        save_image(img, file)