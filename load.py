'''
Functions to load and combine data sets
'''

import itertools
from time import strptime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from datetime import datetime, date, time, timedelta, tzinfo
import pytz

def fmt(i):
    '''
    Reformat input.
    If string: reformats a column by removing unit information and setting it to lowercase.
    If numeric: rounds to two decimals.
    '''
    if type(i) == str:
        i = i.replace(' [MW]', '')
        i = i.replace(' [EUR/MWh]', '-eur')
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

"""
There are two ways to change time:

| Date time format | Normal day | WT to ST  | ST to WT  | Files from (columns)                   |
| ---------------- | ---------- | --------- | --------- | -------------------------------------- |
| 31-12-2015, 1    | 0-23       | 0-22      | 0-24      | OTE-ČR: prices, consumer load profiles |
| 31.12.2015 00:00 | 0-23       | 0-1, 3-23 | 0-2, 2-23 | ČEPS: cross border, load, generation   |
"""

def to_utc_ceps(i_lst, changeover_dates, st_to_wt):

    st_to_wt_set = set(st_to_wt)

    czech_tz = pytz.timezone('Europe/Prague')

    utc_datetime_lst = []

    for i in i_lst:
        date_time = datetime.strptime(i, r'%d.%m.%Y %H:%M')
        local_date = date_time.date()
  
        if local_date not in changeover_dates:
            # regular date; timezone is simply Czech/Prague time (CET/CEST) for whole day
            local_datetime =  czech_tz.localize(date_time)
            utc_datetime = local_datetime.astimezone(pytz.utc)
        elif local_date in st_to_wt:
            # Summer time to winter time
            # 02:00 |--> 03:00
            hour_local = date_time.hour
            if hour_local != 2:
                local_datetime =  czech_tz.localize(date_time)
                utc_datetime = local_datetime.astimezone(pytz.utc)
            elif local_date in st_to_wt_set:
                # first occurence of 02:00 >>> it is still summer time
                st_to_wt_set = st_to_wt_set - {local_date}
                offset = -2
                date_time = date_time + timedelta(hours=offset)
                utc_datetime =  pytz.utc.localize(date_time)
            else:
                # second occurence of 02:00 >>> it is winter time
                offset = -1
                date_time = date_time + timedelta(hours=offset)
                utc_datetime = pytz.utc.localize(date_time)
        else:
            # Winter time to summer time
            # 03:00 |--> 02:00
            local_datetime =  czech_tz.localize(date_time)
            utc_datetime = local_datetime.astimezone(pytz.utc)   
        
        utc_datetime_lst.append(utc_datetime)

    return utc_datetime_lst


def to_utc_otecr(i, changeover_dates, st_to_wt):
    czech_tz = pytz.timezone('Europe/Prague')

    try:
        date_time= datetime.strptime(i, r'%Y-%m-%d %H')

    except ValueError:
        # On the ST-to-WT day, hours run to 24 which breaks datetime
        local_hour = int(i[11:13])
        if local_hour == 24:
            local_date = datetime.strptime(i[:10], r'%Y-%m-%d').date()
            date_time = datetime.combine(local_date, time(22, 0))
            return pytz.utc.localize(date_time)
        else:
            raise ValueError(f'Unexpected value hour value: {i}')

    date_time= datetime.strptime(i, r'%Y-%m-%d %H')
    local_date = date_time.date()
    if local_date not in changeover_dates:
        # regular day
        local_datetime =  czech_tz.localize(date_time)
        return local_datetime.astimezone(pytz.utc)
    elif local_date in st_to_wt:
        # summer time to winter 
        offset = -2
        date_time = date_time + timedelta(hours=offset)
        return pytz.utc.localize(date_time)
    else:
        # winter time to summer 
        offset = -1
        date_time = date_time + timedelta(hours=offset)
        return pytz.utc.localize(date_time)


def to_utc(series, kind):
    wt_to_st_tup = [
        # winter time to summer time dates
        # (year, month, day)
        (2015, 3, 29),
        (2016, 3, 27),
        (2017, 3, 26),
        (2018, 3, 25),
        (2019, 3, 31),
        (2020, 3, 29),
        (2021, 3, 28),    
    ]
    st_to_wt_tup = [
        # summer time to winter time dates
        # (year, month, day)
        (2015, 10, 25),
        (2016, 10, 30),
        (2017, 10, 29),
        (2018, 10, 28),
        (2019, 10, 27),
        (2020, 10, 25),
        (2021, 10, 31)
    ]

    dates_lst = wt_to_st_tup + st_to_wt_tup
    changeover_dates = [date(i[0], i[1], i[2]) for i in dates_lst]
    st_to_wt = [date(i[0], i[1], i[2]) for i in st_to_wt_tup]
    
    if kind == 'otecr':
        return series.apply(lambda i: to_utc_otecr(i, changeover_dates, st_to_wt))
    elif kind == 'ceps':
        return to_utc_ceps(series, changeover_dates, st_to_wt)
    else:
        raise ValueError(f"Uknown kind: {kind} (not 'otecr' or 'ceps')")


def czech_time(i):
    czech_tz = pytz.timezone('Europe/Prague')
    return i.astimezone(czech_tz).replace(tzinfo=None)


