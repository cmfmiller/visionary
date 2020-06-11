#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 16:55:16 2020

@author: cmfmiller
"""


import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import os
import numpy as np
import pandas as pd

def one_cam_paths(cam_folder_path):
    """
    list the paths to all images in a given folder

    Parameters
    ----------
    cam_folder_path : STR
        file path of a folder containing images from the same webcam

    Returns
    -------
    image_paths : LIST
        A list of file paths, one for each of the images in the folder

    """
    # create list of images for a cam 
    image_files = []
    for (dirpath, dirnames, filenames) in os.walk(cam_folder_path):
        image_files.extend(filenames)
        break

    # remove .DS file
    DS = ".DS_Store"
    if DS in image_files: 
        image_files.remove(DS)
  
    # generate full file paths for each image the the cam
    image_paths = [cam_folder_path + img for img in image_files]
    return image_paths

def get_image_paths(base_path):
    """
    Function to read the names of all the images in a given folder 
    and return file paths to each of them
    Parameters
    ----------
    base_path : STR
        A file path to folder cotaining images ending in "/".
        Expects the folder to contain several folders each containing images from a different webcam
    Returns
    -------
    all_image_paths : LIST
        returns a list of file paths, one to each image in the base folder

    """
    # get list of files for each camera
    cam_list = []
    for (dirpath, dirnames, filenames) in os.walk(base_path):
        cam_list.extend(dirnames)
        break

    # use cam list to generate file path to each cam
    cam_paths = [base_path + cam + "/" for cam in cam_list]
  
    # define list of paths to all images
    all_image_paths = []
    for path in cam_paths:
        image_paths = one_cam_paths(path) # defined above
        all_image_paths.extend(image_paths)
    
    return all_image_paths


def car_count(image_path):
    """

    Parameters
    ----------
    image_path : string
        expects a file path to an image in jpg format.

    Returns
    -------
    car_count: integer
        If the file path is valid, a count of the number of cars, trucks, and buses 
        in the image is returned.

    """    
    try:
        # read in image
        im = cv2.imread(image_path) 
        # detect objects in image
        bbox, label, conf = cv.detect_common_objects(im)  
        # sum the number of trucks cars and buses
        car_count = label.count('truck') + label.count('car') + label.count('bus')
    except:
        # if unable to read image return NA
        car_count = np.nan
        
    return car_count

def show_image_detection(image_path):
    '''
    Displays the objects detected in an image with color coded labels and bounding boxes

    Parameters
    ----------
    image_path : string
        File path to jpg image.

    Returns
    -------
    Image with objects labeled

    '''
    # read in image
    im = cv2.imread(image_path)
    # detect objects in image
    bbox, label, conf = cv.detect_common_objects(im)
    
    # plot all objects in image with bounding boxes
    output_image = draw_bbox(im, bbox, label, conf)
    return output_image
    #plt.imshow(output_image)
    #plt.show()

 
def yolo_counts_dict(image_path):
    """
    Counts cars in an image and also parses image name for date_time information

    Parameters
    ----------
    image_path : string
        file path to a jpg image

    Returns
    -------
    dict
        dictionary containing car count and identifying infromation for original image

    """
    yolo_count = car_count(image_path)
    cam_name = image_path.split("/")[-2]
    file_name = image_path.split("/")[-1]
    date_time = file_name.split(".")[0] #  format '%d-%m-%Y-%H-%M'
    
    return {"Parking_lot": cam_name, 
            "file_name": file_name,  
            "date_time": date_time, 
            "yolo_car_count" : yolo_count}

def add_new_images(new_folder, all_csv_path, validate = False, val_csv_path = np.nan):
    """
    Counts the cars in new set of images, and adds the new data to data frame containing all previous data
    Parameters
    ----------
    new_folder : string
        file path to a folder containing all new images
    all_csv_file : string
        file path to csv file containing all previously counted images
    validate: bool
        logical value (True or False) depending on whether the new date should be merged with a set of validation data
    val_csv_path: string
        file path to the validation data set, if one exists

    Returns
    -------
    pandas DataFrame
        dataframe of car counts and dates for all images
    """
    # load in all files up front so it fails early if this is the problem
    # previous data 
    previous = pd.read_csv(all_csv_path)

    # validation data if applicable
    if validate: 
        truth = pd.read_csv(val_csv_path)
    else:
        truth = np.nan

    # Count cars in new images and create dataframe
    new_image_paths = get_image_paths(new_folder)
    new_counts = [yolo_counts_dict(image) for image in new_image_paths] # time limiting step
    new_df = pd.DataFrame(new_counts)
    
    # format datetime
    date_format ='%d-%m-%Y-%H-%M'
    new_df['date_time'] = pd.to_datetime(new_df['date_time'], format = date_format)
    
    # merge datasets
    if validate: 
        # add validation data to object detector counts if applicable
        merged = pd.merge(left = new_df, right= truth, how='left',
                          left_on=  ["Parking_lot", "file_name"], 
                          right_on= ["Parking_lot", "image"])
        merged = merged.drop(["image", "file_name"], 1)
    else:
        merged = new_df.drop(['file_name'], 1)
    
    all_days = pd.concat([previous, merged])
    
    return(all_days)

def latest_image(folder_path):
    '''
    Get the file path to the most recent file in a folder

    Parameters
    ----------
    folder_path : STR
        file path to folder containing files you want to search for the most recent file

    Returns
    -------
    latest_file : STR
        absolute file path to the most recent file

    '''
    list_of_files = glob.glob(folder_path) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def add_current_images(image_folder, all_csv_path):
    '''
    Add the car counts of most recent images to the complete datafile

    Parameters
    ----------
    image_folder : STR
        file path to the folder containing raw data that has been scraped
    all_csv_path : STR
        file path to complete datafile

    Returns
    -------
    all_data : Pandas dataframe
        updated data frame containing data from the latest images.

    '''
    # previous data 
    previous = pd.read_csv(all_csv_path)
    
    cam_list = []
    for (dirpath, dirnames, filenames) in os.walk(image_folder):
        cam_list.extend(dirnames)
        break
    
    cam_paths = [base_path + cam + "/*" for cam in cam_list]
    
    new_image_paths = [latest_image(path) for path in cam_paths]
    
    new_counts = [yolo_counts_dict(image) for image in new_image_paths] # time limiting step
    new_df = pd.DataFrame(new_counts)
    
    # format datetime
    date_format ='%d-%m-%Y-%H-%M'
    new_df['date_time'] = pd.to_datetime(new_df['date_time'], format = date_format)
    
    all_data = pd.concat([previous, new_df])
    
    return(all_data)


