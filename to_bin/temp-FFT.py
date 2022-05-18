import numpy as np
from scipy.fft import fft
import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "C:/Users/czpkersten/Documents/timeslices/data/combined 2015-2021.csv"
OUTPUT_PATH = "C:/Users/czpkersten/Documents/timeslices/data/combined 2015-2021 prices fft.csv"

df = pd.read_csv(INPUT_PATH)

#https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.04-FFT-in-Python.html

# Fourier transform
data = df['Price [CZK/MWh]'].to_numpy()
X = fft(data)
N = len(X)
n = np.arange(N)
sr = 1/(60*60) #Sampling rate: once per hour (1/3600 per second)
T = N/sr
freq = n/T 

# Get the one-sided specturm
n_oneside = N//2
# get the one side frequency
f_oneside = freq[:n_oneside]



fig, axs = plt.subplots(2, 1, figsize=(10,10))

# Plot FFT in hour frequency span
# convert frequency to hour
t_h = 1/f_oneside / (60 * 60)
axs[0].stem(t_h, np.abs(X[:n_oneside])/n_oneside, markerfmt=',')
axs[0].set_xticks([6, 12, 24, 84, 168])
axs[0].set_xlim(0, 200)
axs[0].set_xlabel('Period (hour)')

# Plot FFT in day frequency span
# convert frequency to day
t_d = 1/f_oneside / (60 * 60 * 24)
axs[1].stem(t_d, np.abs(X[:n_oneside])/n_oneside, markerfmt=',')
axs[1].set_xticks([7, 31, 365])
axs[1].set_xlim(0, 370)
axs[1].set_xlabel('Period (day)')

# Save FFT as CSV
dct = {
    'X': np.abs(X[:n_oneside])/n_oneside,
    't_h' : t_h,
    't_d' : t_d
}
df = pd.DataFrame(dct)
df = df[(df['X']>=25) & (df['t_h'] <= 8784) ]
df.sort_values(by='X', ascending=False).to_csv(OUTPUT_PATH, index=False)

plt.show()