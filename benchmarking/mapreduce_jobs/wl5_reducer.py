#!/usr/bin/env python3
import sys

current_key = None
mission_count = 0
total_mission_budget = 0.0
total_annual_expenditure = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 3:
        continue
    key, tag, val_str = parts[0], parts[1], parts[2]
    try:
        val = float(val_str)
    except ValueError:
        continue

    if current_key == key:
        if tag == "M":
            mission_count += 1
            total_mission_budget += val
        elif tag == "E":
            total_annual_expenditure += val
    else:
        if current_key is not None and mission_count > 0 and total_annual_expenditure > 0:
            share = (total_mission_budget / total_annual_expenditure) * 100.0
            k_parts = current_key.split("#")
            print("{0}\t{1}\t{2}\t{3:.2f}\t{4:.2f}\t{5:.2f}".format(k_parts[0], k_parts[1], mission_count, total_mission_budget, total_annual_expenditure, share))
        current_key = key
        mission_count = 1 if tag == "M" else 0
        total_mission_budget = val if tag == "M" else 0.0
        total_annual_expenditure = val if tag == "E" else 0.0

if current_key is not None and mission_count > 0 and total_annual_expenditure > 0:
    share = (total_mission_budget / total_annual_expenditure) * 100.0
    k_parts = current_key.split("#")
    print("{0}\t{1}\t{2}\t{3:.2f}\t{4:.2f}\t{5:.2f}".format(k_parts[0], k_parts[1], mission_count, total_mission_budget, total_annual_expenditure, share))
