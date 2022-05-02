from cmath import inf
import numpy as np
from scipy.fft import fft, fftfreq
import pandas as pd
import matplotlib.pyplot as plt

PATH = "C:/Users/czpkersten/Documents/timeslices/data/combined 2015-2021.csv"
SAMPLE_RATE = 365 # once per day, 365.25 per year
DURATION = 7 # 2015-2016

df = pd.read_csv(PATH)

data = df['Price [CZK/MWh]'].to_numpy()
'''
print(data)

# Number of samples in normalized_tone
N = len(data)

yf = fft(data)
print(yf)
xf = fftfreq(N, 1 / SAMPLE_RATE)

print(np.abs(yf))

print(xf)

plt.plot(xf, np.abs(yf))
plt.xlim(-10,200)
plt.show()
'''

#https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.04-FFT-in-Python.html

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
'''
plt.figure(figsize = (12, 6))
plt.plot(f_oneside, np.abs(X[:n_oneside]), 'b')
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.show()
'''
# convert frequency to hour
t_h = 1/f_oneside / (60 * 60)

fig, axs = plt.subplots(2, 1, figsize=(10,10))

axs[0].stem(t_h, np.abs(X[:n_oneside])/n_oneside, markerfmt=',')
axs[0].set_xticks([6, 12, 24, 84, 168])
axs[0].set_xlim(0, 200)
axs[0].set_xlabel('Period ($hour$)')

# convert frequency to day
t_d = 1/f_oneside / (60 * 60 * 24)

axs[1].stem(t_d, np.abs(X[:n_oneside])/n_oneside, markerfmt=',')
#axs[1].set_xticks([168, 2190, 2890, 8760])
#axs[1].set_xlim(0, 9000)
axs[1].set_xticks([7, 31, 365])
axs[1].set_xlim(0, 370)
axs[1].set_xlabel('Period ($day$)')

dct = {
    'X': np.abs(X[:n_oneside])/n_oneside,
    't_h' : t_h,
    't_d' : t_d
}
df = pd.DataFrame(dct)
df = df[(df['X']>=25) & (df['t_h'] <= 8784) ]
df.sort_values(by='X', ascending=False).to_csv("C:/Users/czpkersten/Documents/timeslices/data/combined 2015-2021 prices fft.csv", index=False)

plt.show()