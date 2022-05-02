import pandas as pd
import itertools
import matplotlib.pyplot as plt
import numpy as np
import os

from variables import GENERATION_PATH, LOAD_PATH, DIRECTORY

"""
# Lists of seasonal timeslices
daynites = ['Night', 'Day', 'Peak']
#           [('Spring', 'Night'), ('Spring', 'Day'), ('Spring', 'Peak')]
spring_ts = [('Spring', i) for i in daynites]
summer_ts = [('Summer', i) for i in daynites]
autumn_ts = [('Autumn', i) for i in daynites]
winter_ts = [('Winter', i) for i in daynites]

# Lists of daynite timeslices
seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
#          [('Spring', 'Night'), ('Summer', 'Night'), ('Autumn', 'Night'), ('Winter', 'Night')]
night_ts = [(i, 'Night') for i in seasons]
day_ts = [(i, 'Day') for i in seasons]
peak_ts = [(i, 'Peak') for i in seasons]



# Full list of time slices
ts_lst = ['1. ZN', '1. ZP', '1. ZD', 
    '2. SN', '2. SP', '2. SD', 
    '3. FN', '3. FP', '3. FD',
    '4. WN', '4. WP', '4. WD']


# Translation dictionary from timeslice character to long name
ts_dct = {
    'N' : 'Night',
    'D' : 'Day',
    'P' : 'Peak',
    'Z' : 'Spring',
    'S' : 'Summer',
    'F' : 'Autumn',
    'W' : 'Winter'}
"""

def fmt(i):
    '''
    Reformat input.
    If string: reformats a column by removing unit information and setting it to lowercase.
    If numeric: rounds to two decimals.
    '''
    if type(i) == str:
        i = i.replace(' [MW]', '')
        i = i.replace(' [EUR/MWh]', '-euro')
        i = i.replace(' [CZK/MWh]', '-czk')
        return i.lower()
    elif type(i) in [float, np.float64]:
        return round(i, 2)
    else:
        raise Exception(f'Input type is not str or float but {type(i)}')


def zero_padded_hour(i):
    '''
    Hours in price data set range from 1-24, Datetime uses 00-23. 
    This function substracts one from the time, changes the type to
    string, and adds a leading zero if the hour is a single digit.
    '''
    j = str(i-1)
    if len(j) == 1:
        return ' 0' + j
    else:
        return ' '  + j


def load_generation(load_path, generation_path):
    '''
    import load and generation CSVs as polished Dataframes
    load_path: path to load data CSV
    generation_path: path to generation data CSV
    output: DataFrame containing load and generation data
    '''

    # Read load data
    load_df = pd.read_csv(load_path, sep=";", header=2)
    # Create a timestamp column based on "Date" and set this as the index
    load_df["Date and time"] = pd.to_datetime(load_df["Date"], format=r"%d.%m.%Y %H:%M")
    load_df.set_index("Date and time", inplace=True)
    # Remove unnecessary columns
    load_df.drop(columns=["Unnamed: 3", "Date"], inplace=True)

    # Read generation data
    generation_df = pd.read_csv(generation_path, sep=';', header=2)
    # Create a timestamp column based on "Date" and set this as the index    
    generation_df["Date and time"] = pd.to_datetime(generation_df["Date"], format=r"%d.%m.%Y %H:%M")
    generation_df.set_index("Date and time", inplace=True)
    # Remove unnecessary columns
    generation_df.drop(columns=["Unnamed: 10", "Date"], inplace=True)
    # Find total generation by summing generation of various technologies
    generation_df["Generation sum [MW]"] = generation_df.sum(axis=1)

    # Merge the generation and load dictionaries based on their shared index.
    combined_df = pd.merge(generation_df, load_df, left_index=True, right_index=True)
    # Create data, year, month, and hour columns
    combined_df["Date"] = combined_df.index.date
    combined_df["Year"] = combined_df.index.year
    combined_df["Month"] = combined_df.index.month
    combined_df["Hour"] = combined_df.index.hour

    # Find 'net' export (without taking losses into consideration)
    combined_df["Net export (generation - load) [MW]"] = combined_df["Generation sum [MW]"] - combined_df["Load including pumping [MW]"]

    return combined_df


def find_import_export(row, kind):
    '''
    determines hourly average import and export values. if there, on average, 
    no import or exports to any border crossing it returns zero (not None) export
    or import.
    row: row from the output of DataFrame of import_cross_border_files
    kind: 'import' or 'export'
    TODO how to restrict values in Python? e.g. kind = ['import', 'export']
    '''
    # border crossing columns
    columns = ['Poland [MW]','Slovakia [MW]', 'Austria [MW]', 'Germany (south) [MW]', 'Germany (north) [MW]']
    if kind == 'import':
        # Imports into CR are positive values. Find all values larger than zero
        transfers = [row[column] for column in columns if row[column] >= 0]
    elif kind == 'export':
        # Exports from CP are negative values. Find all values smaller than zero
        transfers = [row[column] for column in columns if row[column] <= 0]
    # The sum of the values in transfers is the total of the average export/import values
    return sum(transfers)

    # Using `sum()` will automatically return 0 if there are no imports/exports. Should this be None?
    # Alternative: 
    '''
    if sum(transfers) != 0:
        return sum(transfers)
    else:
        return None
    '''


