# Documentation timeslice analysis

_merlijn, April-May 2022_

Table of contents
- Introduction
  - Original time slices
  - Potential new timeslices
  - 
  
- Method
  - Data sources
  - Data cleaning
  - Data transformation
  - Analysis types
    - FFT
	- 
	
- Results
  - Graphs with TS overlayed
  - Year fractions
  - 
  
- Conclusion

- Appendix
  - guide to code (inc. versions)
  

# Introduction

<add some academic background, use Sven's thesis>

TIMES uses timeslices to represent temporal variability in variables.  The current version of the TIMES-CZ model uses twelve timeslices: four seasonal timeslices (spring, summer, autumn, winter) and three daynite timeslices (night, day, peak). Increasing the number of timeslices increases the accuracy of the model, as there are annual variations in the data that have a different frequency than seasonal/daily <rephrase>. 

Milan and Lukáš suggested some alternative timeslices. The basic idea is to test different types of timeslices on load, export, import and price data to see which timeslices we can use to enrich the TIMES-CZ model. 

<idea is to test out different timeslices>

When picking a combination of timeslices, the primary concerns are whether they capture annual variability in the data and thus accurately convey major trends, and the computational cost and <can you get the data> of this increased accuracy. Generally speaking, as time resolution increases, the accuracy of the model increases too but so does its computational complexity. Furthermore, it becomes more difficult to gather economic data and statistics at the same resolution. The data considered in this report (load, consumption, import, export, prices) can be known to a high temporal preciesion, whereas others (such as production of specific factories, or solar output) can either not be known at such a high temporal resolution or have large intra (<inter?>) year variability. The goal of this report is to contribute to finding the right trade off between temporal resolution and computational and statistical complexity.



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


# Method

The following data sources were used:

| Data                | Source                                                   | Scope                              |
| ------------------- | -------------------------------------------------------- | ---------------------------------- |
| Load                | https://www.ceps.cz/en/all-data#Load                     | 2015-2021, hourly average values.  |
| Generation          | https://www.ceps.cz/en/all-data#Generation               | 2015-2021, hourly average values.  |
| Prices              | https://www.ote-cr.cz/en/statistics/yearly-market-report | 2015-2021, hourly day-ahead price. |
| Imports and exports | https://www.ceps.cz/en/all-data#CrossborderPowerFlows    | 2015-2021, hourly average values.  |

Table <x>: Data sources used in this report.

2015 is the base year of the TIMES-CZ model, and 2020 is an <x?> year; 2021 is the last year for which full data is available. 



From these columns, total generation, total import, total export, and net export were calculated. The data sources were combined into a single data file, which can be found in the Github repository [<insert link>](link).

The load, import, export and price data was then categorised into the two original time slices (seasonm daynite) and <x> distinct new timeslices:

1. Month: the month of the date,
2. Weekday 1: whether the date was a working day (generally, Monday-Friday) or a weekend or public holiday (generally, Saturday-Sunday),
3. Weekday 2: the day of the week (Monday, Tuesday, etc),
4. Extended daynite 1: one night time slices, three day time slices. See table <x> for the chosen cut-off times.
5. Extended daynite 2: two night time slices, six day time slices. See table <x> for the chosen cut-off times.
6. Hour: hourly timeslices.

*Note: The code was written so as to readily accept new timeslices, please see the Appendix <X> for more information.*

<to discussion> The hourly and monthly capture the greatest amount of detail, but also increase the complexity of the model greatly. 

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

| Code | Weekday     | Description                                             |
| ---- | ----------- | ------------------------------------------------------- |
| L    | Working day | Any working day (most weeks: Monday to Friday).         |
| H    | Weekend     | Weekend days (Saturday and Sunday) and public holidays. |

Table <x>: Definition of the weekday timeslices.


When analysing the statistics for the different groups of timeslices, the main focus was to determine whether these timeslices accurately captured the major periodic trends in the data, and 

## Fast Fourier transform

To aid the visual analysis of the data, I performed a Fourier transforms of the load, import, export, and price data (using the fast Fourier transform algorithm). This decomposes the time series into temporal frequencies, allowing you to see which frequency (and thus processes) dominate the time series.

## Distribution analysis
A second graphical approach 

