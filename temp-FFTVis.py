import pandas as pd
import matplotlib.pyplot as plt
import os

directory = "C:/Users/czpkersten/Documents/timeslices-output/FFT"

os.chdir(directory)
files = os.listdir(directory)

colors = {
    'combined 2015-2021 exports fft.csv' : 'limegreen',
    'combined 2015-2021 imports fft.csv' : 'gold',
    'combined 2015-2021 prices fft.csv' : 'orangered',
    'combined 2015-2021 load fft.csv' : 'cornflowerblue',
}

labels = {
    'combined 2015-2021 exports fft.csv' : 'Exports',
    'combined 2015-2021 imports fft.csv' : 'Imports',
    'combined 2015-2021 prices fft.csv' : 'Prices',
    'combined 2015-2021 load fft.csv' : 'Load',
}

pos = {
    'combined 2015-2021 exports fft.csv' : 1,
    'combined 2015-2021 imports fft.csv' : 2,
    'combined 2015-2021 prices fft.csv' : 3,
    'combined 2015-2021 load fft.csv' : 0,
}

fig, axs = plt.subplots(4, 2, sharey=True, sharex='col', figsize=(10,11), tight_layout=True)

for file in files:
    
    df = pd.read_csv(file)
    X_d_max = df['X'].max()

    cutoff = 30 #days

    short_df = df[df['t_d']<=cutoff].nlargest(n=20, columns='X')
    X_d = short_df['X'].to_numpy()
    t_d = short_df['t_d'].to_numpy()
    X_d = X_d/X_d_max

    i = pos[file]

    axs[i,0].stem(t_d, X_d, markerfmt=',', linefmt=colors[file], basefmt='grey')
    axs[i,0].set_xticks([1, 7, 14, 21, 28])
    axs[i,0].grid()
    axs[i,0].set_ylabel(labels[file], rotation=0, labelpad=22)


    long_df = df[df['t_d']>=cutoff].nlargest(n=20, columns='X')
    X_d = long_df['X'].to_numpy()
    t_d = long_df['t_d'].to_numpy()
    X_d = X_d/X_d_max

    axs[i,1].stem(t_d, X_d, markerfmt=',', linefmt=colors[file], basefmt='grey')
    axs[i,1].set_xticks([30, 91, 183, 274, 365])
    axs[i,1].grid()

axs[3,0].set_xlabel('Frequency (days)')
axs[3,1].set_xlabel('Frequency (days)')
fig.suptitle('Fast Fourier transform (2015-2021)')
plt.show()