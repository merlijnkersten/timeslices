import pandas as pd
import itertools
import matplotlib.pyplot as plt

# Lists of seasonal timeslices
spring_ts = ['1. ZN', '1. ZP', '1. ZD']
summer_ts = ['2. SN', '2. SP', '2. SD']
autumn_ts = ['3. FN', '3. FP', '3. FD']
winter_ts = ['4. WN', '4. WP', '4. WD']

# Lists of daynite timeslices
night_ts = ['1. ZN', '2. SN', '3. FN', '4. WN']
day_ts = ['1. ZD', '2. SD', '3. FD', '4. WD']
peak_ts = ['1. ZP', '2. SP', '3. FP', '4. WP']

# Full list of time slices
ts_lst = ['1. ZN', '1. ZP', '1. ZD', 
    '2. SN', '2. SP', '2. SD', 
    '3. FN', '3. FP', '3. FD',
    '4. WN', '4. WP', '4. WD']


# Translation dictionary from timeslice character to long name
ts_dct = {
    'N' : 'Night',
    'D' : 'Day',
    'P' : 'Peak',
    'Z' : 'Spring',
    'S' : 'Summer',
    'F' : 'Autumn',
    'W' : 'Winter'}

def fmt_col(col):
    '''
    Reformats a column by removing unit information and setting it to lowercase.
    '''
    col = col.replace(' [MW]', '')
    col = col.replace(' [EUR/MWh]', '-euro')
    col = col.replace(' [CZK/MWh]', '-czk')
    return col.lower()

def import_load_generation(load_path, generation_path):
    '''
    import load and generation CSVs as polished Dataframes
    load_path: path to load data CSV
    generation_path: path to generation data CSV
    output: DataFrame containing load and generation data
    '''

    # Read load data
    load_df = pd.read_csv(load_path, sep=";", header=2)
    # Create a timestamp column based on "Date" and set this as the index
    load_df["Date and time"] = pd.to_datetime(load_df["Date"], format=r"%d.%m.%Y %H:%M")
    load_df.set_index("Date and time", inplace=True)
    # Remove unnecessary columns
    load_df.drop(columns=["Unnamed: 3", "Date"], inplace=True)

    # Read generation data
    generation_df = pd.read_csv(generation_path, sep=';', header=2)
    # Create a timestamp column based on "Date" and set this as the index    
    generation_df["Date and time"] = pd.to_datetime(generation_df["Date"], format=r"%d.%m.%Y %H:%M")
    generation_df.set_index("Date and time", inplace=True)
    # Remove unnecessary columns
    generation_df.drop(columns=["Unnamed: 10", "Date"], inplace=True)
    # Find total generation by summing generation of various technologies
    generation_df["Generation sum [MW]"] = generation_df.sum(axis=1)

    # Merge the generation and load dictionaries based on their shared index.
    combined_df = pd.merge(generation_df, load_df, left_index=True, right_index=True)
    # Create data, year, month, and hour columns
    combined_df["Date"] = combined_df.index.date
    combined_df["Year"] = combined_df.index.year
    combined_df["Month"] = combined_df.index.month
    combined_df["Hour"] = combined_df.index.hour

    # Find 'net' export (without taking losses into consideration)
    combined_df["Net export (generation - load) [MW]"] = combined_df["Generation sum [MW]"] - combined_df["Load including pumping [MW]"]

    return combined_df


def find_import_export(row, kind):
    '''
    determines hourly average import and export values. if there, on average, 
    no import or exports to any border crossing it returns zero (not None) export
    or import.
    row: row from the output of DataFrame of import_cross_border_files
    kind: 'import' or 'export'
    TODO how to restrict values in Python? e.g. kind = ['import', 'export']
    '''
    # border crossing columns
    columns = ['Poland [MW]','Slovakia [MW]', 'Austria [MW]', 'Germany (south) [MW]', 'Germany (north) [MW]']
    if kind == 'import':
        # Imports into CR are positive values. Find all values larger than zero
        transfers = [row[column] for column in columns if row[column] >= 0]
    elif kind == 'export':
        # Exports from CP are negative values. Find all values smaller than zero
        transfers = [row[column] for column in columns if row[column] <= 0]
    # The sum of the values in transfers is the total of the average export/import values
    return sum(transfers)

    # Using `sum()` will automatically return 0 if there are no imports/exports. Should this be None?
    # Alternative: 
    '''
    if sum(transfers) != 0:
        return sum(transfers)
    else:
        return None
    '''


