#!/usr/bin/env python3
"""
plot_nesting.py

Usage:
    python3 plot_nesting.py scale_tag ref_full.csv ref_host.csv ref_nest.csv seq_len output_pdf seq_name non_ref1.csv non_ref2.csv ... non_refN.csv
"""

import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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


def assign_bin(value):
    if value < 0.20:
        return "≤20%"
    elif value < 0.40:
        return "20–40%"
    elif value < 0.60:
        return "40–60%"
    elif value < 0.80:
        return "60–80%"
    else:
        return ">80%"


def read_rows_preserve_header(path):
    rows = []
    with open(path, 'r', newline='') as fh:
        reader = csv.reader(fh)
        for row in reader:
            rows.append(row)
    return rows


def compute_coverages_for_ref_rows(ref_rows, query_list):
    p_coverage_list = []

    start_index = 0
    header_row = None
    for i, r in enumerate(ref_rows):
        if r:
            try:
                _ = int(r[2])
            except Exception:
                header_row = r
                start_index = i + 1
            break

    for i in range(start_index):
        p_coverage_list.append(None)

    for r in ref_rows[start_index:]:
        if not r:
            p_coverage_list.append(None)
            continue
        try:
            ref_start = int(r[2])
            ref_end = int(r[3])
        except Exception:
            p_coverage_list.append(None)
            continue

        elem_perfect_coverage_count = ref_end - ref_start + 1
        if elem_perfect_coverage_count <= 0:
            p_coverage_list.append(0.0)
            continue

        elem_coverage_count = 0
        qlen = len(query_list)
        start_idx = max(0, ref_start - 1)
        end_idx = min(ref_end, qlen)

        for i_pos in range(start_idx, end_idx):
            if query_list[i_pos] == 1:
                elem_coverage_count += 1

        coverage_p = elem_coverage_count / elem_perfect_coverage_count
        p_coverage_list.append(coverage_p)

    return p_coverage_list


def write_ref_with_coverage(out_path, ref_rows, p_coverage_list, header_row_present):
    with open(out_path, 'w', newline='') as out_fh:
        writer = csv.writer(out_fh)

        if header_row_present:
            for r, p in zip(ref_rows, p_coverage_list):
                if r and not is_int(r[2]):
                    writer.writerow(r + ["p_coverage"])
                    break

        for r, p in zip(ref_rows, p_coverage_list):
            if not r:
                writer.writerow(r)
            else:
                if header_row_present and not is_int(r[2]):
                    header_row_present = False
                    continue
                val = "" if p is None else f"{p:.6f}"
                writer.writerow(r + [val])


def is_int(x):
    try:
        int(x)
        return True
    except Exception:
        return False


def main():

    scale_tag = sys.argv[1]
    ref_csv = sys.argv[2]
    host_csv = sys.argv[3]
    nest_csv = sys.argv[4]
    save_pdf = sys.argv[6]
    test_csvs = sys.argv[8:]
    model = sys.argv[7]
    
    try:
        seq_len = int(sys.argv[5])
    except ValueError:
        print("seq_len must be an integer")
        sys.exit(1)

    programs = []
    for path in test_csvs:
        base = os.path.basename(path)
        prog_name = "_".join(base.split("_")[1:-1]) if len(base.split("_")) > 2 else base.split("_")[1].split(".")[0]
        programs.append(prog_name)

    ref1_rows = read_rows_preserve_header(host_csv)
    ref2_rows = read_rows_preserve_header(nest_csv)
    ref3_rows = read_rows_preserve_header(ref_csv)
    
    results = {}
    bins = ["≤20%", "20–40%", "40–60%", "60–80%", ">80%"]

    for prog, test_csv in zip(programs, test_csvs):
        identities = build_list(test_csv, seq_len)

        p_cov_ref1 = compute_coverages_for_ref_rows(ref1_rows, identities)
        p_cov_ref2 = compute_coverages_for_ref_rows(ref2_rows, identities)
        p_cov_ref3 = compute_coverages_for_ref_rows(ref3_rows, identities)

        binned1 = [assign_bin(p) for p in p_cov_ref1 if p is not None]
        binned2 = [assign_bin(p) for p in p_cov_ref2 if p is not None]
        binned3 = [assign_bin(p) for p in p_cov_ref3 if p is not None]

        def proportions_from_binned_list(binned_list):
            counts = {b: 0 for b in bins}
            total = 0
            for val in binned_list:
                if val in counts:
                    counts[val] += 1
                    total += 1
            if total == 0:
                return [0.0 for _ in bins], 0
            props = [100.0 * counts[b] / total for b in bins]
            return props, total

        props1, total1 = proportions_from_binned_list(binned1)
        props2, total2 = proportions_from_binned_list(binned2)
        props3, total3 = proportions_from_binned_list(binned3)

        results[prog] = {"all": props3, "host": props1, "nest": props2, "totals": (total3, total1, total2)}

    x = np.arange(len(bins))
    n_prog = len(programs)

    group_width = 0.8
    width = group_width / n_prog

    colors = plt.cm.tab10.colors
    fig, (ax_all, ax_host, ax_nest) = plt.subplots(
        1, 3, figsize=(12, 12), sharex=True
    )

    for i, prog in enumerate(programs):
        color = colors[i % len(colors)]
        offset = (i - (n_prog - 1) / 2) * width

        ax_all.bar(
            x + offset,
            results[prog]["all"],
            width,
            color=color,
            edgecolor="none",
            label=prog
        )

        ax_host.bar(
            x + offset,
            results[prog]["host"],
            width,
            color=color,
            edgecolor="none",
            label=prog
        )

        ax_nest.bar(
            x + offset,
            results[prog]["nest"],
            width,
            color=color,
            edgecolor="none",
            label=prog
        )
        
    leg = ax_all.legend(title="Program", loc="upper left", prop={"size": 12, "weight": "bold"})

    leg.get_title().set_fontsize(12)
    leg.get_title().set_fontweight("bold")

    fig.suptitle(
        f"Coverage distribution of {model} {scale_tag} TEs across programs",
        fontsize=18,
        fontweight="bold"
    )

    fig.supxlabel("Percent coverage", fontsize=16, fontweight="bold")

    ax_host.set_title(
        r"$\it{Host}$",
        fontsize=16
    )

    ax_nest.set_title(
        r"$\it{Nested}$",
        fontsize=16
    )

    ax_all.set_title(
        r"$\it{Non-nested}$",
        fontsize=16,
    )

    fig.supylabel("Percent of elements", fontsize=16, fontweight="bold")

    ax_nest.set_xticks(x)
    ax_nest.set_xticklabels(bins)

    y_min, y_max = 0, 100
    y_ticks = range(0, 101, 10)

    ax_host.set_ylim(y_min, y_max)
    ax_nest.set_ylim(y_min, y_max)
    ax_all.set_ylim(y_min, y_max)
    
    ax_host.set_yticks(y_ticks)
    ax_host.set_yticklabels(y_ticks, fontsize=12, fontweight="bold")
    ax_nest.set_yticks(y_ticks)
    ax_nest.set_yticklabels(y_ticks, fontsize=12, fontweight="bold")
    ax_all.set_yticks(y_ticks)
    ax_all.set_yticklabels(y_ticks, fontsize=12, fontweight="bold")

    plt.tight_layout()
    plt.savefig(save_pdf, dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
