# Executed-action benchmark — reproducibility package

This archive accompanies the manuscript *"A Budgeted Earth-Science Benchmark for Cross-Regional Reuse of Precipitation
Forecasters"* submitted to *Earth Science Informatics*. It contains no local filesystem paths
and runs as shipped.

It contains the derived action tables, the frozen development predictions, the
analysis scripts, the written protocols, and the claim-traceability matrix
needed to re-derive every number reported in the manuscript, its tables, and its
supplementary material.

## What this package does and does not contain

It **does** contain every artifact downstream of forecaster training: the
realized deploy/adapt/retrain outcomes, the frozen policy predictions, the
budget curves, the target-level AUCs, and the statistical analyses built on
them. All confirmatory claims can be recomputed from these files alone.

It **does not** contain the raw station archives or the trained forecaster
weights. The daily precipitation series originate from public national archives
under their own licences, and the per-station prediction exports run to several
hundred gigabytes. The realized-action tables released here are the aggregated
outputs of those runs and are the inputs to every reported statistic.

## Layout

```
.                                 derived tables and results (analysis inputs/outputs)
├── scripts/                      analysis code, runnable as shipped
├── protocols/                    written protocols frozen before confirmation
├── CLAIM_TRACEABILITY.md         claim -> artifact -> regeneration route matrix
└── MANIFEST_SHA256.txt           SHA-256 of every released file
```

Data files sit at the archive root because each script resolves its own root as
`Path(__file__).resolve().parents[1]`. Run the scripts from the archive root and
they will find their inputs with no path editing.

## Requirements

Python 3.11 or newer with `numpy`, `pandas`, and `scipy`. The modern-learner
benchmark additionally needs `scikit-learn`, `lightgbm`, `torch`, and the
`tabm` / `tabicl` / `tabdpt` packages; its released outputs are provided so that
the panel can be inspected without rerunning it.

## Regenerating the primary confirmatory result

```
python scripts/evaluate_realized_action_confirmatory.py
```

This merges the three frozen confirmatory action tables with the frozen
development predictions, verifies 990 action rows, key uniqueness, complete
action triplets, 30 decisions per target, and agreement between development and
confirmation decision identifiers, then rewrites:

* `realized_action_confirmatory_predictions_outcomes.csv`
* `realized_action_confirmatory_budget_curve.csv`
* `realized_action_confirmatory_target_auc.csv`
* `realized_action_confirmatory_report.md`

The first three are byte-identical to the shipped copies; verify with
`MANIFEST_SHA256.txt`. The report reproduces the primary comparison
(mean AUC 2.547325 for action-value versus 2.550777 for random expected
allocation, 10/11 favorable targets, one-sided paired Wilcoxon *p* = 0.000977,
two-sided robustness *p* = 0.001953) and the Holm-adjusted secondary
comparisons against the five shift-only rankings.

The one-sided test is the prespecified primary analysis. The two-sided
*p*-value is reported as a post-confirmation robustness column only: it does not
enter the success rule and is not multiplicity-adjusted.

## Regenerating the secondary capacity-equivalence analysis

```
python scripts/analyze_capacity_equivalent_gain.py
```

Reproduces the full-curve capacity equivalent of 4.03 additional random
retrainings (target-cluster bootstrap, 100,000 replicates, seed 20260822,
95% CI 3.18–5.17) and the fixed budget grid, including the midpoint at which
random allocation needs 21.51 retrainings to match action-value allocation at 15. The unit is a
retraining count, not measured compute, energy, time, or monetary cost.

## Regenerating the post-hoc modern-learner panel

```
python scripts/benchmark_classical_policy_logo.py
python scripts/benchmark_deep_policy_learners.py
python scripts/evaluate_posthoc_actionvalue_challengers.py
python scripts/evaluate_softbudget_external5.py
```

These reproduce the development and five-region stress-test comparisons of
ExtraTrees, LightGBM, a pointwise residual MLP, FT-Transformer, TabM, TabICLv2,
TabDPT v1.2, and the frozen Ridge policy. Deep-learner outputs depend on
hardware and library versions; `deep_policy_benchmark_config.json` records the
environment used. This panel is a post-hoc model-selection analysis, not a
second independent confirmation, and it cannot alter the frozen Ridge result.

## Regenerating the post-confirmation negative controls

```
python scripts/audit_actionvalue_negative_controls.py
```

Reports the structural audit of the action matrix (retraining is executed once
per target and family, so the realized retraining benefit is a strictly
decreasing function of the cheap-action loss within each of the 33 groups), the
trivial ranker that exploits that identity and nothing else, and a 200-refit
permutation null in which the held-target policy is refitted on shuffled action
outcomes. The ridge penalty is fixed at its modal frozen value so the real policy
and the null are scored identically. Writes
`actionvalue_negative_controls.csv` and `actionvalue_negative_controls.md`.

These controls were specified and run after the frozen confirmation was
complete. They cannot alter a confirmatory number; they test whether the
confirmed gain could have been produced without information.

## Verifying integrity

```
sha256sum -c MANIFEST_SHA256.txt
```

## Claim traceability

`CLAIM_TRACEABILITY.md` maps every submission-facing claim to its evidence
artifact, its regeneration route, and the wording boundary that claim may not
exceed.