def import_cross_border_files(lst):
    '''
    lst: list of paths
    loads CSVs and combines them into a single, polished file.
    '''

    # Empty list, to be populated with DataFrames for every year.
    dfs_lst = []

    # Translation dictionary from TSO names to their respective countries
    tso_dct = {
        'PSE Actual [MW]'   : 'Poland [MW]',
        'SEPS Actual [MW]'  : 'Slovakia [MW]',
        'APG Actual [MW]'   : 'Austria [MW]',
        'TenneT Actual [MW]': 'Germany (south) [MW]',
        '50HzT Actual [MW]' : 'Germany (north) [MW]',
        'CEPS Actual [MW]'  : 'Net import [MW]'
    }

    # Unecessary columns, will be removed later.
    redundant_columns = ['Unnamed: 13', 'Date', 'PSE Planned [MW]', 'SEPS Planned [MW]', 
        'APG Planned [MW]', 'TenneT Planned [MW]', '50HzT Planned [MW]','CEPS Planned [MW]']


    for path in lst:
        # Read cross border data
        df = pd.read_csv(path, skiprows=2, sep=';')
        # Create a timestamp column based on "Date" and set this as the index
        df["Date and time"] = pd.to_datetime(df["Date"], format=r"%d.%m.%Y %H:%M")
        df.set_index("Date and time", inplace=True)       
        # Drop unecessary columns
        df.drop(columns=redundant_columns, inplace=True)
        # Rename columns from TSO names to country names
        df.columns = [tso_dct[i] for i in list(df.columns)]
        # Append the Dataframe to the Datafraemes list
        dfs_lst.append(df)

    # Concatenate dataframes together
    df = pd.concat(dfs_lst)

    # Create import and export columns using the find_import_export function
    df['Imports [MW]'] = df.apply(lambda i: find_import_export(i, 'import'), axis=1)
    df['Exports [MW]'] = df.apply(lambda i: find_import_export(i, 'export'), axis=1)

    return df


def zero_padded_hour(i):
    '''
    Hours in price data set range from 1-24, Datetime uses 00-23. 
    This function substracts one from the time, changes the type to
    string, and adds a leading zero if the hour is a single digit.
    '''
    j = str(i-1)
    if len(j) == 1:
        return ' 0' + j
    else:
        return ' '  + j


def generate_prices_csv(prices_paths, output_path):
    '''
    reads prices XLSs and returns a formatted, polished dataframe
    prices_paths: list of paths to annual prices XLS from 
    https://www.ote-cr.cz/en/short-term-markets/electricity/day-ahead-market
    and saves it as a CSV at output_path
    prices_paths: list of paths
    output_path: path to output CSV
    '''

    # Empty list, will be populated with Dataframes
    df_lst = []

    # For every path:
    for path in prices_paths:
        # Read 'DAM' (day-ahead) sheet 
        df = pd.read_excel(path, skiprows=5,  engine='xlrd', sheet_name='DAM')
        # Keep only the Day, Hour, Marginal price CZ (EUR/MWh), Marginal price CZ (CZK/MWH) columns
        df = df[['Day', 'Hour', 'Marginal price CZ (EUR/MWh)', 'Marginal price CZ (CZK/MWh)']]
        # During DST change, hour is set to 25. I remove this data point as I wasn't sure how to deal with it
        # Better alternative way? Effect on accuracy is likely small due to size of data set. 
        df = df[ df['Hour'] != 25 ]
        # Create a date and time column by cominbining the Day and Hour columns, setting it to datetime
        df['Date and time'] = df['Day'].dt.strftime(r'%Y-%m-%d') + df['Hour'].apply(zero_padded_hour)
        df['Date and time'] = pd.to_datetime(df['Date and time'], format=r'%Y-%m-%d %H')
        # Use this column as the index, and remove the now superfluous day and our columns
        df.set_index("Date and time", inplace=True)
        df.drop(columns=['Day', 'Hour'], inplace=True)
        # Rename the remaining price columns.
        df.columns = ['Price [EUR/MWh]', 'Price [CZK/MWh]']
        # Append the dataframe to the list of dataframes
        df_lst.append(df)
    
    # Concatenate the dataframes in the list together and save it.
    pd.concat(df_lst).to_csv(output_path)


