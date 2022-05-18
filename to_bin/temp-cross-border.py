import pandas as pd
import os

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


def cross_border_files(lst):
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

def cross_border(cross_border_path):
    df = pd.read_csv(cross_border_path)
    df["Date and time"] = pd.to_datetime(df["Date and time"], format=r"%Y-%m-%d %H:%M:%S")
    df.set_index("Date and time", inplace=True)                             

    return df

IMPORT_EXPORT_PATHS = [f"C:/Users/czpkersten/Documents/timeslices/data/cross border {year}.csv" for year in range(2015, 2022)]

df = cross_border_files(IMPORT_EXPORT_PATHS)

print(df)

cwd = os.getcwd()
data_path = os.path.join(cwd, 'data')
path = os.path.join(data_path, 'cross border 2015-2021.csv')

df.to_csv(path)

df2 = pd.read_csv(path)

print(df2)