#!/usr/bin/env python3
"""
generate_stats.py

Usage:
    python3 generate_stats.py ref.csv seq_len output.txt non_ref1.csv non_ref2.csv ... non_refN.csv

"""

import sys
import math
import os
import re

def build_list(csv, seq_len):

    lst = [0] * seq_len
    empty = False

    if not os.path.exists(csv):
        print(f"Warning: {csv} not found. Treating as empty.")
        return lst, True

    with open(csv, 'r') as csv_fh:

        lines = [line.strip() for line in csv_fh if line.strip()]

        if not lines:
            empty = True
            return lst, empty

        
        for line in lines:
            elem = line.split(",")
            if len(elem) < 4:
                continue

            start = int(elem[2])
            end = int(elem[3])

            for i in range(start - 1, end):
                lst[i] = 1

    return lst, empty


def get_stats(ref_csv, test_csv, seq_len, te_type=None):
    ref_list, ref_empty = build_list(ref_csv, seq_len)
    test_list, test_empty = build_list(test_csv, seq_len)

    notes = ""

    if ref_empty:
        notes += f"Reference file {ref_csv} has no TEs"
        if te_type:
            notes += f" of type {te_type}"
        notes += ". Sensitivity will be 0.\n"

    if test_empty:
        notes += f"Warning: {test_csv} has no predicted positives — stats may be misleading.\n"

    TP = 0
    FP = 0
    FN = 0
    TN = 0

    for i in range(0, seq_len):
        # TP
        if ref_list[i] == 1 and test_list[i] == 1:
            TP += 1
        
        # FP
        elif ref_list[i] == 0 and test_list[i] == 1:
            FP += 1

        # FN
        elif ref_list[i] == 1 and test_list[i] == 0:
            FN += 1
        
        # TN
        else:
            TN += 1
    
    mcc = (TP * TN - FP * FN) / math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)) if (TP + FP) * (TP + FN) * (TN + FP) * (TN + FN) > 0 else 0
    sens = TP / (TP + FN) if (TP + FN) > 0 else 0
    spec = TN / (FP + TN) if (FP + TN) > 0 else 0
    accu = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0

    if (TP + FP) == 0:
        prec = 0
    else:
        prec = TP / (TP + FP) if (TP + FP) > 0 else 0
    fdr = 1 - prec
    f1 = (2 * TP) / ((2 * TP) + FP + FN) if ((2 * TP) + FP + FN) > 0 else 0

    return([mcc, sens, spec, accu, prec, fdr, f1]), notes

def extract_prog_name(prog_csv, te_type=None):
    base = os.path.basename(prog_csv)
    base = base.replace(".csv", "")
    if te_type and base.endswith(te_type):
        base = base[:-(len(te_type)+1)]
    prog_name = base.rsplit("_", 1)[-1]

    return prog_name

if __name__ == "__main__":

    args = sys.argv[1:]

    if args and args[0].lower().endswith(".csv"):
        te_type = None
        ref_csv = args[0]
        seq_len = int(args[1])
        output_file = args[2]
        prog_csvs = args[3:]
    else:
        te_type = args[0]
        ref_csv = args[1]
        seq_len = int(args[2])
        output_file = args[3]
        prog_csvs = args[4:]

    results = []

    for prog_csv in prog_csvs:
        prog_name = extract_prog_name(prog_csv, te_type)
        stats, notes = get_stats(ref_csv, prog_csv, seq_len, te_type)
        results.append((prog_name, stats, notes))

    with open(output_file, "w") as f:
        f.write("mcc, sens, spec, accu, prec, fdr, f1\n")
        for prog_name, stats, notes in results:
            f.write(f"\nstats {prog_name}:\n")
            f.write(", ".join(map(str, stats)) + "\n")
            if notes:
                f.write(notes + "\n")
