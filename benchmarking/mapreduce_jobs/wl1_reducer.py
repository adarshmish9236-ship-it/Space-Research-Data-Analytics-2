#!/usr/bin/env python3
import sys

current_key = None
total_units = 0.0
cost_sum = 0.0
total_val = 0.0
count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 5:
        continue
    key, units, cost, val, cnt = parts[0], float(parts[1]), float(parts[2]), float(parts[3]), int(parts[4])

    if current_key == key:
        total_units += units
        cost_sum += cost
        total_val += val
        count += cnt
    else:
        if current_key is not None:
            avg_cost = cost_sum / count if count > 0 else 0.0
            print("{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4}".format(current_key, total_units, avg_cost, total_val, count))
        current_key = key
        total_units = units
        cost_sum = cost
        total_val = val
        count = cnt

if current_key is not None:
    avg_cost = cost_sum / count if count > 0 else 0.0
    print("{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4}".format(current_key, total_units, avg_cost, total_val, count))
