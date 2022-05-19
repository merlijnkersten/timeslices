import pandas as pd
import itertools
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.fft import fft
import seaborn as sns

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
    n_oneside = N//2
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
    df = df[(df['X']>=25) & (df['t_d'] <= 365) ]
    print(output)
    df.sort_values(by='X', ascending=False).to_csv(output, index=False)

def fft_visualisation(directory):
    '''
    directory: directory containing (solely) output files from perform_fft function.
    Plots the FFT over two domains, for all files present in directory.
    '''
    os.chdir(directory)
    files = os.listdir(directory)

    dct = {
        # Add own file names here      
        # 'path_in_directory.csv' : [visualisation position, 'Column label', 'Plot colour']
        'combined 2015-2021 exports fft.csv' : [1, 'Exports', 'limegreen'],
        'combined 2015-2021 imports fft.csv' : [2, 'Imports', 'gold'],
        'combined 2015-2021 price fft.csv' : [3, 'Prices', 'orangered'],
        'combined 2015-2021 load fft.csv' : [0, 'Load', 'cornflowerblue'],      
    }

    fig, axs = plt.subplots(len(dct), 2, sharey=True, sharex='col', figsize=(10,11), tight_layout=True)

    for file in files:
        
        pos = dct[file][0]
        label = dct[file][1]
        color = dct[file][2]

        df = pd.read_csv(file)
        X_d_max = df['X'].max()

        cutoff = 30 #days, cutoff for left and right graph.

        short_df = df[df['t_d']<=cutoff].nlargest(n=20, columns='X')
        X_d = short_df['X'].to_numpy() #y values
        t_d = short_df['t_d'].to_numpy() 
        X_d = X_d/X_d_max # normalised x values

        axs[pos,0].stem(t_d, X_d, markerfmt=',', linefmt=color, basefmt='grey')
        axs[pos,0].set_xticks([1, 7, 14, 21, 28])
        axs[pos,0].grid()
        axs[pos,0].set_ylabel(label, rotation=0, labelpad=22)


        long_df = df[df['t_d']>=cutoff].nlargest(n=20, columns='X')
        X_d = long_df['X'].to_numpy()
        t_d = long_df['t_d'].to_numpy()
        X_d = X_d/X_d_max

        axs[pos,1].stem(t_d, X_d, markerfmt=',', linefmt=color, basefmt='grey')
        axs[pos,1].set_xticks([30, 91, 183, 274, 365])
        axs[pos,1].grid()

    axs[3,0].set_xlabel('Frequency (days)')
    axs[3,1].set_xlabel('Frequency (days)')
    fig.suptitle('Fast Fourier transform (2015-2021)')
    plt.savefig(file.replace('.csv', '.png'), dpi=300, format='png')
    plt.show()

def plot_distribution(directory):
    '''
    Plots basic distribution of data, using Seaborn (instead of Matplotlib).
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
            # Standard deviations
            pm = '+' if sign else '-'
            df[f'Mean{pm}SD'] = df['Mean'] + sign*df['Standard deviation']
            sns.scatterplot(x=f'Mean{pm}SD', y='Timeslice', data=df, color='b', marker='.')

        for column in ['Minimum', 'Maximum', '10% percentile', '90% percentile']:
            # Statistical information
            sns.scatterplot(x=column, y='Timeslice', data=df, color='r', marker='x')

        plt.title(file.replace('.csv','').lower())
        plt.grid()
        plt.tight_layout()
        plt.savefig(file.replace('.csv', '.png'), dpi=300, format='png')
        plt.show()


directory = "C:/Users/Merlijn Kersten/Documents/UK/timeslices-output/temp"
plot_distribution(directory)

quit()
columns = ['Load [MW]', 'Imports [MW]', 'Exports [MW]', 'Price [CZK/MWh]']

for column in columns:
    input = "C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/combined 2015-2021.csv"
    col_fmt = column.replace(' [MW]','').replace(' [CZK/MWh]', '').lower()
    output = f"C:/Users/Merlijn Kersten/Documents/UK/timeslices-output/fft/combined 2015-2021 {col_fmt} fft.csv"
    perform_fft(input, output, column)

directory = "C:/Users/Merlijn Kersten/Documents/UK/timeslices-output/fft"
fft_visualisation(directory)
