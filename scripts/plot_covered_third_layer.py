#!/usr/bin/env python3

# call like python3 plot_covered_third_layer.py "homSap EDTA" test_output/output.html test_output/output.csv 100000000 homSap_wg_Garlic.csv homSap_wg_EDTA.csv

import sys
import os
import csv
import plotly.graph_objects as go


def build_list(csv_file, seq_len):
    arr = [0] * seq_len
    with open(csv_file, 'r') as fh:
        for line in fh:
            elem = line.rstrip().split(",")
            start = int(elem[2])
            end = int(elem[3])
            for i in range(start - 1, end):
                arr[i] += 1
    return arr


def load_test_elements(csv_file):
    elems = []
    with open(csv_file, 'r') as fh:
        reader = csv.reader(fh)
        for row in reader:
            if row:
                start = int(row[2])
                end = int(row[3])
                te_type = row[4].strip().lower()
                elems.append((start, end, te_type))
    return elems


def classify_overlap(ref_start, ref_end, ref_type, test_elems):
    overlapping_types = []

    for t_start, t_end, t_type in test_elems:
        if t_end < ref_start or t_start > ref_end:
            continue
        overlapping_types.append(t_type)

    if not overlapping_types:
        return "none"

    return "same" if ref_type in overlapping_types else "diff"


def main():

    if len(sys.argv) < 7:
        print("Usage: script model output_html output_csv seq_len ref.csv test.csv")
        sys.exit(1)

    model = sys.argv[1]
    save_html = sys.argv[2]
    save_csv = sys.argv[3]
    seq_len = int(sys.argv[4])
    ref_csv = sys.argv[5]
    test_csv = sys.argv[6]

    os.makedirs(os.path.dirname(save_csv), exist_ok=True)
    if os.path.dirname(save_html):
        os.makedirs(os.path.dirname(save_html), exist_ok=True)

    query_list = build_list(test_csv, seq_len)
    test_elems = load_test_elements(test_csv)

    total = {}
    covered = {}
    same = {}

    ref_rows = []
    with open(ref_csv, 'r') as fh:
        for row in csv.reader(fh):
            if row:
                ref_rows.append(row)

    with open(save_csv, 'w', newline='') as out:
        writer = csv.writer(out)

        for line in ref_rows:

            rstart = int(line[2])
            rend = int(line[3])
            rtype = line[4].strip().lower()

            if rtype in ["non-te", "unknown"]:
                continue

            length = rend - rstart + 1

            cov_bp = 0
            for i in range(rstart - 1, rend):
                if query_list[i] == 1:
                    cov_bp += 1

            cov_p = cov_bp / length

            for d in (total, covered, same):
                d.setdefault(rtype, 0)

            total[rtype] += 1

            if cov_p > 0.8:
                covered[rtype] += 1
                writer.writerow(line + [f"{cov_p:.6f}"])

                cls = classify_overlap(rstart, rend, rtype, test_elems)

                if cls == "same":
                    same[rtype] += 1

    print(f"Generated: {save_csv}")

    # ---------------- SUNBURST ----------------

    labels = []
    parents = []
    values = []
    ids = []
    node_type = []

    root = model

    labels.append(root)
    parents.append("")
    values.append(sum(total.values()))
    ids.append("root")
    node_type.append(None)

    type_colors = {
        "dna": "#CB3A2B",
        "ltr": "#E9C716",
        "line": "#5F9ED1",
        "line-dependent": "#41B7A8"
    }

    for t in total:

        # TYPE
        labels.append(t)
        parents.append("root")     
        values.append(total[t])
        ids.append(f"{t}_type")
        node_type.append(t)

        # COVERED
        labels.append(f"{t}_covered")
        parents.append(f"{t}_type")   
        values.append(covered[t])
        ids.append(f"{t}_covered")
        node_type.append(t)

        # SAME
        labels.append(f"{t}_same")
        parents.append(f"{t}_covered") 
        values.append(same[t])
        ids.append(f"{t}_same")
        node_type.append(t)

    colors = [type_colors.get(t, "#999999") if t else "white" for t in node_type]

    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=colors),
        branchvalues="total"
    ))

    fig.update_layout(
        title=f"{model} TE Coverage & Classification Accuracy",
        margin=dict(t=50, l=0, r=0, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        uniformtext=dict(minsize=14, mode="show")
    )

    fig.update_traces(textinfo="label+percent entry")

    fig.write_html(save_html)
    print(f"Generated: {save_html}")

    png_path = os.path.splitext(save_html)[0] + ".png"
    fig.write_image(png_path, width=1200, height=1200, scale=3)
    print(f"Generated: {png_path}")


if __name__ == "__main__":
    main()
