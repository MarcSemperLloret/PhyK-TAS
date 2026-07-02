# Conflict confound-control analysis (all_viable_min100_full)

Pair-level OLS with HC3 robust standard errors. Outcome is standardized absolute error of reliability-weighted source fusion. Predictors are standardized; fixed effects are target region and forecast model.

| term                 |   coef_standardized |   robust_se |   p_value |   ci_low |   ci_high |   n |     r2 |
|:---------------------|--------------------:|------------:|----------:|---------:|----------:|----:|-------:|
| conflict_z           |              0.637  |      0.1571 |    0.0001 |   0.3291 |    0.9449 | 660 | 0.6465 |
| predicted_severity_z |             -0.0818 |      0.1314 |    0.5333 |  -0.3394 |    0.1757 | 660 | 0.6465 |
| shift_magnitude_z    |             -0.0743 |      0.0234 |    0.0015 |  -0.1201 |   -0.0285 | 660 | 0.6465 |

Model formula:

`abs_error_z ~ conflict_z + predicted_severity_z + shift_magnitude_z + C(target_region) + C(forecast_model)`
