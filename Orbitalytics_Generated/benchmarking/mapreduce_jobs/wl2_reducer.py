#!/usr/bin/env python3
import sys

current_key = None
total_qty = 0.0
total_cost = 0.0
count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 4:
        continue
    key, qty, cost, cnt = parts[0], float(parts[1]), float(parts[2]), int(parts[3])

    if current_key == key:
        total_qty += qty
        total_cost += cost
        count += cnt
    else:
        if current_key is not None:
            avg_qty = total_qty / count if count > 0 else 0.0
            print("{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4}".format(current_key, total_qty, total_cost, avg_qty, count))
        current_key = key
        total_qty = qty
        total_cost = cost
        count = cnt

if current_key is not None:
    avg_qty = total_qty / count if count > 0 else 0.0
    print("{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4}".format(current_key, total_qty, total_cost, avg_qty, count))
