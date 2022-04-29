from time import strftime
import pandas as pd
import datetime as dt
import numpy as np
import itertools
import matplotlib.pyplot as plt
import os


from variables import GENERATION_PATH, LOAD_PATH, DIRECTORY

def assign_weekday_weekend(df):
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
        public_holidays.extend([dt.date(year, d[0], d[1]) for year in years])

    easter_dates = [
        (2016, 3, 25), # Good Friday (from 2016)
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
    public_holidays.extend([dt.date(d[0], d[1], d[2]) for d in easter_dates])

    day_dct = {}

    for day in pd.date_range(start='2015/01/01', end='2021/12/31'):
        if day in public_holidays:
            day_dct[day] = 'Weekend'
        elif day.weekday() in [5, 6]:
            # Saturday == 5, Sunday == 6
            day_dct[day] = 'Weekend'
        else:
            # It must be a weekday
            day_dct[day] = 'Weekday'
    
    df['Weekday weekend'] =  df['Date'].map(day_dct)
    #df['Season weekday-weekend'] = df['Season'] + df['Weekday weekend'].lower()
    return df['Weekday weekend'] #, df['Season weekday-weekend]

# set month/hour through df.index.month / .hour eazy


def assign_daynite_8(df):
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
    # {k+8 : f'D{(k // 2) + 1}' for k in range(0,12)}
    # {k : 'N2' for k in range(0,8)}
    # {k : 'N1' for k in range(20,25)}
    return df['Hour'].map(hour_dct)
    #(return)

    # Could do something similar for monts M1, M2, etc

def assign_hour(df):
    def zero_pad(i):
        if len(str(i)) == 1:
            return '0' + str(i)
        else:
            return str(i)
    
    hour_dct = {
        k : f'H{zero_pad(k)}' for k in range(0,24)
    }

    return df['Hour'].map(hour_dct)

def assign_month(df):
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
    return df['Month'].map(month_dct)

def combine_timeslices(df, col_1, col_2):
    return df[[col_1, col_2]].agg(' '.join, axis=1)

'''
Issue: Timeslice is no longer 'XY' 

Solution 1: Come up with other X and Y codes to keep the system consistent

Solution 2: Save timeslices as tuple/'string tuple'

Solution 3: Always use two columns to 'make' timeslices?
'''

def import_load_generation(load_path, generation_path):
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

def assign_seasons(df):
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

def assign_daynite(df, column):
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
    
    indices_sum = len(night_ids) + len(peak_ids) + len(day_ids)
    test = indices_sum == df.shape[0]
    if not test:
        raise Exception(f'DataFrame and Night/Peak/Day index arrays do not have same length: {df.shape[0]} vs {indices_sum}')         
    
    return df.index.map(daynite_dct)


def fmt(i):
    '''
    Reformats a column by removing unit information and setting it to lowercase.
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

df = import_load_generation(LOAD_PATH, GENERATION_PATH)

df['Weekday'] = assign_weekday_weekend(df)

df['Daynite8'] = assign_daynite_8(df)

df['Month_long'] = assign_month(df)

df['Hour_long'] = assign_hour(df)

df['Season'] = assign_seasons(df)

df['Daynite SEASON'] = assign_daynite(df, 'Season')

df['Daynite MONTH'] = assign_daynite(df, 'Month')

df['Daynite WEEKDAY'] = assign_daynite(df, 'Weekday')

df['Daynite DAY'] = assign_daynite(df, 'Date')

df['Season weekday'] = combine_timeslices(df, 'Season', 'Weekday')


##### MONDAY 25 APRIL #####

def create_load_duration_graph(df, ts_lst, column_a, column_b, plot_column, axs, variable):
    '''
    df: dataframe with plotting data,
    ts_list: list of timeslices to plot,
    column: which dataframe column to plot,
    ttl: title of plot,
    axs: matplotlib.pyplot axis

    a: longer time period (season, weekday, month), sets colour
    b: shorter time period (daynite, hour), sets linestyle
    '''

    linestyle_dct = {
        'Night' : 'solid',
        'Day' : 'dashed',
        'Peak' : 'dotted',

        'Night-1' : '-',  # solid
        'Night-2' : '--', # dashed
        'Day-1' : 'o',    # circle
        'Day-2' : 'v',    # triangle
        'Day-3' : 's',    # square
        'Day-4' : 'd',    # diamond
        'Day-5' : '+',    # plus
        'Day-6' : 'x',    # x

        'Spring' : 'solid',
        'Summer' : 'dashed',
        'Autumn' : 'dotted',
        'Winter' : 'dashdot'
    }

    colour_dct = {
        'Spring' : 'limegreen',
        'Summer' : 'gold',
        'Autumn' : 'orangered',
        'Winter' : 'cornflowerblue',

        'Spring Weekday' : '#33a02c', 
        'Spring Weekend' : '#b2df8a',
        'Summer Weekday' : '#ff7f00',
        'Summer Weekend' : '#fdbf6f',
        'Autumn Weekday' : '#e31a1c',
        'Autumn Weekend' : '#fb9a99',
        'Winter Weekday' : '#1f78b4',
        'Winter Weekend' : '#a6cee3',

        'January' : '#1f78b4', 
        'February' : '#cab2d6',
        'March' : '#a6cee3',
        'April' : '#31a1c',
        'May' : '#b2df8ae',
        'June' : '#b15928',
        'July' : '#ff7f00',
        'August' : '#33a02c',
        'September' : '#fb9a99',
        'October' : '#ffff99',
        'November' : '#fdbf6f',
        'December' : '#6a3d9a',

        'Night-1' : '#1f77b4', 
        'Night-2' : '#ff7f0e', 
        'Day-1' : '#2ca02c', 
        'Day-2' : '#d62728', 
        'Day-3' : '#9467bd', 
        'Day-4' : '#e377c2', 
        'Day-5' : '#bcbd22', 
        'Day-6' : '#17becf'
    }

    for ts in ts_lst:
        value_a = ts[0]
        value_b = ts[1]

        if variable == 'a':
            title_text, label_text = value_b, value_a
        else:
            title_text, label_text = value_a, value_b
        
        mask = (df[column_a] == value_a) & (df[column_b] == value_b)
        data = df[mask][plot_column].sort_values(ascending=False)
        y = np.linspace(0, 1, len(data))
        axs.plot(y, data, label=label_text, c=colour_dct[value_a], ls=linestyle_dct[value_b])

    axs.legend()
    axs.set_title(title_text)
    axs.set_xlabel('Annual percentage')


def get_statistics(df, ts_lst, column_a, column_b, statistics_column):
    
    for ts in ts_lst:
        value_a = ts[0]
        value_b = ts[1]

        mask = (df[column_a] == value_a) & (df[column_b] == value_b)
        data = df[mask][statistics_column]

        dct = {
            'Column' : statistics_column.lower(),
            'Timeslice' : f'{value_a.lower()} {value_b.lower()}',
            'Mean' : fmt(data.mean()),
            'Standard deviation' : fmt(data.std()),
            'Minimum' : fmt(data.min()),
            '10% percentile' : fmt(data.quantile(0.1)),
            'Median' : fmt(data.median()),
            '90% percentile' : fmt(data.quantile(0.9)),
            'Maximum' : fmt(data.max())
        }
    
    return dct


def seasonal_weekday_daynite_analysis(df, column, directory):

    statistics = []

    seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    weekday = ['Weekend', 'Weekday']
    daynite = ['Night', 'Peak', 'Day']

    a = [' '.join(i) for i in itertools.product(seasons, weekday)]
    b = daynite
    #[('Spring weekday', 'Night'), (...), ...]

    fig, axs = plt.subplots(2, 4, sharey=True, figsize=(10,5))
    i = 0

    for season_weekday in a:
        ts = list(itertools.product([season_weekday], b))
        create_load_duration_graph(df, ts, 'Season weekday', 'Daynite', column, axs[i%2, i//2], 'b')

        statistics.append(get_statistics(df, ts, 'Season weekday', 'Daynite', column))

        i += 1

    axs[0,0].set_ylabel(column)
    axs[1,0].set_ylabel(column)

    plt.tight_layout()

    sub_directory = f"{directory}Output {fmt(column)}/"
    if not os.path.exists(sub_directory):
        os.makedirs(sub_directory)

    fig_path = f'{sub_directory}Load duration curve {fmt(column)} seasons weekdays.png'
    plt.savefig(fig_path, dpi=300, format='png')

    csv_path = f'{sub_directory}Statistics {fmt(column)} seasons weekdays.csv'
    pd.DataFrame(statistics).to_csv(csv_path, index=False)

    plt.show()


def seasonal_daynite8_analysis(df, column, directory):

    statistics = []

    seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    daynite8 = ['Night-1', 'Night-2', 'Day-1', 'Day-2', 'Day-3', 'Day-4', 'Day-5', 'Day-6']
    #weekday = ['Weekend', 'Weekday']
    #daynite = ['Night', 'Peak', 'Day']

    b = seasons
    a = daynite8
    #[('Spring weekday', 'Night'), (...), ...]

    fig, axs = plt.subplots(2, 4, sharey=True, figsize=(10,5))
    i = 0

    for dn8 in a:
        ts = list(itertools.product([dn8], b))
        create_load_duration_graph(df, ts, 'Daynite8', 'Season', column, axs[i%2, i//2], 'b')

        statistics.append(get_statistics(df, ts, 'Season', 'Daynite8', column))

        i += 1

    axs[0,0].set_ylabel(column)
    axs[1,0].set_ylabel(column)
    
    plt.tight_layout()

    sub_directory = f"{directory}Output {fmt(column)}/"
    if not os.path.exists(sub_directory):
        os.makedirs(sub_directory)

    fig_path = f'{sub_directory}Load duration curve {fmt(column)} seasons weekdays.png'
    plt.savefig(fig_path, dpi=300, format='png')

    csv_path = f'{sub_directory}Statistics {fmt(column)} seasons weekdays.csv'
    pd.DataFrame(statistics).to_csv(csv_path, index=False)

    plt.show()

def monthly_daynite8_analysis(df, column, directory):

    statistics = []

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    daynite8 = ['Night-1', 'Night-2', 'Day-1', 'Day-2', 'Day-3', 'Day-4', 'Day-5', 'Day-6']

    b = months
    a = daynite8

    for dn8 in a:
        ts = list(itertools.product([dn8], b))
        statistics.append(get_statistics(df, ts, 'Season', 'Daynite8', column))

    sub_directory = f"{directory}Output {fmt(column)}/"
    if not os.path.exists(sub_directory):
        os.makedirs(sub_directory)

    csv_path = f'{sub_directory}Statistics {fmt(column)} seasons weekdays.csv'

def timeslice_analysis(df, column_a, column_b, statistics_column, directory):

    statistics = []

    values_a = list(df[column_a].unique())
    values_b = list(df[column_b].unique())

    for value in values_a:
        ts = list(itertools.product([value], values_b))
        statistics.append(get_statistics(df, ts, column_a, column_b, statistics_column))

    sub_directory = f"{directory}Output {fmt(statistics_column)}/"
    if not os.path.exists(sub_directory):
        os.makedirs(sub_directory)

    csv_path = f'{sub_directory}Statistics {fmt(statistics_column)} {fmt(column_a)} {fmt(column_b)}.csv'
    pd.DataFrame(statistics).to_csv(csv_path, index=False)


seasonal_weekday_daynite_analysis(df, "Generation sum [MW]", DIRECTORY)

seasonal_daynite8_analysis(df, "Generation sum [MW]", DIRECTORY)

timeslice_analysis(df, 'Month', '', 'Load [MW]', DIRECTORY)
timeslice_analysis(df, 'Month', 'Hour', 'Load [MW]', DIRECTORY)
timeslice_analysis(df, 'Month', 'Weekday', 'Load [MW]', DIRECTORY)