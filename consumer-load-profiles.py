import pandas as pd
import numpy as np
from scipy.fft import fft

from load import zero_padded_hour

#from analyse import perform_fft

def create_consumer_load_profile_file(directory, output):
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
        print(file)
        df = pd.read_excel(file, skiprows=4)
        df = df[df['Day'].notna()]
        df['Hour_temp'] = df['Hour'].apply(zero_padded_hour)
        #df[['Day', 'Hour']] = df[['Day', 'Hour']].astype(str)
        #df['Hour'] = df['Hour'].apply(zero_padded_hour)
        #df[['Day', 'Hour']] = df[['Day','Hour']].astype(str) 
        df['Date and time'] = df[['Day', 'Hour_temp']].astype(str).agg(''.join, axis=1)
        df.drop('Hour_temp', inplace=True, axis=1)
        #df['Date and time'] = pd.to_datetime(df['Date and time'], format=r'%Y-%m-%d %H')
        df.set_index('Date and time', inplace=True)
        df_lst.append(df)
        df.columns = [col.replace('\n','') for col in df.columns]

    pd.concat(df_lst).to_csv(output)

DIR = "C:/Users/czpkersten/Documents/timeslices/data"
OUT = "C:/Users/czpkersten/Desktop/output.csv"

#create_consumer_load_profile_file(DIR, OUT)

def consumer_load_profile(file):
    df = pd.read_csv(file)
    df.set_index('Date and time', inplace=True)
    return df

FILE = "C:/Users/czpkersten/Desktop/output.csv"

df = consumer_load_profile(FILE)

print(df)



color_lst = [
    'orangered',
    'gold'
    'limegreen',
    'cornflowerblue',
    'orchid',
    'darkorange',
    'darkturquoise',
    'brown',
    'rebeccapurple',
    'seagreen',
    'saddlebrown',
    'khaki',
    'palevioletred',
    'dimgrey'
]

def perform_fft(input, output, column):
    '''
    input: file containing time series
    ouput: output file destination
    column: Load [MW] etc
    '''
    df = pd.read_csv(input)
    #print(df)
    #From: https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.04-FFT-in-Python.html

    # Fourier transform
    data = df[column].to_numpy()
    #print(data)
    X = fft(data)
    N = len(X)
    n = np.arange(N)
    sr = 1/(60*60) #Sampling rate: once per hour (1/3600 per second)
    T = N/sr
    freq = n/T 

    # Get the one-sided spectrum & frequency
    n_oneside = N//2 - 1
    f_oneside = freq[:n_oneside]
    #f_oneside = f_oneside[1:]
    #X = X[1:]
    #f_oneside = f_oneside[f_oneside > 0]
    print(np.abs(X))
    print(f_oneside)
    #print(f_oneside)
    
    # Frequencies in hours and days
    t_h = 1/f_oneside / (60 * 60)
    t_d = 1/f_oneside / (60 * 60 * 24)

    # Save FFT as CSV
    dct = {
        'X': np.abs(X[:n_oneside])/n_oneside,
        't_h' : t_h,
        't_d' : t_d
    }

    df = pd.DataFrame(dct)

    # Filter results: only values with an amplitude higher than 25 and a frequency lower than one year (365 days)
    #df = df[(df['X']>=25) & (df['t_d'] <= 365) ]
    df = df[df['t_d'] <= 365]
    print(output)
    df.sort_values(by='X', ascending=False).to_csv(output, index=False)

DIR = "C:/Users/czpkersten/Desktop"
columns = set(df.columns) - {'Date and time', 'Day', 'Hour', 'Hour number in year'} 
for column in columns:
    output = f"{DIR}/{column.lower()} fft.csv"
    perform_fft(FILE, output, column)