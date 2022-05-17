import os
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Import own packages from other script
import load
import assign
import analyse

cwd = os.getcwd()
data_path = os.path.join(cwd, 'data')
LOAD_PATH = os.path.join(data_path, 'load 2015-2021.csv')
GENERATION_PATH = os.path.join(data_path, 'generation 2015-2021.csv')
PRICE_PATH = os.path.join(data_path, 'prices 2015-2021.csv')
CROSS_BORDER_PATH = os.path.join(data_path, 'cross border 2015-2021.csv')
DIRECTORY =  os.path.join(os.path.dirname(cwd), 'timeslices-output')

load_generation_df = load.load_generation(LOAD_PATH, GENERATION_PATH)
price_df = load.price(PRICE_PATH)
load_generation_price_df = pd.merge(load_generation_df, price_df, left_index=True, right_index=True)
cross_border_df = load.cross_border(CROSS_BORDER_PATH)
combined_df = pd.merge(load_generation_price_df, cross_border_df, left_index=True, right_index=True)

combined_df['Season'] = assign.season(combined_df)
combined_df['Daynite'] = assign.daynite(combined_df, 'Date')
combined_df['Weekday'] = assign.weekday(combined_df)
combined_df['Season weekday'] = assign.combine_timeslices(combined_df, 'Season', 'Weekday')
combined_df['Daynite8'] = assign.daynite_8(combined_df)
combined_df['Month long'] = assign.month(combined_df)
combined_df['Hour long'] = assign.hour(combined_df)
combined_df['Daynite4'] = assign.daynite_4(combined_df)
combined_df['Weekday alt'] = assign.weekday_alt(combined_df)
combined_df['Season weekday alt'] = assign.combine_timeslices(combined_df, 'Season', 'Weekday alt')

combined_df['Season weekday daynite'] = assign.combine_timeslices(combined_df, 'Season weekday', 'Daynite')
combined_df['Season daynite'] = assign.combine_timeslices(combined_df, 'Season', 'Daynite')


PATH = "C:/Users/czpkersten/Documents/timeslices/data/combined 2015-2021.csv"
combined_df.to_csv(PATH)

#column_lst = ['Generation sum [MW]', 'Net import [MW]', 'Imports [MW]', 'Exports [MW]', 'Price [EUR/MWh]', 'Price [CZK/MWh]']
column_lst = ['Load [MW]', 'Imports [MW]', 'Exports [MW]', 'Price [CZK/MWh]', 'Price [EUR/MWh]']

for column in column_lst:

    sub_directory = os.path.join(DIRECTORY, f"Output {load.fmt(column)}")
    if not os.path.exists(sub_directory):
        os.makedirs(sub_directory)
    #create_seasonal_load_duration_graph(combined_df, column, sub_directory)
    #create_daynite_load_duration_graph(combined_df, column, sub_directory)
    #get_all_statistics(combined_df, column, sub_directory)

    #analyse.timeslice_analysis(combined_df, 'Season', 'Daynite', column, sub_directory)
    #analyse.timeslice_analysis(combined_df, 'Season', 'Daynite8', column, sub_directory)
    #analyse.timeslice_analysis(combined_df, 'Season', 'Hour long', column, sub_directory)
    analyse.timeslice_analysis(combined_df, 'Season weekday', 'Daynite', column, sub_directory)
    #analyse.timeslice_analysis(combined_df, 'Month long', 'Daynite', column, sub_directory)
    #analyse.timeslice_analysis(combined_df, 'Month long', 'Daynite8', column, sub_directory)
    #analyse.timeslice_analysis(combined_df, 'Month long', 'Weekday', column, sub_directory)
    #analyse.timeslice_analysis(combined_df, 'Season', 'Daynite4', column, sub_directory)
    #analyse.timeslice_analysis(combined_df, 'Season', 'Weekday alt', column, sub_directory)
    #analyse.timeslice_analysis(combined_df, 'Season weekday alt', 'Daynite', column, sub_directory)