def import_prices(path):
    '''
    Function to import the file created in the create_prices_csv function
    Returns the CSV as a formatted Dataframe
    '''
    # Read file
    df = pd.read_csv(path)
    # Change Date and time column to a datetime column and set it as the index
    df['Date and time'] = pd.to_datetime(df['Date and time'], format=r'%Y-%m-%d %H', )
    df.set_index('Date and time', inplace=True)

    return df


def assign_seasons(df):
    '''
    Assign the correct (Czech) season to every day by creating a look-up 
    dictionary for every date in the dataset, and then matching the dates
    to the correct season. This method is slightly convuleted, but is much
    faster than creating a function that assigns the correct season to a 
    given date 
    df: Dataframe with 'Date' column (in datetime format) 
    returns: Seasons PD series
    '''

    # Empty look-up dictionary, to be populated with 'dates':'season'
    dates_to_season = dict()

    # Years in the data set. Could also retrieve these?
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
    #years = list(df['Year'].unique())

    seasons = [
        # First date of the season (/mm/dd)
        #        |            Last date of the season (/mm/dd )
        #        |                 |            Name of the season 
        {'start' : '/01/01', 'end' : '/03/14', 'season' : 'Winter'},
        {'start' : '/03/15', 'end' : '/05/31', 'season' : 'Spring'},
        {'start' : '/06/01', 'end' : '/08/30', 'season' : 'Summer'},
        {'start' : '/08/31', 'end' : '/11/15', 'season' : 'Autumn'},
        {'start' : '/11/16', 'end' : '/12/31', 'season' : 'Winter'}
    ]

    # For every combination of years and seasons
    for prod in itertools.product(years, seasons):
        # Retrieve year, season start/end date and name from product
        year = prod[0]
        start_date = prod[1]['start']
        end_date = prod[1]['end']
        season = prod[1]['season']

        # For every date in this season and year, add the date with the season to the look-up dictionary.
        for date in pd.date_range(start=f"{year}{start_date}", end=f"{year+1}{end_date}"):
            date_fmt = str(date)[0:10] #Or, format as "%Y-%m-%d"
            dates_to_season[date_fmt] = season

    # Map dates to season and return this series.
    return df['Date'].astype(str).map(dates_to_season)


def assign_daynite(df):
    '''
    Divides data, for every season, into night (between 20:00-08:00, 12h), peak (highest load, 2h) and day (rest, 10h)
    df: Dataframe with 'Hour', 'Season', 'Load [MW]' columns.
    returns: timeslice series
    '''

    # Find a more elegant way to do this

    # Date between 20:00-08:00 is saved in a night dataframe, other day is saved in a day_and_peak dataframe.
    night_df = df[(df['Hour']<8) | (df['Hour']>=20)].copy(deep=True)
    night_df['Daynite'] = 'Night'
    day_and_peak_df = df[(df['Hour']>=8) & (df['Hour']<20)].copy(deep=True)
    
    # For every season, the two hours with the highest load are found and saved in a peak dataframe
    peak_dfs = []
    for season in ['Spring', 'Summer', 'Autumn', 'Winter']:
        season_df = day_and_peak_df[day_and_peak_df['Season']==season].copy(deep=True)
        length = season_df.shape[0]
        percentile = (1/24)*2
        n = round(length * percentile)
        peak_dfs.append(season_df.nlargest(n, 'Load [MW]').copy(deep=True))
    peak_df = pd.concat(peak_dfs)
    peak_df['Daynite'] = 'Peak'
    # The peak data is removed from the day_and_peak dataframe, 
    peak_ids = peak_df.index
    day_df = day_and_peak_df.drop(labels=peak_ids, axis=0).copy(deep=True)
    day_df['Daynite'] = 'Day'

    # Ensure that no data was lost by checkin if the length of the partial dataframes equals the original dataframe
    test = night_df.shape[0] + peak_df.shape[0] + day_df.shape[0] == df.shape[0]
    if not test:
        raise Exception('Timeslice dataframes do not have the correct length')

    # Create a single daynite dataframe and extract the 'Daynite' column
    daynite_df = pd.concat([night_df, peak_df, day_df])['Daynite']

    # Merge the daynite series with the given dataframe, and return the merged dataframe.
    return pd.merge(df, daynite_df, left_index=True, right_index=True)


