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

| # | C/D | Description                                                              |
| - | --- | ------------------------------------------------------------------------ | 
| 1 | C   | No electricity for heat or hot water                                     |
| 2 | C   | Heat accumulation (hot water & heating, includes another source of heat) |
| 3 | C   | Electricity for heating including heat pumps                             |
| 4 | D   | No electricity for heat or hot water                                     |
| 5 | D   | Heat accumulation (usually, hot water)                                   |
| 6 | D   | Electricity for heating (includes another source of heat)                |
| 7 | D   | Electricity for heating including heat pumps                             |
| 8 | C   | Public lighting                                                          |

| Abbreviation | Description                     | #        |
| ------------ | ------------------------------- | -------- |
| CLIG         | Commercial lighting             | #1?      |
| CCOK         | Commercial cooking              | #1?      |
| CREF         | Commercial refrigiration        | #1?      |
| CPLI         | Commercial public lighting      | #8       |
| COEL         | Commercial other electricity    | #1+#2+#3 |
| COEN         | Commercial other energy generic | #1+#2+#3 |

| Abbreviation | Description                     | #        |
| ------------ | ------------------------------------------------------- | -------- |
| CCLE         | Commercial space cooling large existing                 | #        |
| CCSE         | Commercial space cooling small existing                 | #        |
| CHLE         | Commercial space heating large                          | #        |
| CHSE         | Commercial space heating small                          | #        |
| CWLE         | Commercial water heating large existing                 | #        |
| CWSE         | Commercial water heating small existing                 | #        |
| RCDE         | Residential space cooling single detached existing      | #        |
| RCDR         | Residential cloth drying                                | #        |
| RCME         | Residential space cooling multiple all existing         | #        |
| RCMN         | Residential space cooling multiple all new              | #        |
| RCOK         | Residential cooking                                     | #        |
| RCRE         | Residential space cooling single rural existing         | #        |
| RCRN         | Residential space cooling single rural existing         | #        |
| RCWA         | Residential clothes washing                             | #        |
| RDWA         | Residential dish  washing                               | #        |
| RHDE         | Residential space heating single semi-detached existing | #        |
| RHME         | Residential space heating multiple all existing         | #        |
| RHMN         | Residential space heating multiple all existing new     | #        |
| RHRE         | Residential space heating single rural existing         | #        |
| RHRN         | Residential space heating single rural new              | #        |
| RHUN         | Residential space heating single urban new              | #        |
| RLIG         | Residential lighting existing                           | #        |
| ROEL         | Residential other electricity                           | #        |
| ROEN         | Residential other energy generic                        | #        |
| RREF         | Residential refrigiration                               | #        |
| RWDE         | Residential water heating single urban existing         | #        |
| RWME         | Residential water heating multiple all existing         | #        |
| RWMN         | Residential water heating multiple all exisiting        | #        |
| RWRE         | Residential water heating single rural existing         | #        |
| RWRN         | Residential water heating single rural new              | #        |
| RWUN         | Residential water heating single urban new              | #        |

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