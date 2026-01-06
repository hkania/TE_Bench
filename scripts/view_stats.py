#!/usr/bin/env python3
"""
view_stats.py

Usage:
    python3 view_stats.py input.stats output.pdf seq_name coverage
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

def read_stats(file_path):
    stats_dict = {}
    current_label = None

    with open(file_path, 'r') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            if ':' in line:
                label = line.split(':')[0].strip()
                if label.lower().startswith('stats '):
                    label = label[6:].strip()
                current_label = label
                continue

            if current_label:
                try:
                    values = [float(x.strip()) for x in line.split(',')]
                    stats_dict[current_label] = values
                    print(f"Line {i}: Parsed values for '{current_label}': {values}", flush = True)
                    current_label = None
                except ValueError:
                    print(f"Line {i}: Could not parse numbers for '{current_label}', skipping line", flush = True)
                    continue
    return stats_dict

stats_file = sys.argv[1]
save_file = sys.argv[2]
model = sys.argv[3]
coverage = sys.argv[4]

stats_dict = read_stats(stats_file)

if not stats_dict:
    print("DEBUG: File content could not be parsed correctly:")
    with open(stats_file) as f:
        for i, line in enumerate(f):
            print(f"{i+1}: {line.strip()}")
    raise ValueError("No valid stats found in the file!")

stat_labels = ['MCC', 'Sens', 'Spec', 'Acc', 'Prec', 'FDR', 'F1']
num_stats = len(stat_labels)

ideal_values = [1, 1, 1, 1, 1, 0, 1]

angles = np.linspace(0, 2 * np.pi, num_stats, endpoint=False).tolist()

angles += angles[:1]
ideal_values += ideal_values[:1]

fig, ax = plt.subplots(figsize=(6, 6), dpi=100, subplot_kw=dict(polar=True))

colors = plt.cm.tab10.colors

for idx, (method, values) in enumerate(stats_dict.items()):
    if not values:
        print(f"Warning: Method '{method}' has no numeric values and will be skipped.")
        continue
    if len(values) != num_stats:
        print(f"Warning: Method '{method}' has {len(values)} stats, expected {num_stats}. Skipping.")
        continue
    values = values + values[:1]
    color = colors[idx % len(colors)]
    ax.plot(angles, values, color=color, linewidth=1.5, linestyle='solid', label=method)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(stat_labels, fontsize=12)

ax.set_ylim(0, 1)
ax.set_yticks([0.0, 0.3, 0.5, 0.8, 1.0])
ax.set_yticklabels(['0.0', '0.3', '0.5', '0.8', '1.0'], fontsize=10)

ax.set_title(f"{coverage} Metric Scores for {model}", fontsize = 13, fontweight='bold')
ax.legend(loc='upper right', bbox_to_anchor=(1.1, 0.9), fontsize=10)

plt.savefig(save_file)
print(f"Saved radar plot to {save_file}")
