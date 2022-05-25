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

* Plot previous FFT with [Day] [Month] [Year] plots as well?
