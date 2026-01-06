#!/usr/bin/env python3
"""
Usage:
    python create_new_csv_frag_ana.py inserts.txt ref.csv output.csv

Description:
    Creates a new CSV containing only entries present in both the TXT and CSV files,
    matched by end position (the 2nd integer on each alignment line in TXT and the 4th column in CSV).

    The input CSV has NO header row.
    The output CSV will have the same structure (no header) with one additional
    final column containing percent identity values.
"""

import sys
import re
import pandas as pd

def parse_txt_for_identities(txt_path):
    """
    Parses the alignment .txt file.
    Returns a dict mapping {end_position: percent_identity}.
    """
    results = {}
    with open(txt_path, "r") as f:
        lines = [line.rstrip("\n") for line in f]

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        match = re.match(r"^(\d+)\s+(\d+)", line)
        if match:
            end = int(match.group(2))

            # Find alignment line (contains ||, i, v, d)
            align_line = None
            for j in range(i + 1, len(lines)):
                if re.search(r"[|ivd]", lines[j]):
                    align_line = lines[j]
                    i = j
                    break

            if align_line:
                stripped = align_line.replace(" ", "")
                total_len = len(stripped)
                num_matches = stripped.count("|")
                pct_identity = (num_matches / total_len) * 100 if total_len > 0 else 0.0
                results[end] = pct_identity
        i += 1

    return results


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    txt_file = sys.argv[1]
    csv_file = sys.argv[2]
    out_file = sys.argv[3]

    print(f"Reading TXT: {txt_file}")
    txt_identities = parse_txt_for_identities(txt_file)
    print(f"Found {len(txt_identities)} alignments with percent identity values.\n")

    print(f"Reading CSV (no header): {csv_file}")
    df = pd.read_csv(csv_file, header=None)
    if df.shape[1] < 4:
        raise ValueError(f"CSV file {csv_file} must have at least 4 columns (end position in 4th).")

    csv_end_positions = df.iloc[:, 3].astype(int)

    identities = []
    matched = 0
    for end in csv_end_positions:
        if end in txt_identities:
            identities.append(txt_identities[end])
            matched += 1
        else:
            identities.append(None)

    df[len(df.columns)] = identities

    df_filtered = df[df[len(df.columns) - 1].notna()].copy()

    print(f"Matched {matched} entries between TXT and CSV.")
    print(f"Writing output (no header) to: {out_file}")

    df_filtered.to_csv(out_file, header=False, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