# Results

<img annual with rolling average>
Figure <x>: This figure shows the hourly load in 2021 (shaded grey) as well as the 20-day rolling average (blue). This shows how one of the main frequencies driving the load is the annual (as well as daily) variance.

<img average daily>
Figure <x>: This data shows the average daily load from 2015-2021 (blue) as well the 25%-75% percentile range (shaded blue)

<img average daily by season>
Figure <x>: Same data as in figure <x-1> but now split by season (see table <x>), to give an idea how the different timeslices affect the distribution of the data.

<img FFT>
Figure <x>: This figure shows the results of the fast Fourier transform analysis for each variable. On the left, it shows the twenty dominant frequencies lower than 30 days, on the right it shows the twenty dominant frequencies higher than 30 days. 

<img distribution>

# Discussion

<discussion: 2015 saw high imports and exports compared to the other years: exports and imports were 17.2% and 24.5% higher, respectively, than in 2016-2021.>

<discussion: prices periodicity>

<img average daily by season and weekday with timeslice averages>

Figure <x>: Daily load, by season and weekday, with average timeslice values superimposed. 

Monthly timeslices showed a lot of repetition-it did not really capture more of the yearly variability than the seasonal timeslices, whilst many months had nearly identical average imports, exports and loads (e.g. July and August, June and September, etc). To some extent, this is also true for the Spring and Autumn seasonal timeslices: perhaps these could be merged and omitted.

<insert distribution-time slice overlay>

| Season     | Weekday         | Daynite   | TS  | Annual share (%) |
| ---------- | --------------- | --------- | --- | ---------------- |
| Spring (R) | Working day (L) | Night (N) | RLN | 7.28             |
|            |                 | Day (D)   | RLD | 6.67             |
|            |                 | Peak (P)  | RLP | 0.607            |
|            | Weekend day (H) | Night (N) | RHN | 3.50             |
|            |                 | Day (D)   | RHD | 3.23             |
|            |                 | Peak (P)  | RHP | 0.293            |
| Summer (S) | Working day (L) | Night (N) | SLN | 8.78             |
|            |                 | Day (D)   | SLD | 8.05             |
|            |                 | Peak (P)  | SLP | 0.732            |
|            | Weekend day (H) | Night (N) | SHN | 3.28             |
|            |                 | Day (D)   | SHD | 3.50             |
|            |                 | Peak (P)  | SHP | 0.318            |
| Fall (F)   | Working day (L) | Night (N) | FLN | 7.40             |
|            |                 | Day (D)   | FLD | 6.78             |
|            |                 | Peak (P)  | FLP | 0.617            |
|            | Weekend day (H) | Night (N) | FHN | 3.34             |
|            |                 | Day (D)   | FHD | 2.99             |
|            |                 | Peak (P)  | FHP | 0.272            |
| Winter (W) | Working day (L) | Night (N) | WLN | 10.9             |
|            |                 | Day (D)   | WLD | 9.97             |
|            |                 | Peak (P)  | WLP | 0.907            |
|            | Weekend day (H) | Night (N) | WHN | 5.02             |
|            |                 | Day (D)   | WHD | 4.61             |
|            |                 | Peak (P)  | WHP | 0.419            |

Table <x>: Annual share of the new proposed timeslices.

## Future ideas

* Actually apply timeslices to model to see results,
* Other, different timeslices?
* Change daynite timeslots: 20-8 for night might be too long? Data suggests 22-6?



# Appendix

All of the code used to import, analyse, and visualise the data in this report can be found on [Github](https://github.com/merlijnk/timeslices). There are two versions of the code: version 0.1 consists of some initial scripts used to create simple load duration graphs, whereas version 0.1 is a more fully-fledged suite of scripts that contain more generalised functions. The basic structure is as follows:

1. `load.py`: these functions are used to import and clean the data,
2. `assign.py`: this script contains functions that assign the various timeslices to the time series,
3. `analyse.py`: these functions generate visualisations and statistics,

All these functions can be run from the `main.py` file or individually in their respective scripts. The idea behind organising the functions and scripts like this is to make it easier to maintain and extend the functions. To this end, most functions are written in a very generalised manner, which should make it easy to add support for additional timeslices, variables, and other improvements.