def load_generation(load_path, generation_path):
    '''
    import load and generation CSVs as polished Dataframes
    load_path: path to load data CSV
    generation_path: path to generation data CSV
    output: DataFrame containing load and generation data
    '''

    # Read load data
    load_df = pd.read_csv(load_path, sep=";", header=2)

    load_df["Date and time [UTC]"] = to_utc(load_df['Date'], 'ceps')
    load_df.set_index("Date and time [UTC]", inplace=True)

    # Remove unnecessary columns
    load_df.drop(columns=["Unnamed: 3", "Date"], inplace=True)

    # Read generation data
    generation_df = pd.read_csv(generation_path, sep=';', header=2)

    generation_df["Date and time [UTC]"] = to_utc(generation_df['Date'], 'ceps')
    generation_df.set_index("Date and time [UTC]", inplace=True)
    # Remove unnecessary columns
    generation_df.drop(columns=["Unnamed: 10", "Date"], inplace=True)
    # Find total generation by summing generation of various technologies
    generation_df["Generation sum [MW]"] = generation_df.sum(axis=1)

    # Merge the generation and load dictionaries based on their shared index.
    combined_df = pd.merge(load_df, generation_df, left_index=True, right_index=True)
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
    col_dct = {
        # original : new
        'PSE Actual [MW]'   : 'Poland [MW]',
        'SEPS Actual [MW]'  : 'Slovakia [MW]',
        'APG Actual [MW]'   : 'Austria [MW]',
        'TenneT Actual [MW]': 'Germany (south) [MW]',
        '50HzT Actual [MW]' : 'Germany (north) [MW]',
        'CEPS Actual [MW]'  : 'Net import [MW]',
    }

    # Unecessary columns, will be removed later.
    redundant_columns = ['Unnamed: 13', 'Date', 'PSE Planned [MW]', 'SEPS Planned [MW]', 
        'APG Planned [MW]', 'TenneT Planned [MW]', '50HzT Planned [MW]','CEPS Planned [MW]']


    for path in lst:
        # Read cross border data
        df = pd.read_csv(path, skiprows=2, sep=';')
        # Create a timestamp column based on "Date" and set this as the index
        df["Date and time [UTC]"] = to_utc(df["Date"], "ceps")
        df.set_index("Date and time [UTC]", inplace=True)
        # Drop unecessary columns
        df.drop(columns=redundant_columns, inplace=True)
        # Rename columns from TSO names to country names
        df.columns = [col_dct[i] for i in list(df.columns)]
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
    df["Date and time [UTC]"] = pd.to_datetime(df["Date and time [UTC]"])
    df.set_index("Date and time [UTC]", inplace=True)                             

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
        df['Date and time [UTC]'] = to_utc(df['Date and time'], 'otecr')
        df.set_index("Date and time [UTC]", inplace=True)
        df.drop(columns=['Day', 'Hour', 'Date and time'], inplace=True)
        # Rename the remaining price columns.
        col_dct = {
            # original : new
            'Marginal price CZ (EUR/MWh)' : 'Price [EUR/MWh]',
            'Marginal price CZ (CZK/MWh)' : 'Price [CZK/MWh'
        }
        df.columns = [col_dct[i] for i in list(df.columns)]
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
    df["Date and time [UTC]"] = pd.to_datetime(df["Date and time [UTC]"])
    df.set_index("Date and time [UTC]", inplace=True)
    return df    


def generate_consumer_load_profile_csv(directory, output):
    files = [f'{directory}/consumer load profile {year}.xls' for year in range(2015,2022)]

    df_lst = []

    for file in files:
        '''
        columns = pd.read_excel(file, skiprows=4, nrows=1).columns

        type_dct = {
            "Day" : str,
            "Hour" : str,
            "Hour number in year" : int,
        }

        for column in columns:
            if column not in type_dct.keys():
                type_dct[column] = float
        '''

        df = pd.read_excel(file, skiprows=4)
        df = df[df['Day'].notna()]
        df['Hour_temp'] = df['Hour'].astype(int).apply(zero_padded_hour) 
        df['Date and time'] = df[['Day', 'Hour_temp']].astype(str).agg(''.join, axis=1)
        df['Date and time [UTC]'] = to_utc(df['Date and time'], 'otecr')
        df.columns = [col.replace('\n','') for col in df.columns]
        df.drop(['Hour_temp','Date and time', 'Day', 'Hour', 'Hour number in year'], inplace=True, axis=1)
        df.set_index('Date and time [UTC]', inplace=True)
        df_lst.append(df)


    pd.concat(df_lst).to_csv(output)

def consumer_load_profile(path):
    df = pd.read_csv(path)
    df["Date and time [UTC]"] = pd.to_datetime(df["Date and time [UTC]"])
    df.set_index("Date and time [UTC]", inplace=True)   
    return df 


def polish(df):
    df.reset_index(inplace=True)
    df['Date and time [CZ]'] = df['Date and time [UTC]'].apply(czech_time)
    df.set_index('Date and time [UTC]', inplace=True)
    df["Date"] = df['Date and time [CZ]'].dt.date
    df["Year"] = df['Date and time [CZ]'].dt.year
    df["Month"] = df['Date and time [CZ]'].dt.month
    df["Hour"] = df['Date and time [CZ]'].dt.hour
    return df

def merge(df_lst):
    df = df_lst[0]
    rest = df_lst[1:]
    for next_df in rest:
        df = pd.merge(df, next_df, left_index=True, right_index=True)
    
    return polish(df)