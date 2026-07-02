# PhyK-TAS v3 reliability-aware fusion (all_viable_min100_full)

## spatial_knn_ridge
- source wins across regions: physical=1, shift=10
- R2: physical=0.300, shift=0.655, concat=0.823, precision-fusion=0.659 (mean physical weight 0.33)
- conflict vs fusion error: Pearson=0.389, Spearman=0.238; mean |err| low/mid/high conflict = 0.027/0.027/0.045

## stgcn_diffusion
- source wins across regions: physical=5, shift=6
- R2: physical=0.215, shift=0.034, concat=0.311, precision-fusion=0.241 (mean physical weight 0.55)
- conflict vs fusion error: Pearson=0.419, Spearman=0.397; mean |err| low/mid/high conflict = 0.036/0.044/0.109

## graphwavenet_transfer
- source wins across regions: physical=3, shift=8
- R2: physical=0.249, shift=0.158, concat=0.336, precision-fusion=0.305 (mean physical weight 0.53)
- conflict vs fusion error: Pearson=0.483, Spearman=0.496; mean |err| low/mid/high conflict = 0.033/0.047/0.143

## regional_doy_climatology
- source wins across regions: physical=0, shift=11
- R2: physical=0.077, shift=0.965, concat=0.885, precision-fusion=0.965 (mean physical weight 0.04)
- conflict vs fusion error: Pearson=0.460, Spearman=0.370; mean |err| low/mid/high conflict = 0.064/0.067/0.203
