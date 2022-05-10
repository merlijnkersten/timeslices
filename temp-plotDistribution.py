import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

directory = "C:/Users/czpkersten/Documents/timeslices-output/Output load"

os.chdir(directory)
files = os.listdir(directory)

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