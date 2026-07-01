# Deduplication audit report

This is the required 30-edge audit sample for manual inspection.

Total dedup edges: 17763
Merged edges: 14369

## Criteria counts

| criterion                         |   n_edges |
|:----------------------------------|----------:|
| spatial_1km_plus_name_elev10m     |     13038 |
| spatial_1km_plus_elev10m          |      2635 |
| same_candidate_duplicate_key      |      1859 |
| same_wmo_id                       |        95 |
| spatial_1km_plus_name             |        54 |
| spatial_1km_plus_wmo_name_elev10m |        41 |
| spatial_1km_plus_wmo_elev10m      |        40 |
| spatial_1km_plus_wmo              |         1 |

## Audit rule

- Inspect `dedup_audit_sample.csv`.
- Mark `plausible_false_positive=True` for stations that appear legitimately distinct.
- If more than 3 of 30 are plausible false positives, rerun with stricter metadata identity.

## Correlation check

The sampled rows were extended in `dedup_audit_sample_with_correlations.csv`.

Result:

- 30 sampled duplicate edges were checked.
- All sampled pairs have daily correlation >= 0.9997 over 2005-2025.
- All sampled pairs have thousands of overlapping daily observations.

Interpretation:

- The sampled deduplication decisions are consistent with duplicate station identity.
- No sampled edge currently suggests a plausible false positive.
- This does not eliminate the need for manual review before preregistration, but it supports the current deduplication rule.

## Manual decision

Status: accepted for preregistration candidate.

Rationale:

- The 30 sampled duplicate edges have near-perfect daily correlations over long overlaps.
- The sampled metadata are consistent with duplicate identity.
- No plausible false positive was identified at this stage.
