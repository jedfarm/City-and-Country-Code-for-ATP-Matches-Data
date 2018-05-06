#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 17:58:00 2018
Uses the file generated by atp_matches_union_updated.py and insert city names and 
country codes in there.
@author: jedfarm
"""

import pandas as pd
import numpy as np

df = pd.read_csv("atp_matches_tour_level.csv")

# Parse datetime
df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y%m%d', 
     errors='coerce')
df['tourney_date'] = df['tourney_date'].apply(lambda x: x.date())

tourney_name_list = list(df.tourney_name.unique())
tourney_name_new = []
for item in tourney_name_list:
    tourney_name_new.append(item.lower().strip())


df2 = pd.read_csv("atp_tourney_locations.csv")

def rename_tourneys(tourney):
    """
    Three masters tournaments in 2017 had their Masters part of the name missing
    """
    
    output = tourney
    if tourney == 'Madrid':
        output = 'Madrid Masters'
    elif tourney == 'Monte Carlo':
        output = 'Monte Carlo Masters'
    elif tourney == 'Rome':
        output = 'Rome Masters'
    return output

df['tourney_name']= df['tourney_name'].apply(rename_tourneys)
        
  
def add_location(df2, df_tourney_name, df_tourney_date):
    """
    Adds city name and country to each row, based on tourney_name
    """
    output = ['NOT FOUND', 'NOT FOUND']
    df_tourney_name = df_tourney_name.lower().strip()
    if not df2['tourney_name'][df2['tourney_name'].isin([df_tourney_name])].empty:
        idx = df2['tourney_name'][df2['tourney_name'].isin([df_tourney_name])].index[0]
        if df_tourney_name == 'canada masters':
            if df_tourney_date.year % 2 == 0:
                output = ['Toronto', 'Canada']
            else:
                output = ['Montreal', 'Canada']
        else:
                output = [df2['city'][idx], df2['country'][idx] ]
    return output

df['city'] = df[['tourney_name', 'tourney_date']].apply(
        lambda x: add_location(df2, *x)[0], axis=1)           
            
df['country'] = df[['tourney_name', 'tourney_date']].apply(
        lambda x: add_location(df2, *x)[1], axis=1)           
                
df.to_csv("atp_tour_tournaments_2000_2017.csv", index = False, encoding='utf-8')



 