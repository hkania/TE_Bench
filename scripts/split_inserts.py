#!/usr/bin/env python3
"""
split_inserts.py

Usage:
    python3 split_inserts.py model
"""

import re
import os
import sys

seq_name = sys.argv[1]
input_file = f"output/sim_fastas/{seq_name}/{seq_name}_sim.inserts"

pattern = re.compile(r"### ARTIFICIAL SEQUENCE (\d+) ###")
current_seq = None
current_lines = []

def save_seq(seq_num, lines):
    if seq_num is None:
        return
    outfile = f"output/sim_fastas/{seq_name}/{seq_name}_split/{seq_name}_{seq_num}.inserts"
    with open(outfile, "w") as f:
        f.writelines(lines)

with open(input_file, "r") as f:
    for line in f:
        match = pattern.match(line.strip())
        if match:
            save_seq(current_seq, current_lines)
            current_seq = match.group(1)
            current_lines = [line]
        else:
            if current_seq is not None:
                current_lines.append(line)

# Save last
save_seq(current_seq, current_lines)
