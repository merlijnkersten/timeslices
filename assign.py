'''
Functions to assign timeslices to the time series.
Most functions return the timeslices as a Pandas series.
'''

import itertools
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from load import fmt 

def season(df):
    '''
    Assign the correct (Czech) season to every day by creating a look-up 
    dictionary for every date in the dataset, and then matching the dates
    to the correct season. This method is slightly convuleted, but is much
    faster than creating a function that assigns the correct season to a 
    given date 
    df: Dataframe with 'Date' column (in datetime format) 
    returns: Seasons PD series
    '''

    # Empty look-up dictionary, to be populated with 'dates':'season'
    dates_to_season = dict()

    # Years in the data set. Could also retrieve these?
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
    #years = list(df['Year'].unique())

    seasons = [
        # First date of the season (/mm/dd)
        #        |            Last date of the season (/mm/dd )
        #        |                 |            Name of the season 
        {'start' : '/01/01', 'end' : '/03/14', 'season' : 'Winter'},
        {'start' : '/03/15', 'end' : '/05/31', 'season' : 'Spring'},
        {'start' : '/06/01', 'end' : '/08/30', 'season' : 'Summer'},
        {'start' : '/08/31', 'end' : '/11/15', 'season' : 'Autumn'},
        {'start' : '/11/16', 'end' : '/12/31', 'season' : 'Winter'}
    ]

    # For every combination of years and seasons
    for prod in itertools.product(years, seasons):
        # Retrieve year, season start/end date and name from product
        year = prod[0]
        start_date = prod[1]['start']
        end_date = prod[1]['end']
        season = prod[1]['season']

        # For every date in this season and year, add the date with the season to the look-up dictionary.
        for date in pd.date_range(start=f"{year}{start_date}", end=f"{year+1}{end_date}"):
            date_fmt = str(date)[0:10] #Or, format as "%Y-%m-%d"
            dates_to_season[date_fmt] = season

    # Map dates to season and return this series.
    return df['Date'].astype(str).map(dates_to_season)


def daynite(df, column):
    '''
    Divides data, for every season, into night (between 20:00-08:00, 12h), peak (highest load, 2h) and day (rest, 10h)
    df: Dataframe with 'Hour', 'Season', 'Load [MW]' columns.
    returns: timeslice series
    '''
    mask = (df['Hour'] < 8) | (df['Hour'] >= 20)
    night_ids = list(df[mask].index)

    daypeak_df = df[~mask].reset_index()
    peak_ids = []
    for index, sub_df in daypeak_df.groupby(by=[column]):
        percentile = 1/12
        length = sub_df.shape[0]
        n = round(length * percentile)
        peaks = list(sub_df.nlargest(n, 'Load [MW]')['Date and time'])
        peak_ids.extend(peaks)
      
    day_ids = set(daypeak_df['Date and time']) - set(peak_ids)

    daynite_dct = dict()
    for index in night_ids:
        daynite_dct[index] = 'Night'

    for index in peak_ids: 
        daynite_dct[index] = 'Peak'
    
    for index in day_ids:
        daynite_dct[index] = 'Day'
    
    # Need to do it this week due to daylight saving changing oddities in night_ids (better: len(daynite_dct))
    indices_sum = len(night_ids) + len(peak_ids) + len(day_ids)
    test = indices_sum == df.shape[0]
    if not test:
        raise Exception(f'DataFrame and Night/Peak/Day index arrays do not have same length: {df.shape[0]} vs {indices_sum}')         
    
    return df.index.map(daynite_dct)


