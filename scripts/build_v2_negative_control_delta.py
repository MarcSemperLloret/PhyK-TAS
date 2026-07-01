"""PhyK-TAS v2: negative-control delta against shift baseline.

Summarizes the negative-control experiment in a form that is easier to interpret
in the manuscript. The key quantity is not the raw R^2 of physical+shift under
permutation, but its gain over the shift-only baseline. If physical descriptors
carry aligned signal, the observed gain should exceed the permuted gain.
"""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
TAG = os.environ.get("PHYKTAS_V2_TAG", "all_viable_min100_full")

IN = PAPER / f"v2_negative_controls_{TAG}.csv"
OUT = PAPER / f"v2_negative_control_delta_{TAG}.csv"
REPORT = PAPER / f"v2_negative_control_delta_{TAG}_report.md"


def main() -> None:
    df = pd.read_csv(IN)
    rows = []
    for (cv_kind, model), sub in df.groupby(["cv_kind", "forecast_model"]):
        shift = sub[(sub.feature_set == "shift") & (sub.control == "observed")]["r2"].iloc[0]
        phys_obs = sub[(sub.feature_set == "physical") & (sub.control == "observed")]["r2"].iloc[0]
        phys_perm = sub[(sub.feature_set == "physical") & (sub.control == "permuted_physical")]["r2"]
        comb_obs = sub[(sub.feature_set == "physical_plus_shift") & (sub.control == "observed")]["r2"].iloc[0]
        comb_perm = sub[
            (sub.feature_set == "physical_plus_shift") & (sub.control == "permuted_physical")
        ]["r2"]
        rows.append({
            "cv_kind": cv_kind,
            "forecast_model": model,
            "r2_shift_observed": shift,
            "r2_physical_observed": phys_obs,
            "r2_physical_permuted_mean": phys_perm.mean(),
            "physical_signal_loss": phys_obs - phys_perm.mean(),
            "delta_combined_minus_shift_observed": comb_obs - shift,
            "delta_combined_minus_shift_permuted_mean": comb_perm.mean() - shift,
            "delta_gain_lost_under_permutation": (comb_obs - shift) - (comb_perm.mean() - shift),
            "n_permutations": int(comb_perm.shape[0]),
        })
    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)

    lines = [
        f"# PhyK-TAS v2 negative-control delta ({TAG})",
        "",
        "This table interprets the physical-descriptor permutation control as "
        "a gain over the shift-only baseline. A positive `delta_gain_lost_under_"
        "permutation` means the aligned physical descriptors add signal beyond "
        "shift diagnostics that is reduced by permutation.",
        "",
        res.round(4).to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
