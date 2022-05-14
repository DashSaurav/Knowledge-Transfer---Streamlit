import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import time
import math
from statistics import mean
from math import ceil
import datetime
from ast import literal_eval
import streamlit as st
import os

df = pd.read_csv(r"pages/data/processed_clean_df.csv")
df['raw'] = df['raw'].apply(literal_eval)
print("csv",df)

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')#.date()
df['T_time'] = pd.to_datetime(df['T_time'], format='%H:%M:%S')#.time()
df['date'] = df['date'].dt.date
df['T_time'] = df['T_time'].dt.time

dff_kar = pd.read_csv("pages/data/processed_occ_df.csv")

dff_kar['date'] = pd.to_datetime(dff_kar['date'], format='%Y-%m-%d')
dff_kar['T_time'] = pd.to_datetime(dff_kar['T_time'], format='%H:%M:%S')
dff_kar['T_time'] = dff_kar['T_time'].dt.time
dff_kar['Camera3'] = dff_kar["Camera3"].astype(int)

def cleaning_times(start_date, end_date):
    # data = df[(df['date'] >= pd.to_datetime(str(start_date))) & (df['date'] <= pd.to_datetime(str(end_date)))]
    # data = data[['date','Room Number','Floor Cleaning Start Time','Floor Cleaning End Time', 'Deep Cleaning Start Time',
    #              'Deep Cleaning End Time','Floor Cleaning Duration','Deep Cleaning Duration','Avg Occupants']]

    # data.rename(columns = {'Floor Cleaning Start Time':'start_floor','Floor Cleaning End Time':'finish_floor',
    #                         'Deep Cleaning Start Time':'start_deep','Deep Cleaning End Time':'finish_deep'}, inplace = True)
    # data['start_floor'].replace(['0',''], '00:00:00', inplace=True)
    # data['finish_floor'].replace(['0',''], '00:00:00', inplace=True)
    # data['start_deep'].replace(['0', '00:00:00'], '00:00:00', inplace=True)
    # data['finish_deep'].replace(['0', '00:00:00'], '00:00:00', inplace=True)
    # return data.drop_duplicates()
    # strat from here.
    data = df[(df['date'] >= pd.to_datetime(str(start_date))) & (df['date'] <= pd.to_datetime(str(end_date)))]
    # taking data from dataframe
    new_df = data[["date","Floor Cleaning Start Time","Floor Cleaning End Time","Deep Cleaning Start Time","Deep Cleaning End Time"]]
    # renaming columns
    new_df.rename(columns = {'Floor Cleaning Start Time':'start_floor','Floor Cleaning End Time':'finish_floor','Deep Cleaning Start Time':'start_deep','Deep Cleaning End Time':'finish_deep'}, inplace = True)
    # replace where 0 to 00:00:00
    new_df['start_floor'].replace(['0',''], '00:00:00', inplace=True)
    new_df['finish_floor'].replace(['0',''], '00:00:00', inplace=True)
    new_df['start_deep'].replace(['0',''], '00:00:00', inplace=True)
    new_df['finish_deep'].replace(['0',''], '00:00:00', inplace=True)
    
    new_df['start_floor'] = pd.to_datetime(new_df['start_floor'])
    new_df['finish_floor'] = pd.to_datetime(new_df['finish_floor'])
    new_df['start_deep'] = pd.to_datetime(new_df['start_deep'])
    new_df['finish_deep'] = pd.to_datetime(new_df['finish_deep'])

    # Get Min Time Per Hour
    starts_floor = (
        new_df.groupby(['date', pd.Grouper(key='start_floor', freq='H')], as_index=False)
            .agg({'start_floor': 'min', 'date': 'first'})
    )
    # Get Max Time Per Hour
    ends_floor = (
        new_df.groupby(['date', pd.Grouper(key='finish_floor', freq='H')], as_index=False)
            .agg({'finish_floor': 'max', 'date': 'first'})
    )
    starts_deep = (
        new_df.groupby(['date', pd.Grouper(key='start_deep', freq='H')], as_index=False)
            .agg({'start_deep': 'min', 'date': 'first'})
    )
    ends_deep = (
        new_df.groupby(['date', pd.Grouper(key='finish_deep', freq='H')], as_index=False)
            .agg({'finish_deep': 'max', 'date': 'first'})
    )

    # Merge on Name and Same Hour
    new_df_floor = (
        starts_floor.merge(
            ends_floor,
            left_on=['date', starts_floor['start_floor'].dt.hour],
            right_on=['date', ends_floor['finish_floor'].dt.hour])
            .drop('key_1', 1)[['start_floor', 'finish_floor', 'date']]
    )

    new_df_deep = (
        starts_deep.merge(
            ends_deep,
            left_on=['date', starts_deep['start_deep'].dt.hour],
            right_on=['date', ends_deep['finish_deep'].dt.hour])
            .drop('key_1', 1)[['start_deep', 'finish_deep', 'date']]
    )

    fmt_str = '%H:%M:%S'
    new_df_floor['start_floor'] = new_df_floor['start_floor'].dt.strftime(fmt_str)
    new_df_floor['finish_floor'] = new_df_floor['finish_floor'].dt.strftime(fmt_str)
    new_df_deep['start_deep'] = new_df_deep['start_deep'].dt.strftime(fmt_str)
    new_df_deep['finish_deep'] = new_df_deep['finish_deep'].dt.strftime(fmt_str)

    df_new_to_use = pd.merge(new_df_floor, new_df_deep, how='outer')
    return df_new_to_use