def assign_ts(df):
    '''
    Combines 'Season' and 'Daynite' columns into a single 'Timeslice' column
    df: Dataframe with 'Season' and 'Daynite' columns
    output: 'Timeslice' series
    '''
    # Map from season name (long) to model abbreviation (short). Includes number for easy sorting.
    seasons_map = {
        'Spring': '1. Z',
        'Summer': '2. S',
        'Autumn': '3. F',
        'Winter': '4. W'
    }
    # Map from danite name (long) to model abbreviation (short)
    daynite_map = {
        'Night': 'N',
        'Peak' : 'P',
        'Day'  : 'D'
    }
    # Map both season and daynite columns to short form, concatenate and return.
    return df['Season'].map(seasons_map) + df['Daynite'].map(daynite_map)    


def create_load_duration_graph(df, ts_lst, column, ttl, axs):
    '''
    df: dataframe with plotting data,
    ts_list: list of timeslices to plot,
    column: which dataframe column to plot,
    ttl: title of plot,
    axs: matplotlib.pyplot axis
    '''

    linestyle_dct = {
        'N' : 'solid',
        'D' : 'dashed',
        'P' : 'dotted'
    }

    colour_dct = {
        'Z' : 'limegreen',
        'S' : 'gold',
        'F' : 'orangered',
        'W' : 'cornflowerblue'
    }

    for ts in ts_lst:    
        data = sorted(list(df[df['TS']==ts][column]),reverse=True)
        data_len = len(data)
        y = [(i+1)/data_len for i in range(data_len)]
        axs.plot(y, data, label=ts, c=colour_dct[ts[3]], ls=linestyle_dct[ts[4]])
        axs.legend()
        axs.set_title(ttl)
        axs.set_xlabel('Annual percentage')
    

def create_seasonal_load_duration_graph(df, column, directory):
    ts = [spring_ts, summer_ts, autumn_ts, winter_ts]
    name = ['Spring', 'Summer', 'Autumn', 'Winter']
    pos = [0, 1, 2, 3]

    fig, axs = plt.subplots(1, 4, sharey=True, figsize=(10,5))
    for i in zip(ts, name, pos):
        create_load_duration_graph(df, i[0], column, i[1], axs[i[2]])
    axs[0].set_ylabel(column)

    path = directory + f'Load duration curve {fmt_col(column)} seasons.png'
    
    plt.tight_layout()
    plt.savefig(path, dpi=300, format='png')
    plt.show()

def create_daynite_load_duration_graph(df, column, directory):
        
    ts = [night_ts, day_ts, peak_ts]
    name = ['Night', 'Day', 'Peak']
    pos = [0, 1, 2]

    fig, axs = plt.subplots(1, 3, sharey=True, figsize=(10,5))
    for i in zip(ts, name, pos):
        create_load_duration_graph(df, i[0], column, i[1], axs[i[2]])
    axs[0].set_ylabel(column)

    path = directory + f'Load duration curve {fmt_col(column)} daynite.png'
    
    plt.tight_layout()
    plt.savefig(path, dpi=300, format='png')
    plt.show()

def get_statistics(df, ts, column, directory):

    data = df[df['TS']==ts][column]
    dct = {
                 f'{column}' : f'{ts_dct[ts[3]]} {ts_dct[ts[4]].lower()}',
                      'Mean' : round(data.mean(), 2),
        'Standard deviation' : round(data.std(), 2),
                   'Minimum' : round(data.min(), 2),
            '10% percentile' : round(data.quantile(0.1), 2),
                    'Median' : round(data.median(), 2),
            '90% percentile' : round(data.quantile(0.9), 2),
                   'Maximum' : round(data.max(), 2)
    }
    
    ts_fmt = f'{ts_dct[ts[3]].lower()} {ts_dct[ts[4]].lower()}'

    path = directory + f'Statistics {fmt_col(column)} {ts_fmt}.csv'

    output_df = pd.DataFrame([dct]).T
    
    output_df.to_csv(path, header=False)

    output_df.columns = ['Value']

    return output_df


def get_all_statistics(df, column, directory):
    path = directory + f'Output {fmt_col(column)}.xlsx'

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    
    for ts in ts_lst:
        output = get_statistics(df, ts, column, directory)
        name = f'{ts_dct[ts[3]]} {ts_dct[ts[4]].lower()}'
        output.to_excel(writer, sheet_name=f'{name}')
    
    writer.save()