def weekday_1(df):
    years = range(2015, 2022)
    holidays = [
        (1,1),  # New Years
        (5,1),  # Labour Day
        (5,8),  # Liberation from Fascism
        (6,5),  # Cyril and Methodius
        (7, 6),  # Burning at Stake of Jan Hus
        (9, 28), # Czech statehood day
        (10, 28), # Establishment of Czechslovak Republic
        (11, 17), # Freedom and democracy day
        (12, 24), # Christmas Eve
        (12, 25), # Christmas day
        (12, 26) # Chirstmas day
        # Plus Good Friday and Easter Monday: deal with seperately.
    ]
    
    public_holidays = []
    for d in holidays:
        # For every date in holidays, add that date to the public holidays list for every year 2015-2021.
        public_holidays.extend([pd.Timestamp(year, d[0], d[1]) for year in years])

    easter_dates = [
        (2016, 3, 25), # Good Friday (public holiday since 2016)
        (2017, 4, 14),
        (2018, 3, 30),
        (2019, 4, 19),
        (2020, 4, 10),
        (2021, 4, 2),
        (2015, 4, 6), # Easter Monday 
        (2015, 3, 28),
        (2017, 4, 17),
        (2018, 4, 12),
        (2019, 4, 22),
        (2020, 4, 13),
        (2021, 4, 5)
    ]
    public_holidays.extend([pd.Timestamp(d[0], d[1], d[2]) for d in easter_dates])

    day_dct = {}

    for day in pd.date_range(start='2015/01/01', end='2021/12/31'):
        if day in public_holidays:
            # Results in future warning: what to do about this?
            day_dct[day] = 'Weekend'
        elif day.weekday() in [5, 6]:
            # Saturday == 5, Sunday == 6
            day_dct[day] = 'Weekend'
        else:
            # It must be a weekday
            day_dct[day] = 'Working day'
    
    return df['Date'].map(day_dct)

def weekday_2(df):
    day_dct = {
        0 : 'Monday',
        1 : 'Tuesday',
        2 : 'Wednesday',
        3 : 'Thursday',
        4 : 'Friday',
        5 : 'Saturday',
        6 : 'Sunday'
    }
    return df.index.weekday.map(day_dct)


def daynite_8(df):
    hour_dct = {
        0 : 'Night-1', 
        1 : 'Night-1', 
        2 : 'Night-2', 
        3 : 'Night-2', 
        4 : 'Night-2', 
        5 : 'Night-2', 
        6 : 'Night-2',
        7 : 'Night-2',
        8 : 'Day-1', 
        9 : 'Day-1', 
        10 : 'Day-2', 
        11 : 'Day-2', 
        12 : 'Day-3', 
        13 : 'Day-3', 
        14 : 'Day-4', 
        15 : 'Day-4', 
        16 : 'Day-5', 
        17 : 'Day-5', 
        18 : 'Day-6', 
        19 : 'Day-6',
        20 : 'Night-1', 
        21 : 'Night-1', 
        22 : 'Night-1', 
        23 : 'Night-1'
    }
    # To generate dictionary:
    # {k+8 : f'D{(k // 2) + 1}' for k in range(0,12)}
    # {k : 'N2' for k in range(0,8)}
    # {k : 'N1' for k in range(20,25)}
    return df['Hour'].map(hour_dct)
    #(return)

    # Could do something similar for monts M1, M2, etc


def daynite_4(df):
    hour_dct = {
        0 : 'Night', 
        1 : 'Night', 
        2 : 'Night', 
        3 : 'Night', 
        4 : 'Night', 
        5 : 'Night', 
        6 : 'Morning',
        7 : 'Morning',
        8 : 'Morning', 
        9 : 'Morning', 
        10 : 'Afternoon', 
        11 : 'Afternoon', 
        12 : 'Afternoon', 
        13 : 'Afternoon', 
        14 : 'Afternoon', 
        15 : 'Afternoon', 
        16 : 'Evening', 
        17 : 'Evening', 
        18 : 'Evening', 
        19 : 'Evening',
        20 : 'Night', 
        21 : 'Night', 
        22 : 'Night', 
        23 : 'Night'
    }
    return df['Hour'].map(hour_dct)

def hour(df):
    def zero_pad(i):
        if len(str(i)) == 1:
            return '0' + str(i)
        else:
            return str(i)
    
    hour_dct = {
        k : f'H{zero_pad(k)}' for k in range(0,24)
    }

    return df['Hour'].map(hour_dct)


def month(df):
    month_dct = {
        1 : 'January',
        2 : 'February',
        3 : 'March',
        4 : 'April',
        5 : 'May',
        6 : 'June',
        7 : 'July',
        8 : 'August',
        9 : 'September',
        10 : 'October',
        11 : 'November',
        12 : 'December'
    }
    # Could also do this with datetime or calendar package (but this was easier)
    return df['Month'].map(month_dct)


def combine_timeslices(df, col_1, col_2):
    '''
    Combine the two timeslices in col_1 and col_2 into a single column, which is returned.
    '''
    return df[[col_1, col_2]].agg(' '.join, axis=1)
