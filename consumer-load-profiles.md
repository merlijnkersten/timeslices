# Consumer load profiles

_May 2022, merlijn_

[Data source](https://www.ote-cr.cz/en/statistics/electricity-load-profiles/normalized-lp?date=2015-05-24)

| Column        | Frequency 1 | Frequency 2 | Frequency 3 | Frequency 4 |
| ------------- | ----------- | ----------- | ----------- | ----------- |
| tdd1          | 24h         | 7d          | 365d        | 12h         |
| tdd2          | 24h         | 365d        | 7d          | 21h         |
| tdd3          | 365d        | 24h         | 183d        | 7d          |
| tdd4          | 24h         | 12h         | 365d        | 8h          |
| tdd5-jižní    | 24h         | 365d        | 12h         | 8h          |
| tdd5-praha    | 365d        | 12h         | 6h          | 24h         |
| tdd5-severní  | 24h         | 12h         | 365d        | 8h          |
| tdd5-střední  | 365d        | 12h         | 24h         | 7d          |
| ttd5-východní | 12h         | 365d        | 24h         | 7d          |
| ttd5-západní  | 24h         | 8h          | 365d        | 12h         |
| tdd6          | 365d        | 24h         | 12h         | 8h          |
| tdd7          | 365d        | 24h         | 12h         | 183d        |
| tdd8          | 24h         | 365d        | 12h         | 8h          |

* Daily frequencies much more prominent,
* Absence of half/quarter/etc year frequencies etc 
* Week weakly frequencies
* Much less spread in frequencies (stronger dominant frequencies)

| Column        | Frequency 1 | Frequency 2 | Frequency 3 | Frequency 4 |
| ------------- | ----------- | ----------- | ----------- | ----------- |
| tdd1          | Day         | Week        | Year        | Day         |
| tdd2          | Day         | Year        | Week        | Day         |
| tdd3          | Year        | Day         | Year        | Week        |
| tdd4          | Day         | Day         | Year        | Day         |
| tdd5-jižní    | Day         | Year        | Day         | Day         |
| tdd5-praha    | Year        | Day         | Day         | Day         |
| tdd5-severní  | Day         | Day         | Year        | Day         |
| tdd5-střední  | Year        | Day         | Day         | Day         |
| ttd5-východní | Day         | Year        | Day         | Week        |
| ttd5-západní  | Day         | Day         | Year        | Day         |
| tdd6          | Year        | Day         | Day         | Day         |
| tdd7          | Year        | Day         | Day         | Year        |
| tdd8          | Day         | Year        | Day         | Day         |


* category C = commercial/industry
* category D = households

* 1, 4 no electricity for heat or hot water
* 2 - heat accumulation (hot water or heating), there is also another source of heat
* 5 -   heat accumulation (usually hot water)
* 6 -   electricity for heating, but there is also another source of heat
* 3, 7 electricity for heating - including heat pumps
* 8 public lightening

[Czech explanation](https://www.eru.cz/sites/default/files/upload/Priloha_4_541.pdf)




| #    | Category    | Description                                                  |
| ---- | ----------- | ------------------------------------------------------------ |
| 1    | Commercial  | No electricity for heat or hot water                         |
| 2    | Commercial  | Heat accumulation (hot water & heating, includes another source of heat) |
| 3    | Commercial  | Electricity for heating including heat pumps                 |
| 4    | Residential | No electricity for heat or hot water                         |
| 5    | Residential | Heat accumulation (usually, hot water)                       |
| 6    | Residential | Electricity for heating (includes another source of heat)    |
| 7    | Residential | Electricity for heating including heat pumps                 |
| 8    | Commercial  | Public lighting                                              |


Original processes that Lukáš showed me:

| Abbreviation | Description                     | #        |
| ------------ | ------------------------------- | -------- |
| CLIG         | Commercial lighting             | #1?      |
| CCOK         | Commercial cooking              | #1?      |
| CREF         | Commercial refrigeration        | #1?      |
| CPLI         | Commercial public lighting      | #8       |
| COEL         | Commercial other electricity    | #1+#2+#3 |
| COEN         | Commercial other energy generic | #1+#2+#3 |

Additional processes found in the COM_?? tag:

| Abbreviation | Description                                             | #        |
| ------------ | ------------------------------------------------------- | -------- |
| CCLE         | Commercial space cooling large existing                 | #2?+#3?  |
| CCSE         | Commercial space cooling small existing                 | #2?+#3?  |
| CHLE         | Commercial space heating large                          | #2+#3    |
| CHSE         | Commercial space heating small                          | #2+#3    |
| CWLE         | Commercial water heating large existing                 | #2+#3    |
| CWSE         | Commercial water heating small existing                 | #2+#3    |
| RHDE         | Residential space heating single semi-detached existing | #5+#6    |
| RHRE         | Residential space heating single rural existing         | #5+#6    |
| RHRN         | Residential space heating single rural new              | #5+#6    |
| RHUN         | Residential space heating single urban new              | #5+#6    |
| RHME         | Residential space heating multiple all existing         | #5+#6    |
| RHMN         | Residential space heating multiple all existing new     | #5+#6    |
| RCDE         | Residential space cooling single detached existing      | #5+#6    |
| RCRE         | Residential space cooling single rural existing         | #5?+#6   |
| RCRN         | Residential space cooling single rural new              | #5?+#6   |
| RCME         | Residential space cooling multiple all existing         | #5?+#6?  |
| RCMN         | Residential space cooling multiple all new              | #5?+#6?  |
| RWUN         | Residential water heating single urban new              | #5+#6    |
| RWDE         | Residential water heating single urban existing         | #5+#6    |
| RWRN         | Residential water heating single rural new              | #5+#6    |
| RWRE         | Residential water heating single rural existing         | #5+#6    |
| RWME         | Residential water heating multiple all existing         | #5+#6    |
| RWMN         | Residential water heating multiple all new              | #5+#6    |
| RCOK         | Residential cooking                                     | #4       |
| RCWA         | Residential clothes washing                             | #4       |
| RCDR         | Residential cloth drying                                | #5+#6    |
| RDWA         | Residential dish  washing                               | #4       |
| RLIG         | Residential lighting existing                           | #4       |
| RREF         | Residential refrigeration                               | #5?+#6?  |
| ROEL         | Residential other electricity                           | #4+#5+#6 |
| ROEN         | Residential other energy generic                        | #4+#5+#6 |


Remaining timeslice dependent COM_?? processes (I think we cannot use consumer load profiles to determine values):

| Abbreviation | Description             | #        |
| ------------ | ------------------------| -------- |
| TAV          | Aviation generic        | #        |
| TBI          | Road bus intercity      | #        |
| TBU          | Road bus urban          | #        |
| TC           | Road car short distance | #        |
| TFR          | Road freight            | #        |
| TMO          | Road motors             | #        |
| TNA          | Navigation generic      | #        |
| TTF          | Rail freight            | #        |
| TTL          | Rail passengers light   | #        |
| TTP          | Rail passengers heavy   | #        |
| IFT          | Food and tobacco demand | #        |
| IOI          | Other industries demand | #        |

Relevant document `CZ_V02-\VT_CZ_TRA_V2.2.xlsx`

How to combine multiple consumer load patterns?

* Take a weighted average (how to determine weights),
  * Take regular average (or, set weights equal if they are unknown),
* Add them (not weighing them),



* Need to know definitions of load profiles & commodities better to know which combinations produce valid results,
* Why is commercial - public lighting not zero during the day? In baseline/current scenario,
* Would it be better to generate the scenario file (the table in question) automatically?



* Import timeseries (all 13 consumer load profiles) and categorise them into time slices.
  * Is the weighted average of the timeslice values the same as the categorising data into timeslices after taking a weighted average? Test.
* See how different categories (1-8) really are i.e. how much of a difference is there between heat/non-heat etc ones (for commercial and residential separately)?