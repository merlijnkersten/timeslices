'''
Quick & dirty script for generating report visualisations

'''
import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "C:/Users/czpkersten/Documents/timeslices/data/combined 2015-2021.csv"
OUTPUT_PATH = "C:/Users/czpkersten/Documents/timeslices-output/"

INPUT_PATH = "C:/Users/Merlijn Kersten/Documents/uk/timeslices/data/combined 2015-2021.csv"
OUTPUT_PATH = "C:/Users/Merlijn Kersten/Documents/uk/timeslices-output/"

df = pd.read_csv(INPUT_PATH)

# Pesky daylight-saving hours
df = df[df['Hour'] <= 23]

# 1. Seasoan (var_col) graph
var_col = 'Season'
time_col = 'Hour'
value_col = 'Load [MW]'

vars = df[var_col].unique()

colour_dct = {
        'Spring' : 'limegreen',
        'Summer' : 'gold',
        'Autumn' : 'orangered',
        'Winter' : 'cornflowerblue'
}

fig, axs = plt.subplots(1, 4, sharey=True, figsize=(15,5), tight_layout=True)
i = 0
for var in vars:
    temp = df[df[var_col]==var]
    group = temp.groupby(by=[time_col])[value_col]
    
    x = temp[time_col].unique()
    axes = axs[i]
    
    mean = group.mean()
    axs[i].plot(x, mean, label=var, c=colour_dct[var])
    
    q75 = group.quantile(0.75)
    q25 = group.quantile(0.25)
    axs[i].fill_between(x, q25, q75, alpha=0.2, color=colour_dct[var])

    axs[i].set_xlabel(time_col)
    axs[i].set_xticks([0, 6, 12, 18, 24])
    axs[i].set_title(var)
    axs[i].grid()

    i += 1

axs[0].set_ylabel(value_col)

plt.savefig(f'{OUTPUT_PATH} mean.png', dpi=300, format='png')
plt.show()


# 2. Annual average daily
group = df.groupby(by=[time_col])[value_col]

x = temp[time_col].unique()

mean = group.mean()
plt.plot(x, mean, color='tab:blue')

q90 = group.quantile(0.9)
q10 = group.quantile(0.1)
plt.fill_between(x, q10, q90, alpha=0.2, color='dimgrey')

plt.ylabel(value_col)
plt.xlabel(time_col)
plt.xticks([0, 6, 12, 18, 24])
plt.grid()
plt.tight_layout
plt.title('Average daily load (2015-2021)')

fig_path = OUTPUT_PATH + 'Daily average annual.png'
plt.savefig(fig_path, dpi=300, format='png')
plt.show()

# 3. Daily average load by season and weekday with timeslice imposed
var_col = 'Season weekday'
vars = ['Winter Working day', 'Winter Weekend',
    'Spring Working day', 'Spring Weekend',
    'Summer Working day', 'Summer Weekend',
    'Autumn Working day', 'Autumn Weekend'
]
fig, axs = plt.subplots(2, 4, sharey=True, sharex=True, figsize=(10,5))

