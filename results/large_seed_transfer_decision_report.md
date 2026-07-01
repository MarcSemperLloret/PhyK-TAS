# Large-seed transfer decision report

Decision thresholds use MAE out-minus-in degradation:

- deploy: upper 95% seed interval <= 0.010;
- adapt: upper 95% seed interval <= 0.025;
- retrain: upper 95% seed interval > 0.025.

The decision is conservative: it uses mean + 95% half-width across large seeds.

## Decision counts

| model                 | conservative_decision   |   n_pairs |
|:----------------------|:------------------------|----------:|
| graphwavenet_transfer | adapt                   |         3 |
| graphwavenet_transfer | deploy                  |         1 |
| graphwavenet_transfer | retrain                 |         2 |
| stgcn_diffusion       | adapt                   |         2 |
| stgcn_diffusion       | deploy                  |         3 |
| stgcn_diffusion       | retrain                 |         1 |

## Pair-level decisions

| model                 | source_region   | target_region   |   degradation_mean |   degradation_sd |   degradation_ci95_halfwidth | expected_decision   | conservative_decision   | uncertainty_flag           |
|:----------------------|:----------------|:----------------|-------------------:|-----------------:|-----------------------------:|:--------------------|:------------------------|:---------------------------|
| graphwavenet_transfer | WCE             | NEU             |         0.0298683  |      0.00659862  |                  0.00746704  | retrain             | retrain                 | boundary_adapt_to_retrain  |
| graphwavenet_transfer | NEU             | MED             |         0.0132737  |      0.010976    |                  0.0124205   | adapt               | retrain                 | boundary_deploy_to_retrain |
| graphwavenet_transfer | MED             | NEU             |         0.0167164  |      0.00307475  |                  0.0034794   | adapt               | adapt                   | stable                     |
| graphwavenet_transfer | NEU             | WCE             |         0.00331142 |      0.00888808  |                  0.0100578   | deploy              | adapt                   | boundary_deploy_to_adapt   |
| graphwavenet_transfer | WCE             | MED             |         0.00960473 |      0.00080957  |                  0.000916114 | deploy              | adapt                   | boundary_deploy_to_adapt   |
| graphwavenet_transfer | MED             | WCE             |         0.00103611 |      0.00141295  |                  0.0015989   | deploy              | deploy                  | stable                     |
| stgcn_diffusion       | MED             | NEU             |         0.0239938  |      0.00230038  |                  0.00260312  | adapt               | retrain                 | boundary_adapt_to_retrain  |
| stgcn_diffusion       | WCE             | NEU             |         0.0177209  |      0.0043303   |                  0.0049002   | adapt               | adapt                   | stable                     |
| stgcn_diffusion       | NEU             | MED             |         0.0129067  |      0.00363727  |                  0.00411596  | adapt               | adapt                   | boundary_deploy_to_adapt   |
| stgcn_diffusion       | NEU             | WCE             |         0.00466561 |      0.00218245  |                  0.00246967  | deploy              | deploy                  | stable                     |
| stgcn_diffusion       | WCE             | MED             |         0.00641619 |      0.000311808 |                  0.000352843 | deploy              | deploy                  | stable                     |
| stgcn_diffusion       | MED             | WCE             |         0.00342997 |      0.000347009 |                  0.000392677 | deploy              | deploy                  | stable                     |

## Figures

- `figures/fig_large_transfer_decision_graphwavenet_transfer.png`
- `figures/fig_large_transfer_decision_stgcn_diffusion.png`