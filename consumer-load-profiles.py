import pandas as pd
import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt
import os

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
DIR = "C:/Users/Merlijn Kersten/Documents/UK/timeslices/data"
OUT = "C:/Users/czpkersten/Desktop/output.csv"
OUT = "C:/Users/Merlijn Kersten/Desktop/output.csv"
#create_consumer_load_profile_file(DIR, OUT)

def consumer_load_profile(file):
    df = pd.read_csv(file)
    df.set_index('Date and time', inplace=True)
    return df

FILE = "C:/Users/czpkersten/Desktop/output.csv"
FILE = "C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/consumer load profile 2015-2021.csv"

df = consumer_load_profile(FILE)

color_lst = [
    'orangered',
    'gold',
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
    'darkolivegreen',
    'steelblue',
    'navy'
    'dimgrey'
]

def perform_fft(input, output, column):
    '''
    input: file containing time series
    ouput: output file destination
    column: Load [MW] etc
    '''
    df = pd.read_csv(input)

    #From: https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.04-FFT-in-Python.html

    # Fourier transform
    data = df[column].to_numpy()

    X = fft(data)
    N = len(X)
    n = np.arange(N)
    sr = 1/(60*60) #Sampling rate: once per hour (1/3600 per second)
    T = N/sr
    freq = n/T 

    # Get the one-sided spectrum & frequency
    n_oneside = N//2 - 1
    f_oneside = freq[:n_oneside]
    
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
    df = df[df['t_d'] <= 400]
    df.sort_values(by='X', ascending=False).to_csv(output, index=False)

DIR = "C:/Users/czpkersten/Desktop"
DIR = "C:/Users/Merlijn Kersten/Documents/UK/timeslices-fft"
columns = set(df.columns) - {'Date and time', 'Day', 'Hour', 'Hour number in year'} 
for column in columns:
    output = f"{DIR}/{column.lower()} fft.csv"
    perform_fft(FILE, output, column)

def fft_visualisation(directory):
    '''
    directory: directory containing (solely) output files from perform_fft function.
    Plots the FFT over two domains, for all files present in directory.
    '''
    os.chdir(directory)
    files = os.listdir(directory)
    
    fig, axs = plt.subplots(len(files), 3, sharey=True, sharex='col', figsize=(10,11), tight_layout=True)
    if len(files) > len(color_lst):
        raise ValueError(f"{len(files)} files but only {len(color_lst)} available.")

    i = 0
    for file in files:

        label = file.split('/')[-1].split(' ')[0]
        color = color_lst[i]
        
        df = pd.read_csv(file)
        X_max = df['X'].max()

        cutoff_1 = 1.25 #days, (30 hours) cutoff for left and right graph.
        cutoff_2 = 30 # days

        short_df = df[df['t_d']<=cutoff_1].nlargest(n=20, columns='X')
        X = short_df['X'].to_numpy() #y values
        t_h = short_df['t_h'].to_numpy() 
        X = X/X_max # normalised x values

        axs[i,0].stem(t_h, X, markerfmt=',', linefmt=color, basefmt='grey')
        axs[i,0].set_xticks([6, 12, 18, 24])
        axs[i,0].grid()
        axs[i,0].set_ylabel(label, rotation=0, labelpad=22)


        med_df = df[(cutoff_1 <= df['t_d']) & (df['t_d']<=cutoff_2)].nlargest(n=20, columns='X')
        X_d = med_df['X'].to_numpy()
        t_d = med_df['t_d'].to_numpy()
        X_d = X_d/X_max

        axs[i,1].stem(t_d, X_d, markerfmt=',', linefmt=color, basefmt='grey')
        axs[i,1].set_xticks([1, 7, 14, 21, 28])
        axs[i,1].grid()

        long_df = df[df['t_d']>=cutoff_2].nlargest(n=20, columns='X')
        X_d = long_df['X'].to_numpy()
        t_d = long_df['t_d'].to_numpy()
        X_d = X_d/X_max

        axs[i,2].stem(t_d, X_d, markerfmt=',', linefmt=color, basefmt='grey')
        axs[i,2].set_xticks([30, 91, 183, 274, 365])
        axs[i,2].grid()

        i += 1

    axs[i-1,0].set_xlabel('Frequency (hours)')
    axs[i-1,1].set_xlabel('Frequency (days)')
    axs[i-1,2].set_xlabel('Frequency (days)')
    fig.suptitle('Fast Fourier transform (2015-2021)')
    plt.savefig(file.replace('.csv', '.png'), dpi=300, format='png')
    plt.show()

#fft_visualisation(DIR)

def fft_individual_visualisation(directory, output):
    os.chdir(directory)
    files = os.listdir(directory)
       
    if len(files) > len(color_lst):
        raise ValueError(f"{len(files)} files but only {len(color_lst)} available.")
    i=0
    for file in files:
        fig, axs = plt.subplots(1, 3, sharey=True, figsize=(8,5), tight_layout=True)

        label = file.split('/')[-1].split(' ')[0]
        color = color_lst[i]
        
        df = pd.read_csv(file)
        X_max = df['X'].max()

        cutoff_1 = 25/24 #days, (30 hours) cutoff for left and right graph.
        cutoff_2 = 30 # days

        short_df = df[df['t_d']<=cutoff_1].nlargest(n=20, columns='X')
        X = short_df['X'].to_numpy() #y values
        t_h = short_df['t_h'].to_numpy() 
        X = X/X_max # normalised x values

        axs[0].stem(t_h, X, markerfmt=',', linefmt=color, basefmt='grey')
        axs[0].set_xticks([6, 12, 18, 24])
        axs[0].grid()

        med_df = df[(cutoff_1 <= df['t_d']) & (df['t_d']<=cutoff_2)].nlargest(n=20, columns='X')
        X_d = med_df['X'].to_numpy()
        t_d = med_df['t_d'].to_numpy()
        X_d = X_d/X_max

        axs[1].stem(t_d, X_d, markerfmt=',', linefmt=color, basefmt='grey')
        axs[1].set_xticks([1, 7, 14, 21, 28])
        axs[1].grid()

        long_df = df[df['t_d']>=cutoff_2].nlargest(n=20, columns='X')
        X_d = long_df['X'].to_numpy()
        t_d = long_df['t_d'].to_numpy()
        X_d = X_d/X_max

        axs[2].stem(t_d, X_d, markerfmt=',', linefmt=color, basefmt='grey')
        axs[2].set_xticks([30, 91, 183, 274, 365])
        axs[2].grid()

        axs[0].set_xlabel('Frequency (hours)')
        axs[1].set_xlabel('Frequency (days)')
        axs[2].set_xlabel('Frequency (days)')
        fig.suptitle(f'Fast Fourier transform - {label} (2015-2021)')
        plt.savefig(f'{output} {label}.png', dpi=300, format='png')
        #plt.show()
        i+=1



OUTPUT = "C:/Users/Merlijn Kersten/Documents/UK/graphs/"

fft_individual_visualisation(DIR, OUTPUT)

NEW_DIR = "C:/Users/Merlijn Kersten/Documents/UK/timeslices-output/fft"

fft_individual_visualisation(NEW_DIR, OUTPUT)