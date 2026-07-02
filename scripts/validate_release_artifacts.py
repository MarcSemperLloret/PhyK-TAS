from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "REPRODUCIBILITY.md",
    "TRACEABILITY.md",
    "LICENSE",
    "DATA_LICENSE.md",
    "CITATION.cff",
    "requirements.txt",
    "results/all_viable_min100_full_aggregate_report.md",
    "results/all_viable_min100_full_sanity_report.md",
    "results/all_viable_min100_full_kbs_results_all.csv",
    "results/all_viable_min100_full_pair_summary_all.csv",
    "results/v2_significance_all_viable_min100_full.csv",
    "results/v2_meta_models_all_viable_min100_full.csv",
    "results/v2_monotonic_all_viable_min100_full.csv",
    "results/v2_conformal_all_viable_min100_full.csv",
    "results/v2_conformal_utility_all_viable_min100_full.csv",
    "results/v2_negative_controls_all_viable_min100_full.csv",
    "results/v2_negative_control_delta_all_viable_min100_full.csv",
    "results/v2_random_dim_control_all_viable_min100_full.csv",
    "results/v2_decision_costs_all_viable_min100_full.csv",
    "results/v2_fusion_ablation_summary_all_viable_min100_full.csv",
    "results/v2_region_sensitivity_all_viable_min100_full.csv",
    "results/v3_fusion_scores_all_viable_min100_full.csv",
    "results/v3_complementarity_all_viable_min100_full.csv",
    "results/v3_conflict_all_viable_min100_full.csv",
    "results/v3_conflict_conformal_all_viable_min100_full.csv",
    "results/v3_distance_generalization_all_viable_min100_full.csv",
    "figures/fig_all_viable_kbs_r2_by_model.png",
    "figures/fig_all_viable_degradation_heatmaps.png",
    "figures/fig_all_viable_threshold_sensitivity.png",
    "figures/fig_all_viable_source_accuracy_vs_transfer.png",
    "figures/fig_v3_distance_generalization.png",
    "scripts/analyze_v2_significance.py",
    "scripts/build_v2_meta_models.py",
    "scripts/build_v2_monotonic.py",
    "scripts/build_v2_conformal.py",
    "scripts/build_v2_conformal_utility.py",
    "scripts/build_v2_negative_controls.py",
    "scripts/build_v2_negative_control_delta.py",
    "scripts/build_v2_random_dim_control.py",
    "scripts/build_v2_decision_costs.py",
    "scripts/build_v2_fusion_ablation_summary.py",
    "scripts/build_v2_region_sensitivity.py",
    "scripts/build_v3_fusion.py",
    "scripts/build_v3_conflict_conformal.py",
    "scripts/build_v3_distance_generalization.py",
]

FORBIDDEN_DIRS = [
    "manuscript_latex",
    "manuscript_latex_eswa",
    "manuscript_latex_infofusion",
    "Data",
    "raw",
    "sources",
]


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    forbidden = [path for path in FORBIDDEN_DIRS if (ROOT / path).exists()]
    too_large = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.stat().st_size >= 90_000_000
    ]

    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"  - {path}")
    if forbidden:
        print("Forbidden local-only directories present:")
        for path in forbidden:
            print(f"  - {path}")
    if too_large:
        print("Files at or above 90 MB:")
        for path in too_large:
            rel = path.relative_to(ROOT)
            size_mb = path.stat().st_size / 1024 / 1024
            print(f"  - {rel} ({size_mb:.1f} MB)")

    if missing or forbidden or too_large:
        return 1

    print("Release artifact check passed.")
    print(f"Checked {len(REQUIRED_FILES)} required files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
