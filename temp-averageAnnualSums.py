import pandas as pd
from itertools import product

PATH = r"C:/Users/czpkersten/Documents/timeslices/data/combined 2015-2021.csv"

df = pd.read_csv(PATH)

timeslices = ['Season weekday daynite', 'Season daynite']
columns = ['Imports [MW]', 'Exports [MW]', 'Load [MW]']

# Find average annual sum of the value of load/import/export/price over a timeslice.
for prod in product(timeslices, columns):
    ts = prod[0]
    col = prod[1]
    MWh_to_GJ = 3.6*(10**-6)
    number_of_years = 7 # 2015-2021

    temp = df.groupby(by=[ts])[col].sum().abs() * MWh_to_GJ / number_of_years
    
    output = f"C:/Users/czpkersten/Desktop/Sum {col.replace(' [MW]','')} {ts}.csv"
    temp.to_csv(output)