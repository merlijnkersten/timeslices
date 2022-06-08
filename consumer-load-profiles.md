# Consumer load profiles

_May-June 2022, merlijn_

[Data source](https://www.ote-cr.cz/en/statistics/electricity-load-profiles/normalized-lp?date=2015-05-24)

Fast Fourier transform results:

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

Compared to previous columns:

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



# Categories

Category descriptions ([Czech explanation](https://www.eru.cz/sites/default/files/upload/Priloha_4_541.pdf)):


| Category | Type        | Description                                                  |
| -------- | ----------- | ------------------------------------------------------------ |
| 1        | Commercial  | No electricity for heat or hot water                         |
| 2        | Commercial  | Heat accumulation (hot water & heating, includes another source of heat) |
| 3        | Commercial  | Electricity for heating including heat pumps                 |
| 4        | Residential | No electricity for heat or hot water                         |
| 5        | Residential | Heat accumulation (usually, hot water)                       |
| 6        | Residential | Electricity for heating (includes another source of heat)    |
| 7        | Residential | Electricity for heating including heat pumps                 |
| 8        | Commercial  | Public lighting                                              |



Commercial processes:

| Abbreviation | Description                             | Category |
| ------------ | --------------------------------------- | -------- |
| CHLE         | Commercial space heating large          | #3a      |
| CHSE         | Commercial space heating small          | #3a      |
| CCLE         | Commercial space cooling large existing | #1       |
| CCSE         | Commercial space cooling small existing | #1       |
| CWLE         | Commercial water heating large existing | #2       |
| CWSE         | Commercial water heating small existing | #2       |
| CLIG         | Commercial lighting                     | #1       |
| CCOK         | Commercial cooking                      | #1       |
| CREF         | Commercial refrigeration                | #1       |
| CPLI         | Commercial public lighting              | #8       |
| COEL         | Commercial other electricity            | #1+#2    |
| COEN         | Commercial other energy generic         | #1+#2    |



Residential processes:

| Abbreviation | Description                                             | Category |
| ------------ | ------------------------------------------------------- | -------- |
| RHDE         | Residential space heating single semi-detached existing | #6a+#7a  |
| RHRE         | Residential space heating single rural existing         | #6a+#7a  |
| RHRN         | Residential space heating single rural new              | #6a+#7a  |
| RHUN         | Residential space heating single urban new              | #6a+#7a  |
| RHME         | Residential space heating multiple all existing         | #6a+#7a  |
| RHMN         | Residential space heating multiple all existing new     | #6a+#7a  |
| RCDE         | Residential space cooling single detached existing      | #4       |
| RCRE         | Residential space cooling single rural existing         | #4       |
| RCRN         | Residential space cooling single rural new              | #4       |
| RCME         | Residential space cooling multiple all existing         | #4       |
| RCMN         | Residential space cooling multiple all new              | #4       |
| RWUN         | Residential water heating single urban new              | #5       |
| RWDE         | Residential water heating single urban existing         | #5       |
| RWRN         | Residential water heating single rural new              | #5       |
| RWRE         | Residential water heating single rural existing         | #5       |
| RWME         | Residential water heating multiple all existing         | #5       |
| RWMN         | Residential water heating multiple all new              | #5       |
| RCOK         | Residential cooking                                     | #4       |
| RCWA         | Residential clothes washing                             | #4       |
| RCDR         | Residential cloth drying                                | #4       |
| RDWA         | Residential dish  washing                               | #4       |
| RLIG         | Residential lighting existing                           | #4b      |
| RREF         | Residential refrigeration                               | #4       |
| ROEL         | Residential other electricity                           | #4+#5    |
| ROEN         | Residential other energy generic                        | #4+#5    |



Other processes (timeslice dependent `COM_FR` processes). I don't think we can use consumer load profiles to determine their values.

| Abbreviation | Description             | Category |
| ------------ | ----------------------- | -------- |
| TAV          | Aviation generic        |          |
| TBI          | Road bus intercity      |          |
| TBU          | Road bus urban          |          |
| TC           | Road car short distance |          |
| TFR          | Road freight            |          |
| TMO          | Road motors             |          |
| TNA          | Navigation generic      |          |
| TTF          | Rail freight            |          |
| TTL          | Rail passengers light   |          |
| TTP          | Rail passengers heavy   |          |
| IFT          | Food and tobacco demand |          |
| IOI          | Other industries demand |          |

Relevant document: `CZ_V02-\VT_CZ_TRA_V2.2.xlsx`



The same information as in the previous three tables, but now by category (instead of process):

| Category | Processes                                                  |
| -------- | ---------------------------------------------------------- |
| 1     	 | CCLE, CCSE, CLIG, CCOK, CCREF				                      |
| 2        | CWLE, CWSE 				                                        |
| 3        | _None_                                                     |
| 4        | RCDE, RCRE, RCRN, RCME, RCMN, RCOK, RCWA, RCDR, RDWA, RREF	|
| 5        | RWUN, RWDE, RWRN, RWRE, RWME,  RWMN                        |
| 6	       | _None_                                                     |
| 7        | _None_                                                     |
| 8        | CPLI						                                            |
| 1, 2     | COEL, COEN				                                          |
| 4, 5     | ROEL, ROEN				                                          |
| 3a       | CHLE, CHSE				                                          |
| 6a, 7a   | RHDE, RHRE, RHRN, RHUN, RHME, RHMN						              |
| 4b       | RLIG				                                                |

a: No summer heating,
b: No summer lighting,

To get the values for the TTD5 profile, I took a population-weighted average of the regional TDD5 profiles. I combined Czech regions into the regional TTD5 profiles in the following way:

| Name (CZ)      | Name (EN)       | Regions	                  | Pop (,000) | Pop (relative) |
| -------------- | --------------- | -------------------------- | ---------- | -------------- |
| jižní čechy    | South Bohemia   | South Bohemian, Vysocina   |	1141       | 0.11           |
| jižní morava   | South Moravia   | South Moravian, Zlin       | 1757       | 0.17           |
| praha          | Prague          | Praha                      | 1275       | 0.12           |
| severní čechy  | North Bohemia   | Liberec, Usti nad Labem    | 1237       | 0.12           |
| severní morava | North Moravia   | Moravian-Silesian, Olomouc | 1801       | 0.17           |
| střední čechy  | Central Bohemia | Central Bohemia            | 1387       | 0.13           |
| východní čechy | East Bohemia    | Hradec Kralove, Pardubice  | 1058       | 0.10           |
| západní čechy  | West Bohemia    | Karlovy Vary, Plzen        |862         | 0.08           |



# To do's

* Check that categorisation of processes and categorisation of regions is correct,
* Determine how to average combinations of categories (which weights to assign).
* Add timeslice values of the consumer load profiles into TIMES-CZ,



# Other 

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