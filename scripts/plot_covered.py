#!/usr/bin/env python3
"""
plot_covered.py

Usage:
    python3 plot_covered.py seq_name output_pdf output_csv seq_len reference.csv test.csv extra_TEs

"""

import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import matplotlib.patheffects as pe
from matplotlib.transforms import Affine2D


def build_list(csv_file, seq_len):
    list = [0] * seq_len

    with open(csv_file, 'r') as csv_fh:
        for line in csv_fh:
            elem = line.rstrip().split(",")
            start = int(elem[2])
            end = int(elem[3])

            for i in range(start - 1, end):
                list[i] += 1

    return list

def basename_no_ext(path):
    return os.path.splitext(os.path.basename(path))[0]

# Center label helper

def get_center_label(csv_file):
    with open(csv_file, 'r') as fh:
        reader = csv.reader(fh)
        for line in reader:
            if line:
                return line[1]
    return ""

# MAIN LOGIC

def main():

    if len(sys.argv) < 7:
        print("Usage: python3 plot_covered.py seq_name pdf_csv coverage_csv seq_len reference.csv test.csv")
        sys.exit(1)

    model = sys.argv[1]
    save_pdf = sys.argv[2]
    save_csv = sys.argv[3]
    seq_len = int(sys.argv[4])
    ref_csv = sys.argv[5]
    test_csv = sys.argv[6]

    extras = []
    if len(sys.argv) > 7:
        extras = sys.argv[7].split(",")

    os.makedirs(os.path.dirname(save_csv), exist_ok=True)
    os.makedirs(os.path.dirname(save_pdf), exist_ok=True)
    
    type_colors = {
        "dna": "#CB3A2B",
        "ltr": "#E9C716",
        "line": "#5F9ED1",
        "line-dependent": "#41B7A8"
    }
    default_color = "#808080"

    extras = [e.lower() for e in extras]
    all_types_allowed = list(type_colors.keys()) + extras

    ref_rows = []
    with open(ref_csv, 'r', newline='') as fh:
        reader = csv.reader(fh)
        for row in reader:
            if row:
                ref_rows.append(row)

    header_row = None
    start_index = 0
    if ref_rows:
        first = ref_rows[0]
        try:
            _ = int(first[2])
        except Exception:
            header_row = first
            start_index = 1

    # Process each test CSV independently

    query_list = build_list(test_csv, seq_len)
    center_label = get_center_label(test_csv)

    total_counts = {}
    covered_counts = {}
    zero_counts = {}

    with open(save_csv, 'w', newline='') as out_fh:
        writer = csv.writer(out_fh)

        if header_row is not None:
            writer.writerow(header_row + ["p_coverage"])

        perfect_coverage_count = 0
        coverage_count = 0
        elem_coverage_list = []

        for line in ref_rows[start_index:]:

            ref_start = int(line[2])
            ref_end   = int(line[3])

            elem_perfect_coverage_count = ref_end - ref_start + 1
            perfect_coverage_count += elem_perfect_coverage_count

            elem_coverage_count = 0
            for i in range(ref_start - 1, ref_end):
                if query_list[i] == 1:
                    elem_coverage_count += 1

            coverage_count += elem_coverage_count

            coverage_p = elem_coverage_count / elem_perfect_coverage_count
            elem_coverage_list.append(coverage_p)

            te_type = line[4].strip().lower()
            if te_type == "non-te" or te_type == "unknown":
                continue

            if te_type not in total_counts:
                total_counts[te_type]  = 0
                covered_counts[te_type] = 0
                zero_counts[te_type]    = 0

            total_counts[te_type] += 1

                # Write only if coverage > 0.8
            if coverage_p > 0.8:
                writer.writerow(line + [f"{coverage_p:.6f}"])
                covered_counts[te_type] += 1
            else:
                zero_counts[te_type] += 1

    all_types_found = list(total_counts.keys())
    labels = [t for t in all_types_allowed if t in all_types_found]
    labels += [t for t in all_types_found if t not in labels]

    inner_sizes = [total_counts[t] for t in labels]

    outer_sizes = []
    outer_colors = []
    for t in labels:
        color = type_colors.get(t, default_color)
        cov   = covered_counts.get(t, 0)
        zero  = zero_counts.get(t, 0)
        outer_sizes.extend([cov, zero])
        outer_colors.extend([color, "white"])

    inner_labels = []
    for t in labels:
        total = total_counts[t]
        covered = covered_counts.get(t, 0)
        percent = 100 * covered / total if total > 0 else 0
        inner_labels.append(f"{t.upper()} – {percent:.1f}%")

    center_label = get_center_label(test_csv)






# Plot
    fig, ax = plt.subplots(figsize=(8, 8))

    wedges_inner, _ = ax.pie(
        inner_sizes,
        labels=None,
        startangle=180,
        counterclock=False,
        radius=0.7,
        wedgeprops=dict(width=0.3, edgecolor="black", linewidth=1.5),
        colors=[type_colors.get(t, default_color) for t in labels]
    )

    wedges_outer, _ = ax.pie(
        outer_sizes,
        startangle = 180,
        counterclock=False,
        radius=1.0,
        wedgeprops=dict(width=0.3, edgecolor="black", linewidth=1.5),
        colors=outer_colors
    )

    outer_index = 0
    for t in labels:
        covered = covered_counts[t]
        total = total_counts[t]
        percent = (covered / total) * 100 if total > 0 else 0.0

        wedge = wedges_outer[outer_index]
        angle = 0.5 * (wedge.theta1 + wedge.theta2)
        x = 0.85 * np.cos(np.deg2rad(angle))
        y = 0.85 * np.sin(np.deg2rad(angle))

        ax.text(
            x, y, f"{percent:.1f}%",
            ha="center", va="center", multialignment='center',
            fontsize=12, fontweight="bold"
        )

        outer_index += 2   # skip the zero/uncovered slice

    for wedge, t in zip(wedges_inner, labels):
        if t == "line-dependent":
            label = "LINE-\nDEP."
        else:
            label = t.upper()

        mid_angle = 0.5 * (wedge.theta1 + wedge.theta2)
        mid_rad = np.deg2rad(mid_angle)

        label_r = 0.55
        x = label_r * np.cos(mid_rad)
        y = label_r * np.sin(mid_rad)

        rot = mid_angle
        rot = ((rot + 180) % 360) - 180
        if rot < -90:
            rot += 180
        elif rot > 90:
            rot -= 180

        ax.text(
            x, y, label,
            ha="center", va="center",
            fontsize=12, fontweight="bold",
            rotation_mode='anchor'
        )

    ax.text(
        0, 0, center_label,
        ha="center", va="center",
        fontsize=14, fontweight="bold"
    )

    ax.set(aspect="equal")
    ax.set_title("Percent of " + model + " TEs covered", fontsize=18, fontweight='bold')
    plt.savefig(save_pdf, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Generated: {save_csv}")
    print(f"Generated: {save_pdf}")


if __name__ == "__main__":
    main()
