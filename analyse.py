'''
Functions to analyse and visualise the data.

To do: re-create code for generation load/etc duration graphs.
  - Automatic plotting was difficult to get right (and not necessarily important).
    work on it was therefore abandoned. 
  - Homogenise plotting approach.

'''

import itertools
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.fft import fft
import seaborn as sns

from load import fmt

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

    # Two dictionaries to provide colours and linestyle - TODO rewrite code to do without?
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
        elif variable== 'b':
            title_text, label_text = value_a, value_b
        else:
            raise ValueError(f"Variable is: {variable} ({type(variable)}), but must be 'a' or 'b'.")
        
        mask = (df[column_a] == value_a) & (df[column_b] == value_b)
        data = df[mask][plot_column].sort_values(ascending=False)
        y = np.linspace(0, 1, len(data))
        axs.plot(y, data, label=label_text, c=colour_dct[value_a], ls=linestyle_dct[value_b])

    axs.legend()
    axs.set_title(title_text)
    axs.set_xlabel('Annual percentage')
    

def get_statistics(df, ts_lst, column_a, column_b, statistics_column, statistics_lst):
    
    for ts in ts_lst:
        value_a = ts[0]
        value_b = ts[1]

        mask = (df[column_a] == value_a) & (df[column_b] == value_b)
        data = df[mask][statistics_column]

        statistics_lst.append({
            'Column' : statistics_column.lower(),
            'Timeslice' : f'{value_a.lower()} {value_b.lower()}',
            'Mean' : fmt(data.mean()),
            'Standard deviation' : fmt(data.std()),
            'Minimum' : fmt(data.min()),
            '10% percentile' : fmt(data.quantile(0.1)),
            'Median' : fmt(data.median()),
            '90% percentile' : fmt(data.quantile(0.9)),
            'Maximum' : fmt(data.max())
        })

def timeslice_analysis(df, column_a, column_b, statistics_column, directory):
    # TODO Recreate version WITH plotting!
    statistics = []

    values_a = df[column_a].unique()
    values_b = df[column_b].unique()

    for value in values_a:
        ts = itertools.product([value], values_b)
        get_statistics(df, ts, column_a, column_b, statistics_column, statistics)

    #sub_directory = os.path.join(directory, f"Output {fmt(statistics_column)}")
    #if not os.path.exists(sub_directory):
    #    os.makedirs(sub_directory)

    csv_path = os.path.join(directory, f'Statistics {fmt(statistics_column)} - {fmt(column_a)} - {fmt(column_b)}.csv')
    pd.DataFrame(statistics).to_csv(csv_path, index=False)

