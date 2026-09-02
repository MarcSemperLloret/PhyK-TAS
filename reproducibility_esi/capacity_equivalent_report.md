# Post-confirmation capacity-equivalent analysis

## Status

**Exploratory practical-significance analysis of the frozen confirmation.** No policy was refit and no budget was selected as a new confirmatory endpoint.

## Main result

Across the complete 0--30 capacity curve, the AUC advantage is equivalent to 4.03 additional random retrainings (target-cluster bootstrap 95% CI 3.18--5.17), or 13.4% of the full 30-decision capacity.
The estimate remains between 3.84 and 4.45 when each target region is omitted in turn.

At the natural midpoint budget of 15, PhyK-TAS obtains mean MAE 2.545211. Random allocation requires an interpolated budget of 21.51 to reach the same pooled mean MAE: a capacity-equivalent saving of 6.51 retrainings (95% CI 5.05--8.37). The action-value policy is better than random in 10/11 targets and better than MMD in 10/11 at this budget.

## Fixed reporting grid of representative budgets

|   budget |   random_equivalent_budget |   capacity_equivalent_saving |   saving_ci95_low |   saving_ci95_high |   mmd_equivalent_budget |   targets_action_better_than_random |   targets_action_better_than_mmd |
|---------:|---------------------------:|-----------------------------:|------------------:|-------------------:|------------------------:|------------------------------------:|---------------------------------:|
|        5 |                      9.053 |                        4.053 |             3.022 |              5.701 |                   7.162 |                                  10 |                                7 |
|       10 |                     15.741 |                        5.741 |             4.001 |              7.881 |                  14.402 |                                  10 |                                6 |
|       15 |                     21.505 |                        6.505 |             5.053 |              8.374 |                  21.624 |                                  10 |                               10 |
|       20 |                     25.158 |                        5.158 |             4.068 |              6.632 |                  25.694 |                                  10 |                                8 |
|       25 |                     28.504 |                        3.504 |             2.108 |              4.825 |                  29.418 |                                  10 |                                7 |

## Interpretation boundary

Random expected allocation is exactly linear in budget, which makes the horizontal capacity conversion identifiable on the pooled mean curve. MMD equivalence uses the first crossing of its at-most-budget envelope. The bootstrap resamples target regions, not the 330 decisions. The confidence intervals quantify geographic sampling variability; they are not a second confirmatory test. Target-specific capacity ratios can be unstable when random retraining has a very shallow marginal benefit, so the manuscript-safe claim is the pooled curve result together with the 10/11 target direction, not a universal per-region saving.

## Target-level audit

The full-curve AUC advantage is favorable in 10/11 targets. NCA is the only unfavorable target and must remain visible in any presentation.
