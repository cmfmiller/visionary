#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 10:37:45 2020

@author: cmfmiller
"""

# import scraping functions from file
import scrape_dermnet_functions as dn

# define paths to image page url
chicken_pox_url = "https://dermnetnz.org/topics/varicella-images/"
ring_worm_url = "https://www.dermnetnz.org/topics/tinea-corporis-images/"
herpes_simplex_url = "https://www.dermnetnz.org/topics/herpes-simplex-images/"
impetigo_url = "https://www.dermnetnz.org/topics/impetigo-images/"
pityriasis_url = "https://www.dermnetnz.org/topics/pityriasis-rosea-images/"

urls = [chicken_pox_url, ring_worm_url, herpes_simplex_url, impetigo_url, pityriasis_url]

# define keywords
cp_kw = "'Chickenpox'"
rw_kw = "'Tinea'"
hs_kw = "'Herpes'"
i_kw = "'impetigo'"
p_kw = "'rosea'" 

key_words = [cp_kw, rw_kw, hs_kw, i_kw, p_kw]

# define paths to each rash folder within data
cp_bp = "../data/raw/chicken_pox/"
rw_bp = "../data/raw/ring_worm/"
hs_bp = "../data/raw/herpes_simplex/"
i_bp = "../data/raw/impetigo/"
p_bp = "../data/raw/pityriasis/"

base_paths = [cp_bp, rw_bp, hs_bp, i_bp, p_bp]

# srape dermnet NZ for photos of all rashes
for url, kw, path in zip(urls, key_words, base_paths):
    dn.dermnetNZ_wrapper(start_url = url, base_path = path, key_word = kw)