from datetime import datetime, date, time, timedelta, tzinfo
import itertools
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pytz
from scipy.fft import fft
import seaborn as sns

# Import own packages from other scripts
import load


lst = [f"C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/cross border {year}.csv" for year in range(2015, 2022)]
df = load.generate_cross_border_csv(lst)
df.to_csv("C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/cross border 2015-2021.csv")

lst = [f"C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/prices {year}.xls" for year in range(2015, 2022)]
output = "C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/prices 2015-2021.csv"
load.generate_price_csv(lst, output)

directory = "C:/Users/Merlijn Kersten/Documents/UK/timeslices/data"
output = "C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/consumer load profile 2015-2021.csv"
load.generate_consumer_load_profile_csv(directory, output)

'''
path = "C:/Users/Merlijn Kersten/Desktop/combined.csv"

df = pd.read_csv(path)

df["Date and time [UTC]"] = pd.to_datetime(df["Date and time [UTC]"])#, format=r"%Y-%m-%d %H:%M:%S+%z")

df.set_index("Date and time [UTC]", inplace=True)   

df = load.polish(df)

df.to_csv(path.replace('.csv', ' 2.csv'))
'''