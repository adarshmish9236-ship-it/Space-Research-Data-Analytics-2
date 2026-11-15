#!/usr/bin/env python3
import sys

current_key = None
total_units = 0.0
total_val = 0.0
lead_time_sum = 0.0
count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 5:
        continue
    key, units, val, lt, cnt = parts[0], float(parts[1]), float(parts[2]), float(parts[3]), int(parts[4])

    if current_key == key:
        total_units += units
        total_val += val
        lead_time_sum += lt
        count += cnt
    else:
        if current_key is not None:
            avg_lt = lead_time_sum / count if count > 0 else 0.0
            k_parts = current_key.split("#")
            print("{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4:.2f}".format(k_parts[0], k_parts[1], total_units, total_val, avg_lt))
        current_key = key
        total_units = units
        total_val = val
        lead_time_sum = lt
        count = cnt

if current_key is not None:
    avg_lt = lead_time_sum / count if count > 0 else 0.0
    k_parts = current_key.split("#")
    print("{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4:.2f}".format(k_parts[0], k_parts[1], total_units, total_val, avg_lt))
