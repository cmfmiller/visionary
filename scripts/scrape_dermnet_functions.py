#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 21:27:16 2020

@author: cmfmiller
"""

# Web scraping tools
import lxml.html as lx
import requests
import numpy as np

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
            

# get all links for multipule pages of images (dermnet.com)
def get_all_urls(base_url):
    # get response from url
    page1_url = base_url + "1"
    response = requests.get(page1_url)
    response.raise_for_status()

    # parse response to html
    html = lx.fromstring(response.text)
    html.make_links_absolute(page1_url)    

    # count the number of pages with images
    page_links = html.xpath("//div[contains(@class, 'pagination')]/a")
    
    # divide by 2 becuase there links are repeated at top and bottom of the page
    page_count = len(page_links)//2 # integer division

    # generate list of all page urls for given rash
    all_page_urls = [base_url + str(count) for count in list(np.arange(1, page_count + 1))]
    return all_page_urls 
            

# wrapper DermnetNZ for a start page for specific rash 
def dermnetNZ_wrapper(start_url, key_word, base_path):
 
    pic_links = get_picture_links( start_url, key_word)
    
    for count, link in enumerate(pic_links, 1):
        try:
            path = base_path + "dermnetNZ" + str(count) + ".jpeg"
            save_image(link, path)
        except:
            print("no picture")
            
# wrapper for Dermnet for a specific rash
def dermnet_wrapper(start_url, key_word, base_path):
    page_urls = get_all_urls(start_url)

    pic_links = []
    for url in page_urls:
        links = get_picture_links(url, key_word)
        pic_links.extend(links)
    
    for count, link in enumerate(pic_links, 1):
        try:
            path = base_path + "dermnet" + str(count) + ".jpeg"
            save_image(link, path)
        except:
            print("no picture")            
