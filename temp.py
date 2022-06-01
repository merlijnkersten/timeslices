from multiprocessing.sharedctypes import Value
import pandas as pd
import pytz
from datetime import datetime, date, time, timedelta

path = "C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/consumer load profile 2015-2021.csv"

df = pd.read_csv(path)

'''
change_dates_no_fmt = [
    '2015-03-29', '2016-03-27', '2017-03-26', '2018-03-25', '2019-03-31', '2020-03-29', '2021-03-28',
    '2015-10-25', '2016-10-30', '2017-10-29', '2018-10-28', '2019-10-27', '2020-10-25', '2021-10-31'
]

change_dates = [dt.date(i, r'%Y-%m-%d') for i in change_dates_no_fmt]
'''

wt_to_st_lst = [
    (2015, 3, 29),
    (2016, 3, 27),
    (2017, 3, 26),
    (2018, 3, 25),
    (2019, 3, 31),
    (2020, 3, 29),
    (2021, 3, 28),    
]
st_to_wt_lst = [
    (2015, 10, 25),
    (2016, 10, 30),
    (2017, 10, 29),
    (2018, 10, 28),
    (2019, 10, 27),
    (2020, 10, 25),
    (2021, 10, 31)
]

dates_lst = wt_to_st_lst + st_to_wt_lst
changeover_dates = [date(i[0], i[1], i[2]) for i in dates_lst]
st_to_wt = [date(i[0], i[1], i[2]) for i in st_to_wt_lst]

prague_tz = pytz.timezone('Europe/Prague')

def to_utc(i):
    hour_int = float(i[11:13])
    if hour_int > 23:
        # 2019-01-01 03
        # 01234567890123
        if hour_int != 24:
            raise ValueError(f'Unexpected value: {i}')
        date = datetime.strptime(i, r'%Y-%m-%d %H')
        date_time = datetime.combine(date, time(23, 0))
        return pytz.utc.localize(date_time)
    else:
        date_time= datetime.strptime(i[:13], r'%Y-%m-%d %H')
        date = date_time.date()
        hour = date_time.hour
        if date not in changeover_dates:
            local_date_time =  prague_tz.localize(date_time)
            return local_date_time.astimezone(pytz.utc)
        elif date not in st_to_wt:
            # winter time to summer time change-over
            # 02:00 |---> 03:00
            if hour <= 1:
                # winter time
                offset = - 1 # UTC offset
            else:
                # summer time
                offset = - 2 # UTC offset 
            date_time = date_time - timedelta(hours=offset)
            return pytz.utc.localize(date_time)
        else:
            # summer time to winter time change-over
            # 03:00 |---> 03:00
            if hour <= 3:
                # summer time
                offset =  - 2
            else:
                # winter time
                offset = - 1 
            date_time = date_time - timedelta(hours=offset)
            return pytz.utc.localize(date_time)

temp = df['Date and time'].to_list()
test = {i[11:13] for i in temp}
print(test)

df['UTC'] = df['Date and time'].apply(to_utc)
print(df['UTC'])
df.to_csv("C:/Users/Merlijn Kersten/Desktop/test.csv")

i = 2

try:
    i.append('z')
except:
    print('Except')
    i = i
    i += 1
    print('Except 2') 
else:
    print('Else')
finally:
    print('Finally')