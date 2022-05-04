import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

directory = "C:/Users/czpkersten/Documents/timeslices-output/Output load"

os.chdir(directory)

files = os.listdir()

directory_og = r"C:/Users/Merlijn Kersten/Documents/UK/timeslices-outputs/Output load/"

files_og = [
    'Statistics load month_long daynite day.csv',
    'Statistics load month_long daynite month.csv',
    'Statistics load month_long daynite8.csv',
    'Statistics load month_long hour_long.csv',
    'Statistics load month_long weekday.csv',
    'Statistics load season daynite8.csv',
    'Statistics load season daynite day.csv',
    'Statistics load season daynite month.csv',
    'Statistics load season daynite season.csv',
    'Statistics load season weekday daynite8.csv',
    'Statistics load season weekday daynite day.csv',
    'Statistics load season weekday daynite month.csv',
    'Statistics load season weekday daynite season.csv',
]

for file in files:

    #path = directory + file
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

    plt.title(file.replace('.csv',''))
    plt.grid()
    plt.tight_layout()
    plt.savefig(file.replace('.csv', '.png'), dpi=300, format='png')
    plt.show()