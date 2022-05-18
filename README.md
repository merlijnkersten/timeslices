# timeslice_analysis

*March-April 2022, merlijn*

To analyse energy data time series by time slice using load/price/etc duration profiles.

For version 0.2:

| Script                     | Function                                                                             | Branch |
| -------------------------- | ------------------------------------------------------------------------------------ | ------ |
| `load.py`                  | these functions are used to import and clean the data                                | all    |
| `assign.py`                | this script contains functions that assign the various timeslices to the time series | all    |
| `analyse.py`               | these functions generate visualisations and statistics,                              | all    |
| `report_visualisations.py` | quick script to create visualisations for the report                                 | all    |

# Documentation timeslice analysis

[toc]

## Introduction

TIMES uses timeslices to represent temporal <variability> in variables.  The current version of the TIMES-CZ model uses twelve timeslices: four seasonal timeslices (spring, summer, autumn, winter) and three daynite timeslices (night, day, peak), see tables <x>, <x> and <x>. Increasing the number of timeslices increases the accuracy of the model, as there are annual variations in the data that have a different frequency than the daily and seasonal variations that are currently captured by the timeslices.

Milan and Lukáš suggested some alternative timeslices (see Method). The basic idea is to test different types of timeslices on load, export, import and price data to see which combination of timeslices we can use to enrich the TIMES-CZ model. In order to do this, I wrotea suite of functions that can test different timeslices, in order to determine which combination of timeslices would best enrich the model.

When picking a combination of timeslices, the primary concerns are whether they capture intra/inter-annual variability in the data and thus accurately convey major trends, and the computational and data-gathering cost and of this increased accuracy. Generally speaking, as time resolution increases, the accuracy of the model increases too but so does its computational complexity. Furthermore, it becomes more difficult to gather economic statistics at the same resolution, which reduced the efficacy of the increase timeslice resolution. The data considered in this report (load, consumption, import, export, prices) can be known to a high temporal precision, whereas others (such as production of specific factories, or solar output) can either not be known at such a high temporal resolution or have large intra (<inter?>) year variability. The goal of this report is to contribute to finding the right trade off between temporal resolution and computational and statistical complexity.



| Code | Season | Length (days) | Description           |
| ---- | ------ | ------------- | --------------------- |
| R    | Spring | 78            | 15 March-31 May       |
| S    | Summer | 91            | 1 June-30 August      |
| F    | Autumn | 77            | 31 August-15 November |
| W    | Winter | 119           | 16 November-14 March  |

Table <x>: Definition of the seasonal timeslices.

| Code | Daynite | Length (hours) | Description                                          |
| ---- | ------- | -------------- | ---------------------------------------------------- |
| N    | Night   | 12             | all hours between 20:00-08:00.                       |
| P    | Peak    | 1              | the hour with the highest load during the day.       |
| D    | Day     | 11             | all hours between 08:00-20:00, except the peak hour. |

Table <x>: Definition of the daynite timeslices.

| Season     | Daynite   | TS   | Annual share (%) |
| ---------- | --------- | ---- | ---------------- |
| Spring (R) | Night (N) | RN   | 10.7             |
|            | Day (D)   | RD   | 9.80             |
|            | Peak (P)  | RP   | 0.980            |
| Summer (S) | Night (N) | SN   | 12.5             |
|            | Day (D)   | SD   | 11.4             |
|            | Peak (P)  | PD   | 1.04             |
| Fall (F)   | Night (N) | FN   | 10.5             |
|            | Day (D)   | FD   | 9.67             |
|            | Peak (P)  | FP   | 0.879            |
| Winter (W) | Night (N) | WN   | 16.3             |
|            | Day (D)   | WD   | 14.9             |
|            | Peak (P)  | WP   | 1.36             |

Table <x>: Annual share of the current timeslices.


## Method

The following data sources were used:

| Data                | Source                                                   | Scope                              |
| ------------------- | -------------------------------------------------------- | ---------------------------------- |
| Load                | https://www.ceps.cz/en/all-data#Load                     | 2015-2021, hourly average values.  |
| Generation          | https://www.ceps.cz/en/all-data#Generation               | 2015-2021, hourly average values.  |
| Prices              | https://www.ote-cr.cz/en/statistics/yearly-market-report | 2015-2021, hourly day-ahead price. |
| Imports and exports | https://www.ceps.cz/en/all-data#CrossborderPowerFlows    | 2015-2021, hourly average values.  |

