import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


INPUT_PATH = "C:/Users/merlijn Kersten/Documents/UK/timeslices/data/combined 2015-2021.csv"
OUTPUT_PATH = "C:/Users/merlijn Kersten/Documents/UK/timeslices-outputs/"

df = pd.read_csv(INPUT_PATH)

df = df[df['Hour'] <= 23]

var_col = 'Season'
time_col = 'Hour'
value_col = 'Load [MW]'

vars = df[var_col].unique()

colour_dct = {
        'Spring' : 'limegreen',
        'Summer' : 'gold',
        'Autumn' : 'orangered',
        'Winter' : 'cornflowerblue',

        'Spring Working day' : '#33a02c', 
        'Spring Weekend' : '#b2df8a',
        'Summer Working day' : '#ff7f00',
        'Summer Weekend' : '#fdbf6f',
        'Autumn Working day' : '#e31a1c',
        'Autumn Weekend' : '#fb9a99',
        'Winter Working day' : '#1f78b4',
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
}

fig, axs = plt.subplots(1, 4, sharey=True, figsize=(10,5))
i = 0
for var in vars:
    temp = df[df[var_col]==var]
    group = temp.groupby(by=[time_col])[value_col]
    mean = group.mean()
    q75 = group.quantile(0.75)
    q25 = group.quantile(0.25)
    x = temp[time_col].unique()
    axes = axs[i]
    print(colour_dct[var])
    axs[i].plot(x, mean, label=var, c=colour_dct[var])
    axs[i].fill_between(x, q25, q75, alpha=0.2, color=colour_dct[var])

    axs[i].set_xticks([0, 6, 12, 18, 24])
    #axs[i].legend()
    axs[i].set_title(var)
    axs[i].set_xlabel(time_col)
    axs[i].grid()

    i += 1

axs[0].set_ylabel(value_col)

plt.tight_layout
plt.savefig(OUTPUT_PATH+'mean.png', dpi=300, format='png')
plt.show()


# ANNUAL PLOT
group = df.groupby(by=[time_col])[value_col]
mean = group.mean()
q90 = group.quantile(0.9)
q10 = group.quantile(0.1)
x = temp[time_col].unique()
plt.plot(x, mean)
plt.fill_between(x, q10, q90, alpha=0.2)
plt.xticks([0, 6, 12, 18, 24])
#axs[i].legend()
plt.title('Annual')
plt.xlabel(time_col)
plt.grid()
plt.ylabel(value_col)
plt.tight_layout
plt.savefig(OUTPUT_PATH+'annual.png', dpi=300, format='png')
plt.show()

var_col = 'Season weekday'
vars = ['Winter Working day',
'Winter Weekend',
'Spring Working day',
'Spring Weekend',
'Summer Working day',
'Summer Weekend',
'Autumn Working day',
'Autumn Weekend']
fig, axs = plt.subplots(2, 4, sharey=True, sharex=True, figsize=(10,5))

# WINTER WORKING DAY
axs[0,0].hlines(8714.58, 0, 7.5, color='tab:blue') # NIGHT
axs[0,0].hlines(8714.58, 19.5, 24, color='tab:blue')
axs[0,0].hlines(10284.11, 7.5, 8.5, color='tab:green') # DAY
axs[0,0].hlines(10284.11, 9.5, 19.5, color='tab:green')
axs[0,0].hlines(10535.77, 8.5, 9.5, color='tab:orange') # PEAK

# WINTER WEEKEND
axs[1,0].hlines(7515.47, 0, 7.5, color='tab:blue')
axs[1,0].hlines(7515.47, 19.5, 24, color='tab:blue')
axs[1,0].hlines(8613.91, 7.5, 10.5, color='tab:green')
axs[1,0].hlines(8613.91, 11.5, 19.5, color='tab:green')
axs[1,0].hlines(8993.77, 10.5, 11.5, color='tab:orange')


