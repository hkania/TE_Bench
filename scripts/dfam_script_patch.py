#!/usr/bin/env python3

"""
dfam_script_patch.py

Usage:
    python3 dfam_script_patch.py input_script_prefix dfam_url output_file
"""

import sys
import re


def patch_dfam_line_from_url(script_path, dfam_url, output_file):
    if not dfam_url:
        raise ValueError("No Dfam URL provided")

    basename = dfam_url.rstrip("/").split("/")[-1]


    match = re.match(r"(Dfam.*?)(?=\.embl)", basename)
    if not match:
        raise ValueError(f"Cannot extract Dfam version from URL: {dfam_url}")

    dfam_version = match.group(1)


    with open(script_path, "r") as f:
        lines = f.readlines()

    replaced = False
    new_lines = []

    for line in lines:
        if not replaced and re.search(r"\$repbase_file\s*=", line):
            new_line = re.sub(
                r"Dfam[^/]*\.embl",
                f"{dfam_version}.embl",
                line
            )

            if new_line != line:
                replaced = True
                line = new_line

        new_lines.append(line)

    if not replaced:
        raise RuntimeError("Did not find or modify the $repbase_file line")

    with open(script_path, "w") as f:
        f.writelines(new_lines)

    with open(output_file, "w") as f:
        f.write(f"Patched {script_path} with {dfam_version}\n")

    print(f"Edited the script: {script_path} with {dfam_version}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 dfam_script_patch.py <script_prefix> <dfam_url> <output_file>")
        sys.exit(1)

    input_script = sys.argv[1] + ".pl"
    input_dfam_url = sys.argv[2]
    output_file = sys.argv[3]

    patch_dfam_line_from_url(input_script, input_dfam_url, output_file)


if __name__ == "__main__":
    main()