Table <x>: Data sources used in this report.

2015 is the base year of the TIMES-CZ model, and 2020 is an <x?> year; 2021 is the last year for which full data is available. 

From these columns, total generation, total import, total export, and net export were calculated. The data sources were combined into a single data file, which can be found in the GitHub repository (see Appendix).

The load, import, export and price data was then categorised into the two original time slices (season daynite) and six new timeslices:

1. Month: the month of the date (January, February, ..., December),
2. Weekday 1: whether the date was a working day (generally, Monday-Friday) or a weekend or public holiday (generally, Saturday-Sunday),
3. Weekday 2: the day of the week (Monday, Tuesday, etc),
4. Extended daynite 1: one night time slices, three day time slices. See table <x> for the chosen cut-off times.
5. Extended daynite 2: two night time slices, six day time slices. See table <x> for the chosen cut-off times.
6. Hour: hourly timeslices (00:00, 01:00, ...,, 23:00).

*Note: The code was written so as to readily accept new timeslices, please see the Appendix for more information.*

These timeslices were then combined to into groups .

| Name | Group                                   | Size            |
| ---- | --------------------------------------- | --------------- |
| Null | Season - daynite                        | 4 * 3 = 12      |
| A    | Season - extended daynite 1             | 4 * 4 = 16      |
| B    | Season - extended daynite 2             | 4 * 8 = 24      |
| C    | Season - hour                           | 4 * 24 = 96     |
| D    | Season - weekday 1 - daynite            | 4 * 2 * 3 = 24  |
| E    | Season - weekday 1 - extended daynite 1 | 4 * 2 * 4 = 32  |
| F    | Season - weekday 2                      | 4 * 7 = 28      |
| G    | Season - weekday 2 - daynite            | 4 * 7 * 3 = 84  |
| H    | Month - daynite                         | 12 * 3 = 36     |
| I    | Month - extended daynite 1              | 12 * 4 = 48     |
| J    | Month - extended daynite 2              | 12 * 8 = 96     |
| K    | Month - weekday 1                       | 12 * 2 = 24     |
| L    | Month - weekday 1 - daynite             | 12 * 2 * 3 = 72 |
| M    | Month - hour                            | 12 * 24 = 288   |

Table <x>: The different timeslice groupings considered in this report. The _Null_ group is the current timeslices group used in the TIMES-CZ model.

These combinations of timeslices were then plotted for load, import, export, and price time series and their key statistics (mean, standard deviation, percentiles) were recorded. 

*Note: when the sample size is large enough, for most time slices and metrics, the time series are approximately normal.*

| Extended daynite 2 | Description |
| ------------------ | ----------- |
| Night-1            | 20:00-01:00 |
| Night-2            | 02:00-07:00 |
| Day-1              | 08:00-09:00 |
| Day-2              | 10:00-11:00 |
| Day-3              | 12:00-13:00 |
| Day-4              | 14:00-15:00 |
| Day-5              | 16:00-17:00 |
| Day-5              | 18:00-19:00 |

Table <x>: Definition of the extended daynite 2 timeslices.

| Extended daynite 1 | Description |
| ------------------ | ----------- |
| Night              | 20:00-05:00 |
| Morning            | 06:00-09:00 |
| Afternoon          | 10:00-15:00 |
| Evening            | 16:00-19:00 |

Table <x>: Definition of the extended daynite 1 timeslices.

| Code | Weekday     | Length | Description                                             |
| ---- | ----------- | ------ | ------------------------------------------------------- |
| L    | Working day | 68.7%  | Any working day (most weeks: Monday to Friday).         |
| H    | Weekend day | 31.3%  | Weekend days (Saturday and Sunday) and public holidays. |

Table <x>: Definition of the weekday timeslices. The length of the timeslices, expressed as an annual percentage, is calculated over 2015-2021 but can vary year-to-year due to differences of the date of public holidays. Note that the length of the working day/weekend day slices is not exactly 5/7 and 2/7 (71.4% and 28.6%), respectively, due to the inclusion of public holidays as weekend days. 

When analysing the statistics for the different groups of timeslices, the main focus was to determine whether these timeslices accurately captured the major periodic trends in the data, and <expand>