#cleaning_times('2022-03-15', '2022-03-17')

def heat_map_func(date, thresh_1, thresh_2):
    """
    Takes in the dataframe created by AI engine with additional type and column changes and returns a dataframe containing records for given input date
    with 0-24 hour bucket where each row shows how many times the occupancy count went above the given threshold in that particular hour range.
    
    Args:
        df: Input dataframe
        date: date in string form (ex:-"2022-03-28")for which records have to be retrieved
        thresh: Threshold for occupancy
    Returns:
        op_df: Output Dataframe
    """
    data = dff_kar[dff_kar['date'] == pd.to_datetime(str(date))]
    data_m1 = data[data['Room No']=='M1 Separation Room']
    data_m2 = data[data['Room No']=='M2 Purification Room']
    try:
        last_hr_r1 = data_m1.iloc[-1]['Hour']
    except:
        last_hr_r1 = 0
    try:
        last_hr_r2 = data_m2.iloc[-1]['Hour']
    except:
        last_hr_r2 = 0
    last_hr = max(last_hr_r1, last_hr_r2)
    # print(last_hr)
    m1_thresh_val = []
    m2_thresh_val = []
    hour_index = []
    for hour in range(0,last_hr+1):
        hour_index.append(hour)
        data_m1_hour = data_m1[data_m1['Hour'] == hour]
        m1_thresh_count = 0
        for m1_occ in data_m1_hour['T_Occupancy']:
            if m1_occ > int(thresh_1):
                m1_thresh_count += 1
        m1_thresh_val.append(m1_thresh_count)
        data_m2_hour = data_m2[data_m2['Hour'] == hour]
        m2_thresh_count = 0
        for m2_occ in data_m2_hour['T_Occupancy']:
            if m2_occ > int(thresh_2):
                m2_thresh_count += 1
        m2_thresh_val.append(m2_thresh_count)
    dff = {'Hour':hour_index,'M1 Separation Room': m1_thresh_val,'M2 Purification Room': m2_thresh_val}
    op_df = pd.DataFrame(dff)
    m1 = op_df['M1 Separation Room'].to_list()
    m2 = op_df['M2 Purification Room'].to_list()
    return dict({'M1':m1, 'M2':m2})
#kar_df[(kar_df['date'] == pd.to_datetime(str('2022-03-23'))) & (kar_df['Room No'] == 'M1 Separation Room')]
#heat_map_func('2022-03-23',1, 0)

def create_dashboard_occ_heatmap(heat_map_data,save_path,**kwargs):

    ## y-axis - list of ylabels : M1 , M2
    ## x-axis - list of labels : [1-24]
    ## values - array of integers : [1,3,4,0,2] - people detected hourly.(order of data should be 1 to 24)

    ''' excepted data format

        heat_map_data = {"M1":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
                        "M2":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]}
        
        
    '''

    hm_y_labels = list(heat_map_data.keys())
    hm_x_labels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

    max_hours = len(list(heat_map_data.values())[0])
    hm_x_labels = hm_x_labels[:(max_hours)]

    hm_values = np.array(list(heat_map_data.values()))
    hm_new_value = hm_values

    fig, ax = plt.subplots(figsize=(10,2))
    # FIGURE size manupilation. dynamically

    im = ax.imshow(hm_new_value, **kwargs)
    #cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)

    ax.set_xticks(np.arange(len(hm_x_labels)), labels=hm_x_labels)
    ax.set_yticks(np.arange(len(hm_y_labels)), labels=hm_y_labels)
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(hm_y_labels)):
        for j in range(len(hm_x_labels)):
            text = ax.text(j, i, hm_new_value[i, j],
                        ha="center", va="center", color="b")

    ax.set_title("")
    #fig.tight_layout()
    fig_savename = os.path.join(save_path , "dash_occ_heatmap.png")
    fig.savefig(fig_savename)
    #image = Image.open(fig_savename)
    return fig
    #plt.show()