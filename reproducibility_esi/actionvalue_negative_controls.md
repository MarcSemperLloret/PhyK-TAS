# Post-confirmation negative controls for the action-value policy

These controls were run after the frozen confirmation was completed. They do not
alter any confirmatory number; they test whether that number could have arisen
without information.

## Structural audit of the action matrix

- Decisions: 330
- Distinct realized outcomes: deploy 330, adapt 330, retrain 33
- Retraining is executed once per (target, family) and shared across the ten
  source candidates, because a target-trained model does not depend on the source.
- Consequently, within each of the 33 (target, family) groups the realized
  retraining benefit is a strictly decreasing function of the cheap-action loss:
  Spearman rho = 1.000 in 100% of groups (minimum 1.0000).
- The within-family ordering is therefore not a learning problem. The learnable
  content of the benchmark is the comparison across families competing for the
  same target budget.

## Trivial ranker

Allocating by realized cheap-action loss alone, with no learning, is the ranking
the structural property suggests. Pooled over the thirty candidates of a target it
gains -0.000527 MAE-AUC against random expectation (-6.6% of the ceiling) and is favorable in 4/11 targets.
It is worse than random ordering: cheap-action loss is not comparable across
families, so high-error families absorb the budget regardless of what retraining
would return there.

## Permutation null

The held-target policy was refitted on shuffled action outcomes 200 times and
re-evaluated on the confirmation block, with the ridge penalty fixed at the modal
frozen value so that the real policy and the null are scored identically.

- Real policy under the same fixed penalty: +0.004167 MAE-AUC, 10/11 favorable
- Null: mean +0.000066, sd 0.001401, 95th percentile +0.002474, maximum +0.003533
- P(null gain >= real gain) = 0.0000 over 200 permutations

The null is centred on zero, as it must be, and the observed gain lies 2.9 null standard deviations above it.
Seed 20260902.