def generate_cross_border_csv(lst):
    '''
    lst: list of paths
    loads CSVs and combines them into a single, polished file.
    '''

    # Empty list, to be populated with DataFrames for every year.
    dfs_lst = []

    # Translation dictionary from TSO names to their respective countries
    tso_dct = {
        'PSE Actual [MW]'   : 'Poland [MW]',
        'SEPS Actual [MW]'  : 'Slovakia [MW]',
        'APG Actual [MW]'   : 'Austria [MW]',
        'TenneT Actual [MW]': 'Germany (south) [MW]',
        '50HzT Actual [MW]' : 'Germany (north) [MW]',
        'CEPS Actual [MW]'  : 'Net import [MW]'
    }

    # Unecessary columns, will be removed later.
    redundant_columns = ['Unnamed: 13', 'Date', 'PSE Planned [MW]', 'SEPS Planned [MW]', 
        'APG Planned [MW]', 'TenneT Planned [MW]', '50HzT Planned [MW]','CEPS Planned [MW]']


    for path in lst:
        # Read cross border data
        df = pd.read_csv(path, skiprows=2, sep=';')
        # Create a timestamp column based on "Date" and set this as the index
        df["Date and time"] = pd.to_datetime(df["Date"], format=r"%d.%m.%Y %H:%M")
        df.set_index("Date and time", inplace=True)       
        # Drop unecessary columns
        df.drop(columns=redundant_columns, inplace=True)
        # Rename columns from TSO names to country names
        df.columns = [tso_dct[i] for i in list(df.columns)]
        # Append the Dataframe to the Datafraemes list
        dfs_lst.append(df)

    # Concatenate dataframes together
    df = pd.concat(dfs_lst)

    # Create import and export columns using the find_import_export function
    df['Imports [MW]'] = df.apply(lambda i: find_import_export(i, 'import'), axis=1)
    df['Exports [MW]'] = df.apply(lambda i: find_import_export(i, 'export'), axis=1)
    
    return df


def cross_border(cross_border_path):
    df = pd.read_csv(cross_border_path)
    df["Date and time"] = pd.to_datetime(df["Date and time"], format=r"%Y-%m-%d %H:%M:%S")
    df.set_index("Date and time", inplace=True)                             

    return df


def generate_price_csv(prices_paths, output_path):
    '''
    reads prices XLSs and returns a formatted, polished dataframe
    prices_paths: list of paths to annual prices XLS from 
    https://www.ote-cr.cz/en/short-term-markets/electricity/day-ahead-market
    and saves it as a CSV at output_path
    prices_paths: list of paths
    output_path: path to output CSV
    '''

    # Empty list, will be populated with Dataframes
    df_lst = []

    # For every path:
    for path in prices_paths:
        # Read 'DAM' (day-ahead) sheet 
        df = pd.read_excel(path, skiprows=5,  engine='xlrd', sheet_name='DAM')
        # Keep only the Day, Hour, Marginal price CZ (EUR/MWh), Marginal price CZ (CZK/MWH) columns
        df = df[['Day', 'Hour', 'Marginal price CZ (EUR/MWh)', 'Marginal price CZ (CZK/MWh)']]
        # During DST change, hour is set to 25. I remove this data point as I wasn't sure how to deal with it
        # Better alternative way? Effect on accuracy is likely small due to size of data set. 
        df = df[ df['Hour'] != 25 ]
        # Create a date and time column by cominbining the Day and Hour columns, setting it to datetime
        df['Date and time'] = df['Day'].dt.strftime(r'%Y-%m-%d') + df['Hour'].apply(zero_padded_hour)
        df['Date and time'] = pd.to_datetime(df['Date and time'], format=r'%Y-%m-%d %H')
        # Use this column as the index, and remove the now superfluous day and our columns
        df.set_index("Date and time", inplace=True)
        df.drop(columns=['Day', 'Hour'], inplace=True)
        # Rename the remaining price columns.
        df.columns = ['Price [EUR/MWh]', 'Price [CZK/MWh]']
        # Append the dataframe to the list of dataframes
        df_lst.append(df)
    
    # Concatenate the dataframes in the list together and save it.
    pd.concat(df_lst).to_csv(output_path)


def price(path):
    '''
    Function to import the file created in the create_prices_csv function
    Returns the CSV as a formatted Dataframe
    '''
    # Read file
    df = pd.read_csv(path)
    # Change Date and time column to a datetime column and set it as the index
    df['Date and time'] = pd.to_datetime(df['Date and time'], format=r'%Y-%m-%d %H', )
    df.set_index('Date and time', inplace=True)

    return df