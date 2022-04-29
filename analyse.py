import pandas as pd
import itertools
import matplotlib.pyplot as plt
import numpy as np
import os

from variables import GENERATION_PATH, LOAD_PATH, DIRECTORY

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
        else:
            title_text, label_text = value_a, value_b
        
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

    sub_directory = f"{directory}Output {fmt(statistics_column)}/"
    if not os.path.exists(sub_directory):
        os.makedirs(sub_directory)

    csv_path = f'{sub_directory}Statistics {fmt(statistics_column)} - {fmt(column_a)} - {fmt(column_b)}.csv'
    pd.DataFrame(statistics).to_csv(csv_path, index=False)

def timeslice_analysis_2(df, statistics_column, directory):
    # TODO Recreate version WITH plotting!
    # EXAMPLE WITH Season weekday AS column_a AND Daynite AS column_b
    statistics = []

    values_a = df['Season weekday'].unique()
    values_b = df['Daynite'].unique()

    fig, axs = plt.subplots(2, 4, sharey=True, figsize=(10,5))
    i = 0
    for value in values_a:
        ts = itertools.product([value], values_b)
        create_load_duration_graph(df, ts, 'Season weekday', 'Daynite', statistics_column, axs[i%2, i//2], 'b')
        get_statistics(df, ts, 'Season weekday', 'Daynite', statistics_column, statistics)
        i += 1

    axs[0,0].set_ylabel(statistics_column)
    axs[1,0].set_ylabel(statistics_column)

    plt.tight_layout()

    #sub_directory = f"{directory}Output {fmt(statistics_column)}/"
    #if not os.path.exists(sub_directory):
    #    os.makedirs(sub_directory)

    fig_path = f'{directory}Load duration curve {fmt(statistics_column)} seasons weekdays.png'
    plt.savefig(fig_path, dpi=300, format='png')

    csv_path = f'{directory}Statistics {fmt(statistics_column)} - season weekday - daynite.csv'
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

    fig, axs = plt.subplots(2, 4, sharey=True, figsize=(10,5))
    i = 0

    for season_weekday in a:
        ts = list(itertools.product([season_weekday], b))

        create_load_duration_graph(df, ts, 'Season weekday', 'Daynite', column, axs[i%2, i//2], 'b')

        statistics.append(get_statistics(df, ts, 'Season weekday', 'Daynite', column))

        i += 1

    axs[0,0].set_ylabel(column)
    axs[1,0].set_ylabel(column)

    plt.tight_layout()

    #sub_directory = f"{directory}Output {fmt(column)}/"
    #if not os.path.exists(sub_directory):
    #    os.makedirs(sub_directory)

    fig_path = f'{directory}Load duration curve {fmt(column)} seasons weekdays.png'
    plt.savefig(fig_path, dpi=300, format='png')

    csv_path = f'{directory}Statistics {fmt(column)} seasons weekdays.csv'
    pd.DataFrame(statistics).to_csv(csv_path, index=False)

    plt.show()