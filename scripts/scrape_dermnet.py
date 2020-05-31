#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 12:52:01 2020

@author: cmfmiller
"""


# import scraping functions from file
import scrape_dermnet_functions as dn

# define paths to image page url
chicken_pox_url = "http://www.dermnet.com/images/Varicella/photos/"
ring_worm_url = "http://www.dermnet.com/images/Tinea-Ringworm-Body/photos/"
herpes_simplex_url = "http://www.dermnet.com/images/Herpes-Simplex/photos/"
impetigo_url = "http://www.dermnet.com/images/Impetigo/photos/"
pityriasis_url = "http://www.dermnet.com/images/Pityriasis-Rosea/photos/"

urls = [chicken_pox_url, ring_worm_url, herpes_simplex_url, impetigo_url, pityriasis_url]

# define keywords
cp_kw = "'Varicella'"
rw_kw = "'Tinea'"
hs_kw = "'Herpes'"
i_kw = "'Impetigo'"
p_kw = "'Pityriasis'" 

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
    dn.dermnet_wrapper(start_url = url, base_path = path, key_word = kw)

