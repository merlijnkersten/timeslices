'''
Run script
'''

import itertools
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.fft import fft
import seaborn as sns

# Import own packages from other script
import load
import assign
import analyse

# Set path variables. 
# You need to create a timeslices-output folder in the root folder prior to running script.
cwd = os.getcwd()
data_path = os.path.join(cwd, 'data')
LOAD_PATH = os.path.join(data_path, 'load 2015-2021.csv')
GENERATION_PATH = os.path.join(data_path, 'generation 2015-2021.csv')
PRICE_PATH = os.path.join(data_path, 'prices 2015-2021.csv')
CROSS_BORDER_PATH = os.path.join(data_path, 'cross border 2015-2021.csv')
DIRECTORY =  os.path.join(os.path.dirname(cwd), 'timeslices-output')

# Load data sets
load_generation_df = load.load_generation(LOAD_PATH, GENERATION_PATH)
price_df = load.price(PRICE_PATH)
load_generation_price_df = pd.merge(load_generation_df, price_df, left_index=True, right_index=True)
cross_border_df = load.cross_border(CROSS_BORDER_PATH)
combined_df = pd.merge(load_generation_price_df, cross_border_df, left_index=True, right_index=True)

# Assign (and combine) various timeslices to the time series
combined_df['Season'] = assign.season(combined_df)
combined_df['Daynite'] = assign.daynite(combined_df, 'Date')
combined_df['Weekday 1'] = assign.weekday(combined_df)
combined_df['Daynite8'] = assign.daynite_8(combined_df)
combined_df['Month long'] = assign.month(combined_df)
combined_df['Hour long'] = assign.hour(combined_df)
combined_df['Daynite4'] = assign.daynite_4(combined_df)
combined_df['Weekday 2'] = assign.weekday_alt(combined_df)

combined_df['Season weekday 1'] = assign.combine_timeslices(combined_df, 'Season', 'Weekday 1')
combined_df['Season weekday 2'] = assign.combine_timeslices(combined_df, 'Season', 'Weekday 2')
combined_df['Season weekday 1 daynite'] = assign.combine_timeslices(combined_df, 'Season weekday 1', 'Daynite')
combined_df['Season daynite'] = assign.combine_timeslices(combined_df, 'Season', 'Daynite')

# Optional: save combined data file with timeslices
#PATH = os.path.join(data_path, 'combined 2015-2021.csv')
#combined_df.to_csv(PATH)

# Run various analysis scripts

# Generate statistics reports for selected columns:
column_lst = ['Load [MW]', 'Imports [MW]', 'Exports [MW]', 'Price [CZK/MWh]', 'Price [EUR/MWh]']

for column in column_lst:

    sub_directory = os.path.join(DIRECTORY, f"Output {load.fmt(column)}")
    if not os.path.exists(sub_directory):
        os.makedirs(sub_directory)
    analyse.timeslice_analysis(combined_df, 'Season weekday 1', 'Daynite', column, sub_directory)

# Create distribution visualisation
sub_directory = os.path.join(DIRECTORY, "Distribution graphs")
if not os.path.exists(sub_directory):
    os.makedirs(sub_directory)
analyse.plot_distribution(sub_directory)

# Perform FFT for selected columns
columns = ['Load [MW]', 'Imports [MW]', 'Exports [MW]', 'Price [CZK/MWh]']

sub_directory = os.path.join(DIRECTORY, "FFT")
if not os.path.exists(sub_directory):
    os.makedirs(sub_directory)

for column in columns:
    input = os.path.join(data_path, "combined 2015-2021.csv")
    output = os.path.join(sub_directory, f"{load.fmt(column)} fft.csv")
    analyse.perform_fft(input, output, column)

# Create FFT visualisation (for all files in directory)
analyse.fft_visualisation(sub_directory)
