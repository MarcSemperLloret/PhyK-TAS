# Frozen protocol: Soft-Budget external-region validation

**Frozen:** 22 August 2026.  
**Status at freeze:** no deploy/adapt/retrain outcomes have been generated or inspected for CAU, NAU, NEN, ESB, or RFE.  
**Purpose:** test whether the Soft-Budget objective improves the complete retraining-budget curve beyond a capacity-matched pointwise neural learner on geographically external targets.

## 1. External targets and source library

The untouched target set is fixed to five IPCC AR6 regions selected only from station viability counts:

| Target | Coverage threshold | Stations | 5-degree cells |
|---|---:|---:|---:|
| CAU | 80% | 69 | 9 |
| NAU | 80% | 58 | 7 |
| NEN | 80% | 51 | 21 |
| ESB | 80% | 39 | 19 |
| RFE | 80% | 37 | 17 |

The source library remains the original 11 regions: CNA, EAS, EAU, ENA, MED, NCA, NEU, NWN, SAU, WCE, and WNA. Each external target therefore contains 11 sources × 3 forecasting families = 33 decisions. The complete external validation contains 165 decisions and 495 realized action outcomes.

No external target is added to policy training, hyperparameter selection, feature scaling, or source-model training.

## 2. Temporal blocks and actions

- Source training: 2005–2012.
- Source validation: 2013–2015.
- Target adaptation training: 2013–2014.
- Target adaptation validation: 2015.
- External action outcomes: 2023–2025.

The deploy, adapt, and retrain implementations remain identical to the frozen 11-region experiment. No architecture, epoch count, learning rate, graph construction, affine-calibration rule, or action data window may be changed after external outcomes are generated.

## 3. Frozen Soft-Budget learner

Training data are the 330 original-region development decisions with 2020–2022 realized outcomes. The learner receives the same 62 pre-deployment predictors: 11 shift/distance measures, 48 physical-regime features, and 3 model-family indicators.

The network is fixed as follows:

- two-output residual MLP;
- hidden width 128, SiLU activations, LayerNorm, dropout 0.10;
- output 1: adaptation benefit over deployment;
- output 2: incremental retraining gain over the better realized cheap action;
- ensemble of 3 independently seeded members;
- 300 full-batch AdamW epochs;
- learning rate 0.001 with cosine decay;
- weight decay 0.0002 and gradient clipping at 5.0;
- pointwise loss: 0.50 SmoothL1 for adaptation plus 0.25 SmoothL1 for incremental gain;
- Soft-Budget weight 1.0 and soft-rank temperature 0.5.

The Soft-Budget term maximizes exposure-weighted incremental gain over differentiable descending ranks separately within each training target. The exact discrete identity relating ranks to the mean loss over all budgets must be reported in the manuscript.

## 4. Frozen baselines and ablations

1. Capacity-matched pointwise neural ablation: identical network, ensemble, optimizer, epochs, and pointwise targets; Soft-Budget weight set to zero.
2. Pairwise neural ablation: identical architecture with gain-weighted pairwise logistic ranking.
3. TabICLv2 regression with four estimators and no task-specific tuning.
4. Frozen StandardScaler–Ridge action-value policy.
5. ExtraTrees and LightGBM with hyperparameters selected only from original-region development using grouped validation.
6. Random expected allocation, shift-only rankings, and restricted oracle.

## 5. Evaluation and success rule

Each target has budgets 0–33. The primary metric is the discrete mean MAE over all 34 budgets, computed within target. The five external target AUCs are the independent paired units.

The primary hypothesis is directional: Soft-Budget AUC is lower than the capacity-matched pointwise neural AUC.

**GO for objective-specific novelty requires all of the following:**

1. favorable mean and median paired difference;
2. Soft-Budget improves all 5 external targets;
3. exact one-sided paired Wilcoxon p=0.03125;
4. no forecasting family has an unfavorable mean difference;
5. Soft-Budget is not worse than TabICLv2 in mean AUC;
6. code checks confirm 495 unique complete action rows and no missing 2023–2025 MAE.

If any primary condition fails, the Soft-Budget objective remains exploratory and cannot replace the frozen Ridge contribution. Comparisons with Ridge, TabICLv2, trees, shift-only rankings, and the oracle are secondary; they do not rescue a failure against the matched pointwise ablation.

## 6. Integrity boundary

The previously inspected 2023–2025 outcomes for the original 11 regions are retrospective challenger stress tests and must remain labeled post hoc. Only the five regions in this protocol can provide external objective-specific validation. Station viability and feature availability may be checked before running actions; action MAE files must not be partially inspected or used to revise this protocol.
