from time import strftime
import pandas as pd
import datetime as dt
import numpy as np

def set_weekday_weekend(df):
    public_holidays = [
        #TODO create list of Czech public holidays
    ]
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


def set_daynite_8(df):
    hour_dct = {
        0 : 'N1', 
        1 : 'N1', 
        2 : 'N2', 
        3 : 'N2', 
        4 : 'N2', 
        5 : 'N2', 
        6 : 'N2',
        7 : 'N2',
        8 : 'D1', 
        9 : 'D1', 
        10 : 'D2', 
        11 : 'D2', 
        12 : 'D3', 
        13 : 'D3', 
        14 : 'D4', 
        15 : 'D4', 
        16 : 'D5', 
        17 : 'D5', 
        18 : 'D6', 
        19 : 'D6',
        20 : 'N1', 
        21 : 'N1', 
        22 : 'N1', 
        23 : 'N1'
    }
    # {k+8 : f'D{(k // 2) + 1}' for k in range(0,12)}
    # {k : 'N2' for k in range(0,8)}
    # {k : 'N1' for k in range(20,25)}
    return df['Hour'].map(hour_dct)
    #(return)

    # Could do something similar for monts M1, M2, etc

def set_hour(df):
    def zero_pad(i):
        if len(str(i)) == 1:
            return '0' + str(i)
        else:
            return str(i)
    
    hour_dct = {
        k : f'H{zero_pad(k)}' for k in range(0,24)
    }

    return df['Hour'].map(hour_dct)

def set_month(df):
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
    return df[[col_1, col_2]].agg('-'.join, axis=1)


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

load_path = r"C:/Users/Merlijn Kersten/Documents/Univerzita Karlova/Timeslice analysis/timeslice_analysis/data/load 2015-2021.csv"
generation_path = r"C:/Users/Merlijn Kersten/Documents/Univerzita Karlova/Timeslice analysis/timeslice_analysis/data/generation 2015-2021.csv"

df = import_load_generation(load_path, generation_path)

print(df.head())

df['Weekday-weekend'] = set_weekday_weekend(df)

print(df['Weekday-weekend'])

df['Daynite8'] = set_daynite_8(df)

print(df['Daynite8'])

print(df['Month'])#.dt.strftime('%B'))


##### MONDAY 25 APRIL #####

def create_load_duration_graph(df, ts_lst, column_a, column_b, plot_column, title, axs):
    '''
    df: dataframe with plotting data,
    ts_list: list of timeslices to plot,
    column: which dataframe column to plot,
    ttl: title of plot,
    axs: matplotlib.pyplot axis
    '''

    linestyle_dct = {
        'Night' : 'solid',
        'Day' : 'dashed',
        'Peak' : 'dotted'
    }

    colour_dct = {
        'Spring' : 'limegreen',
        'Summer' : 'gold',
        'Autumn' : 'orangered',
        'Winter' : 'cornflowerblue'
    }

    for ts in ts_lst:
        value_a = ts[0]
        value_b = ts[1]
        label_text = f'{value_a}, {value_b}'
        mask = (df[column_a] == value_a) & (df[column_b] == value_b)
        data = df[mask][plot_column].sort_values(ascending=False)
        y = np.linspace(0, 1, len(data))
        axs.plot(y, data, label=label_text, c=colour_dct[value_a], ls=linestyle_dct[value_b])
    
    axs.legend()
    axs.set_title(title)
    axs.set_xlabel('Annual percentage')