### Fast Fourier transform

To aid the graphical analysis of the data, I performed a Fourier transforms of the load, import, export, and price data (using the fast Fourier transform algorithm). This decomposes the time series into temporal frequencies, allowing you to see which frequencies (and thus processes) dominate the time series.

### Distribution analysis

To determine whether different timeslice groupings yielded similar results, I also looked at the distribution of data points within timeslices. I did this by plotting the major statistics (mean, standard deviation, major percentiles) and seeing to what extent different timeslices presented a 'unique' view of the data and to what extent the mean value was representative of that timeslice (i.e. whether there was excessively large variance about the mean). <rephrase>

## Results

<img annual with rolling average>
Figure <x>: This figure shows the hourly load in 2021 (shaded grey) as well as the 20-day rolling average (blue). This shows how one of the main frequencies driving the load is the annual (as well as daily) variance.

<img average daily>
Figure <x>: This data shows the average daily load from 2015-2021 (blue) as well the 25%-75% percentile range (shaded blue)

<img average daily by season>
Figure <x>: Same data as in figure <x-1> but now split by season (see table <x>), to give an idea how the different timeslices affect the distribution of the data.

<img FFT>
Figure <x>: This figure shows the results of the fast Fourier transform analysis for each variable. On the left, it shows the twenty dominant frequencies lower than 30 days, on the right it shows the twenty dominant frequencies higher than 30 days. 

<img distribution>

Fig <x>: This figure shows an example of the distribution graphs, in this case for group <expand>.

## Conclusion and discussion

My recommendation is that we add a weekday (working day (L)/weekend day (H)) timeslice to the model. This timeslice enriches the data as it allows us to capture weekly variance in the data, without adding much computational complexity or complicating data gathering. Figure <x> shows that the load, export, and import values have a strong weekly and intraweekly (7 days and 3.5 days) frequencies, but these are currently not captured in the daynite and season timeslices. Using a seven-day weekday timeslice increases computational costs ($$4*7*3 = 84$$ vs $4*2*3=24$) without increasing accuracy and is therefore not recommended. 

I suggest using the abbreviation 'L' for working days (**l**abour) and 'H' for weekend days (**h**oliday). Using these conventions, the new timeslices and their annual share are:  

<img average daily by season and weekday with timeslice averages>

Figure <x>: Daily load, by season and weekday, with average timeslice values superimposed. 

| Season     | Weekday         | Daynite   | TS   | Annual share (%) |
| ---------- | --------------- | --------- | ---- | ---------------- |
| Spring (R) | Working day (L) | Night (N) | RLN  | 7.28             |
|            |                 | Day (D)   | RLD  | 6.67             |
|            |                 | Peak (P)  | RLP  | 0.607            |
|            | Weekend day (H) | Night (N) | RHN  | 3.50             |
|            |                 | Day (D)   | RHD  | 3.23             |
|            |                 | Peak (P)  | RHP  | 0.293            |
| Summer (S) | Working day (L) | Night (N) | SLN  | 8.78             |
|            |                 | Day (D)   | SLD  | 8.05             |
|            |                 | Peak (P)  | SLP  | 0.732            |
|            | Weekend day (H) | Night (N) | SHN  | 3.28             |
|            |                 | Day (D)   | SHD  | 3.50             |
|            |                 | Peak (P)  | SHP  | 0.318            |
| Fall (F)   | Working day (L) | Night (N) | FLN  | 7.40             |
|            |                 | Day (D)   | FLD  | 6.78             |
|            |                 | Peak (P)  | FLP  | 0.617            |
|            | Weekend day (H) | Night (N) | FHN  | 3.34             |
|            |                 | Day (D)   | FHD  | 2.99             |
|            |                 | Peak (P)  | FHP  | 0.272            |
| Winter (W) | Working day (L) | Night (N) | WLN  | 10.9             |
|            |                 | Day (D)   | WLD  | 9.97             |
|            |                 | Peak (P)  | WLP  | 0.907            |
|            | Weekend day (H) | Night (N) | WHN  | 5.02             |
|            |                 | Day (D)   | WHD  | 4.61             |
|            |                 | Peak (P)  | WHP  | 0.419            |

Table <x>: Annual share of the new proposed timeslices.

