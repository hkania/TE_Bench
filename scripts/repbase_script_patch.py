#!/usr/bin/env python3
"""
repbase_script_patch.py

Usage:
    python3 ./repbase_script_patch.py scripts/createFakeSequence_repbase repbase_version output_file

"""

import sys
import os

def patch_repbase_line(script_path, repbase, done_file):
    with open(script_path) as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if repbase and "RepBaseXX.XX.embl" in line:
            line = line.replace("RepBaseXX.XX", repbase)
        new_lines.append(line)

    with open(script_path, "w") as f:
        f.writelines(new_lines)
    print (F"Edited the script: {script_path} with {repbase}")

    if done_file is None:
        done_file = script_path + ".done"

    with open(done_file, "w") as f:
        f.write(f"Patched {script_path} with {repbase}\n")

    print(f"Created .done file: {done_file}")

def main():
    input_script = sys.argv[1] + ".pl"
    input_repbase = sys.argv[2]
    output_file = sys.argv[3]

    patch_repbase_line(input_script, input_repbase, output_file)

if __name__ == "__main__":
    main()