def timeslice_analysis_2(df, statistics_column, directory):
    # TODO Recreate version WITH plotting!
    # EXAMPLE WITH Season weekday AS column_a AND Daynite AS column_b
    print('Unfinished')
    quit()
    statistics = []

    values_a = df['Season weekday 1'].unique()
    values_b = df['Daynite'].unique()

    fig, axs = plt.subplots(2, 4, sharey=True, figsize=(10,5))
    i = 0
    for value in values_a:
        ts = itertools.product([value], values_b)
        create_load_duration_graph(df, ts, 'Season weekday 1', 'Daynite', statistics_column, axs[i%2, i//2], 'b')
        get_statistics(df, ts, 'Season weekday 1', 'Daynite', statistics_column, statistics)
        i += 1

    axs[0,0].set_ylabel(statistics_column)
    axs[1,0].set_ylabel(statistics_column)

    plt.tight_layout()

    #sub_directory = f"{directory}Output {fmt(statistics_column)}/"
    #if not os.path.exists(sub_directory):
    #    os.makedirs(sub_directory)

    fig_path = f'{directory}Load duration curve {fmt(statistics_column)} seasons weekdays.png'
    plt.savefig(fig_path, dpi=300, format='png')

    csv_path = f'{directory}Statistics {fmt(statistics_column)} - season weekday 1 - daynite.csv'
    pd.DataFrame(statistics).to_csv(csv_path, index=False)

    plt.show()


def seasonal_weekday_daynite_analysis(df, column, directory):
    statistics = []

    seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    weekday = ['Weekend', 'Weekday']
    daynite = ['Night', 'Peak', 'Day']

    a = [' '.join(i) for i in itertools.product(seasons, weekday)]
    b = daynite
    #[('Spring weekday', 'Night'), (...), ...]

    fig, axs = plt.subplots(2, 4, sharey=True, figsize=(10,5), tight_layout=True)
    i = 0

    for season_weekday in a:
        ts = list(itertools.product([season_weekday], b))

        create_load_duration_graph(df, ts, 'Season weekday 1', 'Daynite', column, axs[i%2, i//2], 'b')

        statistics.append(get_statistics(df, ts, 'Season weekday 1', 'Daynite', column))

        i += 1

    axs[0,0].set_ylabel(column)
    axs[1,0].set_ylabel(column)

    fig_path = os.path.join(directory, f'Load duration curve {fmt(column)} seasons weekdays.png')
    plt.savefig(fig_path, dpi=300, format='png')

    csv_path = os.path.join(directory, f'Statistics {fmt(column)} seasons weekdays.csv')
    pd.DataFrame(statistics).to_csv(csv_path, index=False)

    plt.show()


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
    # WHAT DOES THE -1 DO HERE & WHY DOES IT WORK
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

    df = df[df['t_d'] <= 400]
    df.sort_values(by='X', ascending=False).to_csv(output, index=False)

linestyle_st = [
    'solid',
    'dashed',
    'dotted',
    'dashdot'
    'o', # circle
    'v', # triangle
    's', # square
    'd', # diamond
    '+', # plus
    'x', # x
]

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
    'palevioletred',
    'darkolivegreen',
    'steelblue',
    'navy'
    'dimgrey'
    'khaki', # TOO LIGHT REPLACE
]


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
        axs[0].set_title('Day')

        med_df = df[(cutoff_1 <= df['t_d']) & (df['t_d']<=cutoff_2)].nlargest(n=20, columns='X')
        X_d = med_df['X'].to_numpy()
        t_d = med_df['t_d'].to_numpy()
        X_d = X_d/X_max

        axs[1].stem(t_d, X_d, markerfmt=',', linefmt=color, basefmt='grey')
        axs[1].set_xticks([1, 7, 14, 21, 28])
        axs[1].grid()
        axs[1].set_title('Month')

        long_df = df[df['t_d']>=cutoff_2].nlargest(n=20, columns='X')
        X_d = long_df['X'].to_numpy()
        t_d = long_df['t_d'].to_numpy()
        X_d = X_d/X_max

        axs[2].stem(t_d, X_d, markerfmt=',', linefmt=color, basefmt='grey')
        axs[2].set_xticks([30, 91, 183, 274, 365])
        axs[2].grid()
        axs[2].set_title('Year')

        axs[0].set_xlabel('Frequency (hours)')
        axs[1].set_xlabel('Frequency (days)')
        axs[2].set_xlabel('Frequency (days)')
        fig.suptitle(f'Fast Fourier transform - {label} (2015-2021)')
        plt.savefig(f'{output} {label}.png', dpi=300, format='png')
        plt.show()
        i+=1


def plot_distribution(directory):
    '''
    Plots basic distribution of data, using Seaborn for a change (instead of Matplotlib).
    directory: folder containing solely files from get_statistics function (analyse.py)
    '''
    os.chdir(directory)

    files = os.listdir(directory)

    for file in files:
        #path variable needed here?

        df = pd.read_csv(file)

        sns.scatterplot(x='Mean', y='Timeslice', data=df, color='b', label='Mean')
        sns.scatterplot(x='Median', y='Timeslice', data=df, color='r', label='Median')

        for sign in [1, -1]:
            # Plot standard deviations
            pm = '+' if sign else '-'
            df[f'Mean{pm}SD'] = df['Mean'] + sign*df['Standard deviation']
            sns.scatterplot(x=f'Mean{pm}SD', y='Timeslice', data=df, color='b', marker='.')

        for column in ['Minimum', 'Maximum', '10% percentile', '90% percentile']:
            # Plot statistical information
            sns.scatterplot(x=column, y='Timeslice', data=df, color='r', marker='x')

        plt.title(file.replace('.csv','').lower())
        plt.grid()
        plt.tight_layout()
        plt.savefig(file.replace('.csv', '.png'), dpi=300, format='png')
        plt.show()