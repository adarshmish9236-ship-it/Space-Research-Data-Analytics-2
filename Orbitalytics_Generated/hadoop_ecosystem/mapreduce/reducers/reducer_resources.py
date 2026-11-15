#!/usr/bin/env python3
"""
Hadoop Streaming Reducer: Resource Consumption
Aggregates total consumption and expenditure per resource type.
"""
import sys

current_resource = None
total_qty = 0.0
total_cost = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) < 3:
        continue
    resource, qty_str, cost_str = parts[0], parts[1], parts[2]
    try:
        q = float(qty_str)
        c = float(cost_str)
    except ValueError:
        continue

    if current_resource == resource:
        total_qty += q
        total_cost += c
    else:
        if current_resource:
            cost_m = round(total_cost / 1e6, 2)
            print(f"{current_resource}\t{round(total_qty, 1)}\t{cost_m}")
        current_resource = resource
        total_qty = q
        total_cost = c

if current_resource:
    cost_m = round(total_cost / 1e6, 2)
    print(f"{current_resource}\t{round(total_qty, 1)}\t{cost_m}")

