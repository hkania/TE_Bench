#!/usr/bin/env python3
"""
plot_identity_vs_coverage.py

Usage:
    python3 plot_identity_vs_coverage.py ref_identity.csv test.csv seq_len output.pdf extra_TEs
"""

import sys
import csv
import matplotlib.pyplot as plt
import numpy as np

def build_coverage_list(csv_file, seq_len):
    """Returns a list where each index represents a base in the genome.
       1 means covered by TE, 0 means not covered."""
    coverage = [0] * seq_len
    with open(csv_file, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(",")
            start = int(parts[2])
            end = int(parts[3])
            for i in range(start - 1, end):
                coverage[i] = 1
    return coverage


def compute_coverage_for_elements(ref_csv, query_coverage):
    """For each element in ref_csv, compute percent coverage (0–100%)."""
    coverages = []
    types = []
    identities = []
    with open(ref_csv, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            start = int(row[2])
            end = int(row[3])
            elem_type = str(row[4])
            identity = float(row[-1])

            length = end - start + 1
            covered = sum(query_coverage[start-1:end])
            coverage_pct = (covered / length) * 100

            coverages.append(coverage_pct)
            identities.append(identity)
            types.append(elem_type)
    return identities, coverages, types


def main():
    if len(sys.argv) != 6:
        print("Usage: python3 plot_identity_vs_coverage.py reference.csv test.csv seq_len out_plot extras")
        sys.exit(1)

    ref_csv = sys.argv[1]
    test_csv = sys.argv[2]
    seq_len = int(sys.argv[3])
    out_name = sys.argv[4]
    extras_allowed = sys.argv[5].split(",") if len(sys.argv) > 5 else []
    extras_allowed = [e.strip().lower() for e in extras_allowed if e.strip()]

    print("Building coverage map from test CSV...")
    test_coverage = build_coverage_list(test_csv, seq_len)

    print("Computing coverage for reference elements...")
    identities, coverages, types = compute_coverage_for_elements(ref_csv, test_coverage)

    identities = np.array(identities)
    coverages = np.array(coverages)
    types = np.array(types)

    type_colors = {
        "dna": "#CB3A2B",
        "ltr": "#E9C716",
        "line": "#5F9ED1",
        "line-dependent": "#41B7A8"
    }
    default_color = "#808080"

    core_types = set(type_colors.keys())
    types_lower = np.array([t.lower() for t in types])
    all_types_found = set(types_lower)

    core_present = sorted(core_types & all_types_found)
    extra_present = sorted(set(extras_allowed) & all_types_found)
    unique_types = core_present + extra_present

    print(f"Types to plot: {unique_types}")
    print("Types found in reference:", sorted(set(types)))
    print("Core types:", sorted(core_types))
    print("Extras allowed:", extras_allowed)

    n_types = len(unique_types)
    if n_types > 6:
        print(f"Found {n_types} types. Plotting only the first 6: {unique_types[:6]}")
        unique_types = unique_types[:6]

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.flatten()

    for i, elem_type in enumerate(unique_types):
        ax = axes[i]
        mask = (types_lower == elem_type)
        x = identities[mask]
        y = coverages[mask]

        color = type_colors.get(elem_type, default_color)
        display_name = elem_type.upper()
        ax.scatter(x, y, alpha=0.5, s=8, label=display_name, color=color)

        if len(x) > 1:
            m, b = np.polyfit(x, y, 1)
            ax.plot(x, m * x + b, color="black", linestyle="-", linewidth=1)
            r = np.corrcoef(x, y)[0, 1]
        else:
            r = np.nan

        ax.text(
            52, 95,
            f"r = {r:.2f}",
            fontsize=12,
            fontweight="bold",
            color="black",
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=2)
        )
        ax.set_title(display_name, fontsize=12, fontweight="bold")
        ax.set_xlim(50, 100)
        ax.set_ylim(0, 100)
        ax.tick_params(axis='both', labelsize=12, width=1.5)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight("bold")
        fig.supxlabel("Percent identity to consensus", fontsize=16, fontweight="bold")
        fig.supylabel("Percent coverage", fontsize=16, fontweight="bold")
        plt.tight_layout()


    for j in range(len(unique_types), 6):
        fig.delaxes(axes[j])

    fig.suptitle(f"Identity vs Coverage\n{ref_csv.split('/')[-1]} vs {test_csv.split('/')[-1]}", fontsize=18, y=1.02, fontweight="bold")
    plt.tight_layout()

    plt.savefig(out_name, dpi=300, bbox_inches="tight")
    print(f"Plot saved as: {out_name}")

if __name__ == "__main__":
    main()