i = 0
for var in vars:
    temp = df[df[var_col]==var]
    group = temp.groupby(by=[time_col])[value_col]

    x = temp[time_col].unique()
    axes = axs[i%2, i//2]

    mean = group.mean()
    lbl = 'Mean' if i==0 else None
    axes.plot(x, mean, label=lbl, c='dimgrey')
    
    q75 = group.quantile(0.75)
    q25 = group.quantile(0.25)
    lbl = r'50% interval' if i==0 else None
    axes.fill_between(x, q25, q75, alpha=0.3, color='dimgrey', label=lbl)
    
    q95 = group.quantile(0.95)
    q05 = group.quantile(0.05)
    lbl = r'90% interval' if i==0 else None
    axes.fill_between(x, q05, q95, alpha=0.15, color='dimgrey', label=lbl)
    
    axes.set_xticks([0, 6, 12, 18, 24])
    axes.set_title(var[0] + var[1:].lower())
    axes.grid()
    
    i += 1

# There's a better way to do this, but this was faster VVVV

# WINTER WORKING DAY
axs[0,0].hlines(8724.72, 0, 7.5, color='tab:blue') # NIGHT
axs[0,0].hlines(8724.72, 19.5, 24, color='tab:blue')
axs[0,0].hlines(10291.27, 7.5, 8.5, color='tab:green') # DAY
axs[0,0].hlines(10291.27, 9.5, 19.5, color='tab:green')
axs[0,0].hlines(10543.49, 8.5, 9.5, color='tab:orange') # PEAK

# WINTER WEEKEND
axs[1,0].hlines(7512.47, 0, 7.5, color='tab:blue')
axs[1,0].hlines(7512.47, 19.5, 24, color='tab:blue')
axs[1,0].hlines(8607.61, 7.5, 10.5, color='tab:green')
axs[1,0].hlines(8607.61, 11.5, 19.5, color='tab:green')
axs[1,0].hlines(8989.28, 10.5, 11.5, color='tab:orange')


# SPRING WORKING DAY
axs[0,1].hlines(7656.91, 0, 7.5, color='tab:blue') # NIGHT
axs[0,1].hlines(7656.91, 19.5, 24, color='tab:blue')
axs[0,1].hlines(8919.02, 7.5, 8.5, color='tab:green') # DAY
axs[0,1].hlines(8919.02, 9.5, 19.5, color='tab:green')
axs[0,1].hlines(9266.34, 8.5, 9.5, color='tab:orange') # PEAK

# SPRING WEEKEND
axs[1,1].hlines(6580.08, 0, 7.5, color='tab:blue') # NIGHT
axs[1,1].hlines(6580.08, 19.5, 24, color='tab:blue')
axs[1,1].hlines(7374.75, 7.5, 10.5, color='tab:green') # DAY
axs[1,1].hlines(7374.75, 11.5, 19.5, color='tab:green')
axs[1,1].hlines(7846.18, 10.5, 11.5, color='tab:orange') # PEAK


# SUMMER WORKING DAY
axs[0,2].hlines(6873.75, 0, 7.5, color='tab:blue') # NIGHT
axs[0,2].hlines(6873.75, 19.5, 24, color='tab:blue')
axs[0,2].hlines(8334.82, 7.5, 11.5, color='tab:green') # DAY
axs[0,2].hlines(8334.82, 12.5, 19.5, color='tab:green')
axs[0,2].hlines(8751.55, 11.5, 12.5, color='tab:orange') # PEAK

# SUMMER WEEKEND
axs[1,2].hlines(5944.68, 0, 7.5, color='tab:blue') # NIGHT
axs[1,2].hlines(5944.68, 19.5, 24, color='tab:blue')
axs[1,2].hlines(6892.71, 7.5, 10.5, color='tab:green') # DAY
axs[1,2].hlines(6892.71, 11.5, 19.5, color='tab:green')
axs[1,2].hlines(7365.16, 10.5, 11.5, color='tab:orange') # PEAK

# AUTUMN WORKING DAY
axs[0,3].hlines(7687.38, 0, 7.5, color='tab:blue') # NIGHT
axs[0,3].hlines(7687.38, 19.5, 24, color='tab:blue')
axs[0,3].hlines(9182.52, 7.5, 8.5, color='tab:green') # DAY
axs[0,3].hlines(9182.52, 9.5, 19.5, color='tab:green')
axs[0,3].hlines(9462.33, 8.5, 9.5, color='tab:orange') # PEAK

# AUTUMN WEEKEND
axs[1,3].hlines(6611.25, 0, 7.5, color='tab:blue', label='Night') # NIGHT
axs[1,3].hlines(6611.25, 19.5, 24, color='tab:blue')
axs[1,3].hlines(7636.36, 7.5, 10.5, color='tab:green', label='Day') # DAY
axs[1,3].hlines(7636.36, 11.5, 19.5, color='tab:green')
axs[1,3].hlines(8092.35, 10.5, 11.5, color='tab:orange', label='Peak') # PEAK

axs[0,0].set_ylabel(value_col)
axs[1,0].set_ylabel(value_col)
axs[1,0].set_xlabel(time_col)
axs[1,1].set_xlabel(time_col)
axs[1,2].set_xlabel(time_col)
axs[1,3].set_xlabel(time_col)
fig.subplots_adjust(right=0.84)
fig.legend(loc='right')
fig_path = OUTPUT_PATH + 'Seasonal weekday with daynite.png'

plt.savefig(fig_path, dpi=300, format='png')
plt.show()

#4. Annual graph with twenty-five rolling average
#https://towardsdatascience.com/moving-averages-in-python-16170e20f6c

df2021 = df[df['Year']==2021]

column = 'Load [MW]'
series = df2021[column]
wndw = 24*25 # Twenty five days
series_avg = series.rolling(window=wndw).mean()

col = column.replace(' [MW]', '').lower()
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(series, label=f'Hourly {col}', alpha=0.2, color='dimgrey')
ax.plot(series_avg, label=f'{int(wndw/24)}-day average {col}', color='tab:blue')
ax.set_ylabel(column)
ax.set_xticks([52608, 54768,56952,59160])
ax.set_xticklabels(['1 January', '1 April', '1 July','1 October'])
ax.set_title(f'Hourly and rolling average {col} (2021)')
plt.grid()
plt.tight_layout()
ax.legend()

fig_path = OUTPUT_PATH + 'Annual rolling average.png'
plt.savefig(fig_path, dpi=300, format='png')
plt.show()