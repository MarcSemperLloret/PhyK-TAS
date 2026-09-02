# Modern deep policy-learner benchmark

Development uses leave-one-target-region-out on 2020--2022. The five-region
2023--2025 results are post hoc for these newly added learners and are not an
independent confirmation.

## Frozen configurations

```json
{
  "date": "2026-08-22",
  "models": [
    "tabm",
    "ft_transformer",
    "tabdpt_v1_2"
  ],
  "features": 62,
  "development_rows": 330,
  "external_rows": 165,
  "epochs": 300,
  "ft_transformer_repetitions": 3,
  "tabm": "package defaults (3x512, k=32), AdamW lr=2e-3 wd=3e-4",
  "ft_transformer": "official two-block default, AdamW lr=1e-4 wd=1e-5",
  "tabdpt": "v1.2.0, context=128, ensembles=8, no task-specific tuning",
  "versions": {
    "tabm": "0.0.3",
    "rtdl-revisiting-models": "0.0.2",
    "tabdpt": "1.2.0",
    "torch": "2.6.0+cu126"
  },
  "device": "NVIDIA GeForce RTX 4070",
  "external_status": "post hoc for the new learners"
}
```

## Development LOGO

| learner        |   mean_budget_curve_auc |   mean_random_auc |   mean_oracle_auc |   mean_difference_vs_random |   targets_better_than_random |   targets_total |   mean_gap_closed | stage            |
|:---------------|------------------------:|------------------:|------------------:|----------------------------:|-----------------------------:|----------------:|------------------:|:-----------------|
| tabm           |                2.565371 |          2.573516 |          2.563806 |                   -0.008145 |                           11 |              11 |          0.718630 | development_logo |
| ft_transformer |                2.565465 |          2.573429 |          2.563572 |                   -0.007964 |                           11 |              11 |          0.703386 | development_logo |
| tabdpt_v1_2    |                2.566207 |          2.573591 |          2.563923 |                   -0.007384 |                           11 |              11 |          0.649459 | development_logo |

## External five-region stress test (post hoc)

| learner        |   mean_budget_curve_auc |   mean_random_auc |   mean_oracle_auc |   mean_difference_vs_random |   targets_better_than_random |   targets_total |   mean_gap_closed | stage             |
|:---------------|------------------------:|------------------:|------------------:|----------------------------:|-----------------------------:|----------------:|------------------:|:------------------|
| tabdpt_v1_2    |                1.607651 |          1.611019 |          1.604028 |                   -0.003368 |                            5 |               5 |          0.548398 | external5_posthoc |
| ft_transformer |                1.607906 |          1.611134 |          1.604017 |                   -0.003228 |                            4 |               5 |          0.324701 | external5_posthoc |
| tabm           |                1.609703 |          1.611472 |          1.604091 |                   -0.001769 |                            4 |               5 |          0.173180 | external5_posthoc |

## Paired external comparisons

| learner        | reference   |   mean_auc_difference |   median_auc_difference |   targets_learner_better |   targets_total |   wilcoxon_one_sided_p |
|:---------------|:------------|----------------------:|------------------------:|-------------------------:|----------------:|-----------------------:|
| ft_transformer | ridge       |             -0.000797 |               -0.001382 |                        3 |               5 |               0.312500 |
| ft_transformer | extratrees  |              0.001613 |                0.001737 |                        1 |               5 |               0.968750 |
| ft_transformer | pointwise   |             -0.000585 |               -0.000619 |                        4 |               5 |               0.156250 |
| ft_transformer | tabicl_v2   |             -0.001022 |               -0.000728 |                        4 |               5 |               0.218750 |
| tabdpt_v1_2    | ridge       |             -0.001052 |               -0.000973 |                        4 |               5 |               0.062500 |
| tabdpt_v1_2    | extratrees  |              0.001358 |                0.000396 |                        2 |               5 |               0.906250 |
| tabdpt_v1_2    | pointwise   |             -0.000840 |               -0.000769 |                        3 |               5 |               0.218750 |
| tabdpt_v1_2    | tabicl_v2   |             -0.001277 |               -0.000325 |                        4 |               5 |               0.062500 |
| tabm           | ridge       |              0.001000 |                0.000191 |                        2 |               5 |               0.781250 |
| tabm           | extratrees  |              0.003409 |                0.004168 |                        0 |               5 |               1.000000 |
| tabm           | pointwise   |              0.001212 |                0.000808 |                        2 |               5 |               0.906250 |
| tabm           | tabicl_v2   |              0.000775 |                0.000838 |                        2 |               5 |               0.781250 |

## Computational cost

| learner        | stage            |   fit_seconds |   predict_seconds |
|:---------------|:-----------------|--------------:|------------------:|
| ft_transformer | development      |        86.312 |             0.108 |
| ft_transformer | external_posthoc |         8.782 |             0.015 |
| tabdpt_v1_2    | development      |         0.026 |             5.715 |
| tabdpt_v1_2    | external_posthoc |         0.002 |             0.486 |
| tabm           | development      |        16.724 |             0.026 |
| tabm           | external_posthoc |         1.733 |             0.005 |

## Interpretation

TabM is the strongest development learner (AUC 2.565371), but its advantage over the matched pointwise MLP is small and non-significant (7/11 targets, one-sided p=0.16016), and it loses to ExtraTrees in all five external targets. TabDPT 1.2 is the strongest external DL learner (AUC 1.607651; 5/5 better than its random allocation), but ExtraTrees remains better overall (1.606294). The modern DL panel therefore justifies the learner-selection process; it does not establish a new architecture or support choosing a model merely because it is recent.

The external five-region comparisons in this report are post hoc for TabM, FT-Transformer, and TabDPT 1.2. They can be reported as a stress test or supplementary analysis, not as independent confirmation.
