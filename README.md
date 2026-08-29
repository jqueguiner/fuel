# fuel — open fuel-price catalog

Every country/source we can find that publishes **fuel prices**, organised
`<COUNTRY>/<source>/source.json` — with the live feed URL, format, license, and whether
it's per-station + real-time. Same idea as the gtfs catalog, for petrol/diesel/LPG.

## Layout
```
<CC>/<source>/source.json   # feed url + format + license + fuels + flags
<CC>/<source>/fetch.sh       # pull current prices into this dir
catalog.csv                  # flat index
```

## Coverage (25 sources, 14 countries)
Keyless + per-station real-time: **FR** (data.economie.gouv.fr), **ES** (minetur, 11k stations),
**IT** (MIMIT Osservaprezzi), **GB** (CMA retailer feeds — Asda/BP/Morrisons/Sainsbury's/Tesco/MFG/…).
Free-key: **DE** (Tankerkönig), **AT** (E-Control), **AU** (NSW FuelCheck), **GR**, **CL**.
Regulated/aggregate: **LU**, **PT**, **BR** (ANP weekly), **ZA** (DMRE monthly), **IN** (city RSP).

| Field | Meaning |
|---|---|
| per_station | true = individual station prices (not a national average) |
| realtime | updated daily or better |
| key_required | needs a free API key |

Contributions: add `<CC>/<source>/source.json` + `fetch.sh`, append to `catalog.csv`.