In general, any group including monthly, weekday 2 (seven weekdays) or hourly timeslices greatly increased computational complexity without adding much detail to the model, as many months and hours had similar load, cross border exchanges, and prices. This is largely because these timeslices do not attempt to categorise the data (as the current daynite timeslice does) but rather focus on increasing accuracy by increasing the number of timeslices. Something similar is true groups including weekday 2. These approaches also suffer from the need to know other statistics at a much higher resolution in order to be useful,  which limits their usefulness in increasing accuracy. Monthly timeslices showed a lot of repetition-it did not really capture more of the yearly variability than the seasonal timeslices, whilst many months had nearly identical average imports, exports and loads (e.g. July and August, June and September, etc). To some extent, this is also true for the Spring and Autumn seasonal timeslices: perhaps these could be merged and omitted.

The data used covers seven years, which should give a good understanding of annual trends in load, export, and import values. However, capturing price developments is more difficult as these are not necessarily periodic, and can see periods of high volatility that are not periodic. There can be such deviations in the other variables too, but due to the long timespan and periodicity these changes are smoothed out. For instance, imports and exports in 2015 were up by 17.2% and 24.5%, respectively, compared to 2016-2021, but by using all seven years these annual deviations are smoothed out.

### Future development

The best way to test the effect of new timeslices is to add them to the TIMES-CZ model. This is quite a labour intensive process, as other statistics also need to be updated. Some of this could be automated (using the data available, new scenario files for processes like EXPELCHIGGA and IMPELCHIGA could  be generated) but it would still require careful setting up of the relevant script, running the model, and analysing the model outputs.

This has not been fully done yet for the proposed season - weekday - daynite group of timeslices, and thus further work is needed to explore the exact impacts on the model of using this new group. Currently, on the EUA-revision branch, I have added a new scenario file CHECK NAME AT OFFICE which incorporates the seaon - weekday - daynite group with a corresponding CHECK NAME AT OFFICE scenario file which replaces CHECK NAME AT OFFICE.

As mentioned previously, many other timeslices remain unexplored. The data gathered suggests that perhaps the spring and autumn seasonal timeslices could be merged, as for some data points they show very similar means and distributions. Alternatively, they could be split and merged; creating an early-Spring/late-Autumn timeslice (capturing the onset/end of Winter) and an late-Spring/early-Autumn timeslice (capturing the onset/end of Summer). Furthermore, the current daynite timeslices could be expanded. The current definition of 'Night' lasting 12-hours appears to be too broad as the reduced demand does not last for so long, perhaps an alternative to the exenteded daynite timeslices discussed in this report. One could envision the following timeslice:

| Extended daynite 3 | Description                               | Lenght (h) |
| ------------------ | ----------------------------------------- | ---------- |
| Night              | 23:00-05:00                               | 6          |
| Morning            | 06:00-08:00                               | 3          |
| Day                | 08:00-20:00, except:                      | 11         |
| Peak               | The hour with the highest load during Day | 1          |
| Evening            | 20:00-22:00                               | 3          |

Lastly, this report only considered electricity production and consumption. Other commodities (most notably natural gas) and consumer behaviour patterns are also of interest. Due to the general nature of the code (see Appendix), analyising these should be relatively straightforward. 

## Appendix

All of the code used to import, analyse, and visualise the data in this report can be found on [GitHub](https://github.com/merlijnk/timeslices). There are two versions of the code: version 0.1 consists of some initial scripts used to create simple load duration graphs, whereas version 0.2 is a more fully-fledged suite of scripts that contain more generalised functions. Version 0.2 was used in this report. The basic structure is as follows:

1. `load.py`: these functions are used to import and clean the data,
2. `assign.py`: this script contains functions that assign the various timeslices to the time series,
3. `analyse.py`: these functions generate visualisations and statistics,

All these functions can be run from the `main.py` file or individually in their respective scripts. The idea behind organising the functions and scripts like this is to make it easier to maintain and extend the functions. To this end, most functions are written in a very generalised manner, which should make it easy to add support for additional timeslices, time series, and other improvements. An important factor here is that the functions are (generally) agnostic to the timeslice or time series used, which means that it is straightforward to add new timeslices (such as the ones mentioned in the discussion) or to use the current functions to analyse new time series.   