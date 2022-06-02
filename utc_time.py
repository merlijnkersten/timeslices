import pandas as pd
import pytz
from datetime import datetime, date, time, timedelta, tzinfo




"""
There are two ways to change time:

| Date time format | Normal day | WT to ST  | ST to WT  | Files                                  |
| ---------------- | ---------- | --------- | --------- | -------------------------------------- |
| 01-01-2015, 1    | 1-24       | 1-23      | 1-25      | OTE-ČR: prices, consumer load profiles |
| 01.01.2015 00:00 | 0-23       | 0-1, 3-23 | 0-2, 2-23 | ČEPS: cross border, load, generation   |


"""



'''
change_dates_no_fmt = [
    '2015-03-29', '2016-03-27', '2017-03-26', '2018-03-25', '2019-03-31', '2020-03-29', '2021-03-28',
    '2015-10-25', '2016-10-30', '2017-10-29', '2018-10-28', '2019-10-27', '2020-10-25', '2021-10-31'
]

change_dates = [dt.date(i, r'%Y-%m-%d') for i in change_dates_no_fmt]
'''


def to_utc_ceps(i, changeover_dates, st_to_wt, st_to_wt_set):
    czech_tz = pytz.timezone('Europe/Prague')
    
    date_time = datetime.strptime(i, r'%d.%m.%Y %H:%M')
    local_date = date_time.date()
    done = []
    if local_date not in changeover_dates:
        # regular date; timezone is simply PRAGUE (CET/CEST) for whole day
        local_date_time =  czech_tz.localize(date_time)
        return local_date_time.astimezone(pytz.utc)
    elif local_date in st_to_wt:
        # Summer time to winter time
        hour_local = date_time.hour
        if hour_local != 2:
            local_date_time =  czech_tz.localize(date_time)
            return local_date_time.astimezone(pytz.utc)
        elif local_date not in st_to_wt_set:
            # first occuence of 02:00 >>> it is still summer time
            st_to_wt_set = st_to_wt_set - {local_date}
            offset = -2
            date_time = date_time + timedelta(hours=offset)
            return pytz.utc.localize(date_time)
        else:
            # second occurence of 02:00 >>> it is winter time
            offset = -1
            date_time = date_time + timedelta(hours=offset)
            return pytz.utc.localize(date_time)
    else:
        # Winter time to summer time
        local_date_time =  czech_tz.localize(date_time)
        return local_date_time.astimezone(pytz.utc)       


def to_utc_otecr(i, changeover_dates, st_to_wt):
    czech_tz = pytz.timezone('Europe/Prague')

    try:
        date_time= datetime.strptime(i, r'%Y-%m-%d %H')

    except ValueError:
        local_hour = int(i[11:13])
        if local_hour == 24:
            local_date = datetime.strptime(i[:10], r'%Y-%m-%d').date()
            date_time = datetime.combine(local_date, time(23, 0))
            return pytz.utc.localize(date_time)
        else:
            raise ValueError(f'Unexpected value hour value: {i}')

    date_time= datetime.strptime(i, r'%Y-%m-%d %H')
    local_date = date_time.date()
    hour_local = date_time.hour
    if local_date not in changeover_dates:
        local_date_time =  czech_tz.localize(date_time)
        return local_date_time.astimezone(pytz.utc)
    elif local_date in st_to_wt:
        # summer time to winter time change-over
        # 03:00 |---> 02:00
        offset = -2
        date_time = date_time + timedelta(hours=offset)
        return pytz.utc.localize(date_time)
    else:
        # winter time to summer time change-over
        # 02:00 |---> 03:00
        offset = -1
        date_time = date_time + timedelta(hours=offset)
        return pytz.utc.localize(date_time)

def to_utc(df, kind):
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
    st_to_wt_set = set(st_to_wt)
    if kind == 'otecr':
        return df['Date and time'].apply(lambda i: to_utc_otecr(i, changeover_dates, st_to_wt))
    elif kind == 'ceps':
        return df['Date'].apply(lambda i: to_utc_ceps(i, changeover_dates, st_to_wt, st_to_wt_set))
    else:
        raise ValueError(f"Uknown kind: {kind} (not 'otecr' or 'ceps')")


def czech_time(i):
    czech_tz = pytz.timezone('Europe/Prague')
    return i.astimezone(czech_tz).replace(tzinfo=None)




path_otecr = "C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/consumer load profile 2015-2021.csv"
df_otecr = pd.read_csv(path_otecr)
df_otecr['UTC'] = to_utc(df_otecr, 'otecr')
df_otecr['Local'] = df_otecr['UTC'].apply(czech_time)
df_otecr.to_csv("C:/Users/Merlijn Kersten/Desktop/test-otecr.csv")

path_ceps = "C:/Users/Merlijn Kersten/Documents/UK/timeslices/data/generation 2015-2021.csv"
df_ceps = pd.read_csv(path_ceps, delimiter=';', skiprows=2)
df_ceps['UTC'] = to_utc(df_ceps, 'ceps')
df_ceps['Local'] = df_ceps['UTC'].apply(czech_time)
df_ceps.to_csv("C:/Users/Merlijn Kersten/Desktop/test_ceps.csv")