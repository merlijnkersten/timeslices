
LOAD_PATH = r"C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/load 2015-2021.csv"

GENERATION_PATH = r"C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/generation 2015-2021.csv"

DIRECTORY =  r"C:/Users/Merlijn Kersten/Documents/UK/timeslices-outputs/"

#PRICE_PATH = r"C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/prices 2015-2021.csv"



# FIX
#IMPORT_EXPORT_PATHS = [f"C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/cross border {year}.csv" for year in range(2015, 2022)]

import os

cwd = os.getcwd()

data_path = os.path.join(cwd, 'data')

LOAD_PATH = os.path.join(data_path, 'load 2015-2021.csv')

GENERATION_PATH = os.path.join(data_path, 'generation 2015-2021.csv')

PRICE_PATH = os.path.join(data_path, 'prices 2015-2021.csv')

CROSS_BORDER_PATH = os.path.join(data_path, 'cross border 2015-2021.csv')

DIRECTORY =  os.path.join(os.path.dirname(cwd), 'timeslices-output-2')
