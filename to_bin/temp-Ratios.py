import pandas as pd

#PATH = "C:/Users/czpkersten/Documents/timeslices/data/combined 2015-2021.csv"
PATH = "C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/combined 2015-2021.csv"
df = pd.read_csv(PATH)

print(f'\nLength: {df.shape}')

print('\nSeason:')

print(df['Season'].value_counts())

print('\nWeekday:')

print(df['Weekday'].value_counts())

print('\nDaynite:')

print(df['Daynite'].value_counts())

print('\nSeason weekday:')

print(df['Season weekday'].value_counts())

print('\nFull time slice:')

print(df['Full time slice'].value_counts())