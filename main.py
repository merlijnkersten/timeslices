import os
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Import own packages from other script
from variables import GENERATION_PATH, LOAD_PATH, DIRECTORY, PRICE_PATH #,IMPORT_EXPORT_PATHS, PRICE_PATH
IMPORT_EXPORT_PATHS = [f"C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/cross border {year}.csv" for year in range(2015, 2022)]

import load
import assign
import analyse


load_generation_df = load.load_generation(LOAD_PATH, GENERATION_PATH)
import_export_df = load.cross_border_files(IMPORT_EXPORT_PATHS)
load_generation_import_export_df = pd.merge(load_generation_df, import_export_df, left_index=True, right_index=True )
price_df = load.prices(PRICE_PATH)
combined_df = pd.merge(load_generation_import_export_df, price_df, left_index=True, right_index=True)

combined_df['Season'] = assign.season(combined_df)
combined_df['Daynite'] = assign.daynite(combined_df, 'Date')
combined_df['Weekday'] = assign.weekday(combined_df)
combined_df['Season weekday'] = assign.combine_timeslices(combined_df, 'Season', 'Weekday')
combined_df['Daynite8'] = assign.daynite_8(combined_df)
combined_df['Month long'] = assign.month(combined_df)
combined_df['Hour long'] = assign.hour(combined_df)

#column_lst = ['Generation sum [MW]', 'Net import [MW]', 'Imports [MW]', 'Exports [MW]', 'Price [EUR/MWh]', 'Price [CZK/MWh]']
column_lst = ['Price [EUR/MWh]', 'Price [CZK/MWh]']

for column in column_lst:

    sub_directory = f"{DIRECTORY} Output {load.fmt(column)}/"
    if not os.path.exists(sub_directory):
        os.makedirs(sub_directory)

    #create_seasonal_load_duration_graph(combined_df, column, sub_directory)
    #create_daynite_load_duration_graph(combined_df, column, sub_directory)
    #get_all_statistics(combined_df, column, sub_directory)
    analyse.timeslice_analysis(combined_df, 'Season', 'Daynite', 'Load [MW]', sub_directory)
