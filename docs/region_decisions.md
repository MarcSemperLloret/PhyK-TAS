# Region decisions v1

Decisions are based on `viability_post_dedup.csv` using the core sources `global_ghcnd_01` + `eur_ecad_01`.

## Candidate starts

|   period_start | ar6_region   |   n80_post_dedup |   n95_post_dedup | decision                         |
|---------------:|:-------------|-----------------:|-----------------:|:---------------------------------|
|           2000 | MED          |              404 |              192 | limited_power_or_grouping_needed |
|           2000 | WCE          |             4646 |             3928 | principal_95                     |
|           2000 | NEU          |             2597 |             2300 | principal_95                     |
|           2005 | MED          |              913 |              311 | principal_80_mask_sensitivity_95 |
|           2005 | WCE          |             4705 |             4100 | principal_95                     |
|           2005 | NEU          |             2704 |             2345 | principal_95                     |

## Selected operational design

Use `period_start=2005` for the preregistration candidate.

Reason:

- `MED` fails the 300-station 95% rule with start 2000 (`n95=192`).
- `MED` passes the 300-station 95% rule with start 2005 (`n95=311`).
- `WCE` and `NEU` are strong under both starts.
- Starting in 2005 improves stability without changing the core design qualitatively.

## Decisions for period_start=2005

|   period_start | ar6_region   |   n80_post_dedup |   n95_post_dedup | decision                         |
|---------------:|:-------------|-----------------:|-----------------:|:---------------------------------|
|           2005 | MED          |              913 |              311 | principal_80_mask_sensitivity_95 |
|           2005 | WCE          |             4705 |             4100 | principal_95                     |
|           2005 | NEU          |             2704 |             2345 | principal_95                     |

## MED contingency

If manual deduplication audit or AR6 boundary review reduces `MED` below 300 at 95%, use 80% with explicit missingness mask as the main MED analysis and retain 95% as strict sensitivity.

## Caveat

This decision is not a frozen preregistration. It becomes preregistrable only after deduplication audit and power analysis.
