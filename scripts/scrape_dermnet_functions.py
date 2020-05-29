#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 21:27:16 2020

@author: cmfmiller
"""

# Web scraping tools
import lxml.html as lx
import requests

# get list of page links for each rash picture
def get_picture_links(start_page, key_word):
    
    response = requests.get(start_page)
    
    html = lx.fromstring(response.text)
    html.make_links_absolute(start_page)
    
    path = "//img[contains(@alt, {})]/@src".format(key_word)
    picture_links = html.xpath(path)
    return picture_links


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
            
            
# wrapper for a start page for a specific rash 
def dermnet_wrapper(start_url, key_word, base_path):
 
    pic_links = get_picture_links( start_url, key_word)
    
    for count, link in enumerate(pic_links, 1):
        try:
            path = base_path + "pic" + str(count) + ".jpeg"
            save_image(link, path)
        except:
            print("no picture")