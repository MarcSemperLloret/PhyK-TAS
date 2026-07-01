# Transfer risk decision layer report

Target:

- risk classes derived from `mae_out_minus_in`.
- safe: degradation <= 0.
- moderate: positive degradation up to the 75th percentile of positive degradation.
- high: above that threshold.

Feature sets:

- physical knowledge;
- generic shift;
- physical plus shift.

Validation:

- leave-target-region-out;
- group-by-cell.

Decision policy:

- `retrain` if p_high >= 0.5.
- `adapt` if p_high >= 0.25 or p_safe < 0.4.
- `deploy` otherwise.

The current decision table uses physical_plus_shift + random forest + group-by-cell.

## Classifier metrics

| feature_set         | cv_kind                 | model         |     n |   n_features |   log_loss |   balanced_accuracy |   macro_f1 |   brier_high |
|:--------------------|:------------------------|:--------------|------:|-------------:|-----------:|--------------------:|-----------:|-------------:|
| physical_knowledge  | leave_target_region_out | logistic      | 14716 |           12 |   0.990841 |            0.527543 |   0.524002 |    0.0559038 |
| physical_knowledge  | leave_target_region_out | random_forest | 14716 |           12 |   1.30279  |            0.579881 |   0.526068 |    0.0527647 |
| generic_shift       | leave_target_region_out | logistic      | 14716 |           11 |   3.6493   |            0.438045 |   0.29192  |    0.200061  |
| generic_shift       | leave_target_region_out | random_forest | 14716 |           11 |   1.87887  |            0.503427 |   0.468995 |    0.1416    |
| physical_plus_shift | leave_target_region_out | logistic      | 14716 |           23 |   2.5823   |            0.294941 |   0.299527 |    0.118554  |
| physical_plus_shift | leave_target_region_out | random_forest | 14716 |           23 |   2.07287  |            0.308706 |   0.289216 |    0.127208  |
| physical_knowledge  | group_by_cell           | logistic      | 14716 |           12 |   0.753118 |            0.676221 |   0.643795 |    0.0419281 |
| physical_knowledge  | group_by_cell           | random_forest | 14716 |           12 |   0.690006 |            0.697343 |   0.653848 |    0.0438235 |
| generic_shift       | group_by_cell           | logistic      | 14716 |           11 |   0.513797 |            0.857341 |   0.863061 |    0.0334776 |
| generic_shift       | group_by_cell           | random_forest | 14716 |           11 |   0.458773 |            0.857341 |   0.863061 |    0.0337064 |
| physical_plus_shift | group_by_cell           | logistic      | 14716 |           23 |   0.42687  |            0.850157 |   0.837091 |    0.0289706 |
| physical_plus_shift | group_by_cell           | random_forest | 14716 |           23 |   0.275913 |            0.9018   |   0.886291 |    0.0255674 |

## Pair-level decision summary

| source_region   | target_region   |    n |   mean_p_safe |   mean_p_moderate |   mean_p_high |   retrain_rate |   adapt_rate |   deploy_rate |   mean_observed_degradation |
|:----------------|:----------------|-----:|--------------:|------------------:|--------------:|---------------:|-------------:|--------------:|----------------------------:|
| MED             | NEU             | 2345 |     0.936952  |        0.0433446  |     0.0197038 |     0          |   0.00511727 |      0.994883 |                  -0.0922296 |
| MED             | WCE             | 4100 |     0.711402  |        0.257565   |     0.0310331 |     0.00268293 |   0.190244   |      0.807073 |                  -0.0362713 |
| NEU             | MED             |  913 |     0.014957  |        0.00975367 |     0.975289  |     1          |   0          |      0        |                   0.284396  |
| NEU             | WCE             | 4100 |     0.0171693 |        0.906194   |     0.076637  |     0.0617073  |   0.938293   |      0        |                   0.0807579 |
| WCE             | MED             |  913 |     0.0149737 |        0.103025   |     0.882001  |     0.992333   |   0.00766703 |      0        |                   0.17791   |
| WCE             | NEU             | 2345 |     0.757948  |        0.222359   |     0.0196924 |     0          |   0.121109   |      0.878891 |                  -0.0416442 |

## Recommendation counts

| source_region   | target_region   | recommendation   |   count |
|:----------------|:----------------|:-----------------|--------:|
| MED             | NEU             | adapt            |      12 |
| MED             | NEU             | deploy           |    2333 |
| MED             | WCE             | adapt            |     780 |
| MED             | WCE             | deploy           |    3309 |
| MED             | WCE             | retrain          |      11 |
| NEU             | MED             | retrain          |     913 |
| NEU             | WCE             | adapt            |    3847 |
| NEU             | WCE             | retrain          |     253 |
| WCE             | MED             | adapt            |       7 |
| WCE             | MED             | retrain          |     906 |
| WCE             | NEU             | adapt            |     284 |
| WCE             | NEU             | deploy           |    2061 |
