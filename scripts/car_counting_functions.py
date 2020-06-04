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

def one_cam_paths(cam_folder_path):
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
  im = cv2.imread(image_path) 
  bbox, label, conf = cv.detect_common_objects(im)  
  car_count = label.count('truck') + label.count('car') + label.count('bus')
  return car_count

def show_image_detection(image_path):
  im = cv2.imread(image_path)
  bbox, label, conf = cv.detect_common_objects(im)
  output_image = draw_bbox(im, bbox, label, conf)
  plt.imshow(output_image)
  plt.show()
  
def yolo_counts_dict(image_path):
  yolo_count = car_count(image_path)
  cam_name = image_path.split("/")[-2]
  file_name = image_path.split("/")[-1]
  file_split = file_name.split("-")
  day = int(file_split[0])
  month = int(file_split[1])
  year = int(file_split[2])
  hour = int(file_split[3])
  minute = int(file_split[-1].split(".")[0])

  return {"Parking_lot": cam_name, 
          "file_name": file_name,  
          "month": month, 
          "day" : day, 
          "year": year,
          "hour" : hour,
          "minute": minute, 
          "yolo_car_count" : yolo_count}