# SPRING WORKING DAY
axs[0,1].hlines(7656.91, 0, 7.5, color='tab:blue') # NIGHT
axs[0,1].hlines(7656.91, 19.5, 24, color='tab:blue')
axs[0,1].hlines(8919.02, 7.5, 8.5, color='tab:green') # DAY
axs[0,1].hlines(8919.02, 9.5, 19.5, color='tab:green')
axs[0,1].hlines(9266.34, 8.5, 9.5, color='tab:orange') # PEAK

# SPRING WEEKEND
axs[1,1].hlines(6582.89, 0, 7.5, color='tab:blue') # NIGHT
axs[1,1].hlines(6582.89, 19.5, 24, color='tab:blue')
axs[1,1].hlines(7374.75, 7.5, 10.5, color='tab:green') # DAY
axs[1,1].hlines(7374.75, 11.5, 19.5, color='tab:green')
axs[1,1].hlines(7846.18, 10.5, 11.5, color='tab:orange') # PEAK


# SUMMER WORKING DAY
axs[0,2].hlines(6873.75, 0, 7.5, color='tab:blue') # NIGHT
axs[0,2].hlines(6873.75, 19.5, 24, color='tab:blue')
axs[0,2].hlines(8334.82, 7.5, 10.5, color='tab:green') # DAY
axs[0,2].hlines(8334.82, 11.5, 19.5, color='tab:green')
axs[0,2].hlines(8751.55, 10.5, 11.5, color='tab:orange') # PEAK

# SUMMER WEEKEND
axs[1,2].hlines(5944.68, 0, 7.5, color='tab:blue') # NIGHT
axs[1,2].hlines(5944.68, 19.5, 24, color='tab:blue')
axs[1,2].hlines(6892.71, 7.5, 11.5, color='tab:green') # DAY
axs[1,2].hlines(6892.71, 12.5, 19.5, color='tab:green')
axs[1,2].hlines(7365.16, 11.5, 12.5, color='tab:orange') # PEAK

# AUTUMN WORKING DAY
axs[0,3].hlines(7687.38, 0, 7.5, color='tab:blue') # NIGHT
axs[0,3].hlines(7687.38, 19.5, 24, color='tab:blue')
axs[0,3].hlines(9182.52, 7.5, 10.5, color='tab:green') # DAY
axs[0,3].hlines(9182.52, 11.5, 19.5, color='tab:green')
axs[0,3].hlines(9462.33, 10.5, 11.5, color='tab:orange') # PEAK

# AUTUMN WEEKEND
axs[1,3].hlines(6617.86, 0, 7.5, color='tab:blue', label='Night') # NIGHT
axs[1,3].hlines(6617.86, 19.5, 24, color='tab:blue')
axs[1,3].hlines(7636.36, 7.5, 8.5, color='tab:green', label='Day') # DAY
axs[1,3].hlines(7636.36, 9.5, 19.5, color='tab:green')
axs[1,3].hlines(8092.35, 8.5, 9.5, color='tab:orange', label='Peak') # PEAK

i = 0
for var in vars:
    temp = df[df[var_col]==var]
    group = temp.groupby(by=[time_col])[value_col]
    mean = group.mean()
    q75 = group.quantile(0.75)
    q25 = group.quantile(0.25)
    x = temp[time_col].unique()
    axes = axs[i%2, i//2]
    print(colour_dct[var])
    lbl = 'Mean' if i==0 else None
    axes.plot(x, mean, label=lbl, c='dimgrey')
    lbl = r'50% interval' if i==0 else None
    axes.fill_between(x, q25, q75, alpha=0.2, color='dimgrey', label=lbl)

    axes.set_xticks([0, 6, 12, 18, 24])
    #axs[i].legend()
    axes.set_title(var)
    axes.grid()

    i += 1

axs[0,0].set_ylabel(value_col)
axs[1,0].set_ylabel(value_col)
axs[1,0].set_xlabel(time_col)
axs[1,1].set_xlabel(time_col)
axs[1,2].set_xlabel(time_col)
axs[1,3].set_xlabel(time_col)
fig.subplots_adjust(right=0.84)
fig.legend(loc='right')

plt.tight_layout
plt.savefig(OUTPUT_PATH+'swd+mean.png', dpi=300, format='png')
plt.show()
