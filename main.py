import pandas as pd
import itertools
import matplotlib.pyplot as plt
import time
import os

# Import own packages from other script
from analysis_functions import import_load_generation, import_cross_border_files, find_import_export, assign_seasons, assign_daynite, assign_ts, create_load_duration_graph, create_seasonal_load_duration_graph, create_daynite_load_duration_graph, get_statistics, get_all_statistics, generate_prices_csv, import_prices, fmt_col

load_path = r"C:/Users/czpkersten/Documents/timeslices/data/load 2015-2021.csv"
generation_path = r"C:/Users/czpkersten/Documents/timeslices/data/generation 2015-2021.csv"
import_export_paths = [f"C:/Users/czpkersten/Documents/timeslices/data/cross border {year}.csv" for year in range(2015, 2022)]
price_path = r"C:/Users/czpkersten/Documents/timeslices/data/prices 2015-2021.csv"
#price_paths = [f"C:/Users/czpkersten/Documents/timeslices/data/prices {year}.xls" for year in range(2015,2022)]

directory = r"C:/Users/czpkersten/Documents/timeslices-output/"

load_generation_df = import_load_generation(load_path, generation_path)

import_export_df = import_cross_border_files(import_export_paths)

load_generation_import_export_df = pd.merge(load_generation_df, import_export_df, left_index=True, right_index=True )

price_df = import_prices(price_path)

combined_df = pd.merge(load_generation_import_export_df, price_df, left_index=True, right_index=True)

combined_df['Season'] = assign_seasons(combined_df)

combined_df = assign_daynite(combined_df)

combined_df['TS'] = assign_ts(combined_df)

#column_lst = ['Generation sum [MW]', 'Net import [MW]', 'Imports [MW]', 'Exports [MW]', 'Price [EUR/MWh]', 'Price [CZK/MWh]']
column_lst = ['Price [EUR/MWh]', 'Price [CZK/MWh]']

for column in column_lst:

    sub_directory = f"{directory} Output {fmt_col(column)}/"
    if not os.path.exists(sub_directory):
        os.makedirs(sub_directory)

    create_seasonal_load_duration_graph(combined_df, column, sub_directory)
    create_daynite_load_duration_graph(combined_df, column, sub_directory)
    get_all_statistics(combined_df, column, sub_directory)