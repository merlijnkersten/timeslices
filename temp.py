import pandas as pd
import pytz
from datetime import datetime, date, time, timedelta

st_to_wt_lst = [
    (2015, 10, 25),
    (2016, 10, 30),
    (2017, 10, 29),
    (2018, 10, 28),
    (2019, 10, 27),
    (2020, 10, 25),
    (2021, 10, 31)
]
st_to_wt = [date(i[0], i[1], i[2]) for i in st_to_wt_lst]
st_to_wt_set = set(st_to_wt)
print(st_to_wt_set)


a = date(year=2015, month=10, day=25)

st_to_wt_set = st_to_wt_set - {a}

print(st_to_wt_set)