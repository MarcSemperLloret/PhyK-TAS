# Phase status v1

## Completed now

### Phase 1: AR6 assignment

Outputs:

- `stations_ar6.csv`
- `stations_ar6_summary.csv`
- `stations_ar6_map.png`

Method:

- `regionmask.defined_regions.ar6.land`
- AR6 land reference regions from Iturbide et al. 2020 via `regionmask 0.13.0`

### Phase 2: Pre-dedup viability

Outputs:

- `viability_pre_dedup.csv`
- `viability_pre_dedup_summary.md`

Key result for core sources `global_ghcnd_01` + `eur_ecad_01`:

- start 2000, 95%: MED 227, WCE 4326, NEU 2833
- start 2000, 80%: MED 470, WCE 5136, NEU 3221
- start 2005, 95%: MED 345, WCE 4565, NEU 2898
- start 2005, 80%: MED 982, WCE 5256, NEU 3363

### Phase 3: Deduplication viability

Outputs:

- `viability_post_dedup.csv`
- `viability_dedup_comparison.md`
- `dedup_log.csv`
- `dedup_audit_sample.csv`
- `dedup_audit_sample_with_correlations.csv`
- `dedup_audit_report.md`

Key result for core sources `global_ghcnd_01` + `eur_ecad_01`:

- start 2000, 95%: MED 192, WCE 3928, NEU 2300
- start 2000, 80%: MED 404, WCE 4646, NEU 2597
- start 2005, 95%: MED 311, WCE 4100, NEU 2345
- start 2005, 80%: MED 913, WCE 4705, NEU 2704

Audit:

- 30 sampled duplicate edges checked with daily correlations.
- All sampled pairs have correlation >= 0.9997 over 2005-2025.

### Phase 4: Region decisions

Output:

- `region_decisions.md`

Operational decision:

- Use `period_start=2005` as preregistration candidate.
- WCE and NEU: principal 95%.
- MED: principal with 80% plus explicit missingness mask, 95% as strict sensitivity.

### Phase 5: Preliminary power analysis

Output:

- `power_analysis.md`
- `dedup_assignments_core_2005.csv`
- `pilot_light_stations.csv`
- `pilot_light_degradation.csv`
- `pilot_light_power.md`

Status:

- Completed as analytic pre-model power check plus lightweight pilot-model degradation estimate.

Key result:

- MED is viable by station count but limiting by 5 x 5 cell count.
- WCE and NEU are strong by station count and better by cell count.
- The pilot confirms that degradation behavior differs by region even for a simple climatology baseline; NEU can show negative degradation in this crude setup, so the final paper must not assume the hypothesis will hold.

## Not completed

### Phase 6: Preregistration

Not completed.

Reasons:

- The directory is not currently a git repository.
- No OSF preregistration was created from this environment.
- Final pilot-model power analysis has not been run.

Required before preregistration:

- manual visual review of `stations_ar6_map.png`;
- manual review of `dedup_audit_sample_with_correlations.csv`;
- final choice of MED 80% main vs 95% main after review;
- pilot-model power analysis if the paper requires inferential claims beyond the analytic pre-check.

Pilot-model power status: completed as lightweight climatology pilot.

### Forecasting experiment status

Status: first sampled forecasting experiment completed.

Artifacts:

- `forecast_dataset_operational_sample.npz`
- `forecast_dataset_operational_sample_metadata.csv`
- `forecast_patchtst_station_metrics.csv`
- `forecast_patchtst_pair_summary.csv`
- `forecast_patchtst_report.md`

Scope:

- 300 stations per region;
- lookback 30 days;
- horizon t+1;
- `linear_window` and `patchtst_small`;
- capped training/validation/test windows for runtime.

Limitation:

- This is a sampled pipeline-validating experiment, not the final full-scale model benchmark.

### Deduplication audit

Status: accepted for preregistration candidate.

Rationale:

- 30 sampled duplicate edges were checked with daily correlations.
- All sampled pairs have correlation >= 0.9997 over 2005-2025.
- No plausible false positive was identified at this stage.

## Manual review notes

### AR6 map

Status: accepted.

Note:

- The Europe coastline/outline is not visually explicit in `stations_ar6_map.png`.
- The station cloud shape and AR6 boundaries are sufficient for the current assignment sanity check.
- No systematic anomaly was reported for MED/WCE/NEU boundaries at this stage.
