#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 20:26:01 2018

    Concatenates all csv files into one and create a new csv file.
    Correct the names of the US Open on some entries, (it was Us Open) 
    and the ATP Finals (which had two names for historical reasons)

@author: jedfarm
"""

import glob
import pandas as pd
import os
import numpy as np

path = r'/Users/jedfarm/Downloads/atp_matches_updated'
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f) for f in all_files)
df   = pd.concat(df_from_each_file, ignore_index=True)


def correct_tourneys_name(names_list, correct_name, tourney_name):
    if tourney_name in names_list:
        tourney_name = correct_name
    return tourney_name

names_list = ['Us Open']
correct_name = 'US Open'

df['tourney_name'] = df['tourney_name'].apply(
        lambda x: correct_tourneys_name(names_list, 
  correct_name, x))

names_list = ['Masters Cup', 'Tour Finals']
correct_name = 'Masters Cup / Tour Finals'
df['tourney_name'] = df['tourney_name'].apply(
        lambda x: correct_tourneys_name(names_list, 
  correct_name, x))   



# Keep only ATP 250, ATP 500, Master1000, GrandSlams & ATPTourFinals
tour_level = ['A', 'M', 'G', 'F']
tour_level_df = df[df['tourney_level'].isin(tour_level)]

tour_level_df.to_csv("atp_matches_tour_level.csv", encoding='utf-8', index=False)