#!/usr/bin/env python3
"""
calculate_overlap_csvs.py

Usage:
    python3 calculate_overlap_csvs.py ref.csv seq_len host_output.csv nest_output.csv

"""

import sys
import csv
import os

def build_list(csv, seq_len):
    list = [0] * seq_len

    with open(csv, 'r') as csv_fh:        
        for line in csv_fh:
            elem = line.rstrip().split(",")
            start = int(elem[2])
            end = int(elem[3])

            for i in range(start - 1, end):
                list[i] += 1

    return list


def calculate_overlap(input_csv, list, minor_nest_csv, major_nest_csv):
    minor_nest_rows = []
    major_nest_rows = []

    with open(input_csv, 'r') as csv_fh:  
        csv_reader = csv.reader(csv_fh)

        for line in csv_reader:

            overlap = "no"
            p_overlap = 0
            num_overlaps = 0
            
            start = int(line[2])
            end = int(line[3])

            for i in range(start - 1, end):
                if list[i] >= 2:
                    if overlap == "no":
                        overlap = "yes"
                    num_overlaps += 1
            
            if overlap == "yes":
                p_overlap = num_overlaps / (end - start + 1)

            line.append(overlap)
            line.append(p_overlap)

            if p_overlap == 1.0:
                minor_nest_rows.append(line)
            elif p_overlap > 0 and p_overlap < 1.0:
                major_nest_rows.append(line)
        
    with open(minor_nest_csv, 'w', newline='') as csv_fh:
        csv_writer = csv.writer(csv_fh)
        csv_writer.writerows(minor_nest_rows)

    with open(major_nest_csv, 'w', newline='') as csv_fh:
        csv_writer = csv.writer(csv_fh)
        csv_writer.writerows(major_nest_rows)                


def main():

    input_csv = sys.argv[1]
    seq_len = int(sys.argv[2])
    minor_nest = sys.argv[3]
    major_nest = sys.argv[4]

    overlap_list = build_list(input_csv, seq_len)

    calculate_overlap(input_csv, overlap_list, minor_nest, major_nest)


if __name__ == "__main__":
    main()
