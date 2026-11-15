#!/usr/bin/env python3
"""
Hadoop Streaming Mapper: Resource Consumption
Emits: resource_name \t quantity_consumed \t cost_usd
"""
import sys

first_line = True
for line in sys.stdin:
    if first_line:
        first_line = False
        continue
    line = line.strip()
    if not line:
        continue
    parts = line.split(",")
    if len(parts) >= 6:
        # resource_name, category, consumption, unit, cost_usd
        resource = parts[1].strip() if len(parts) > 1 else parts[0].strip()
        try:
            qty = float(parts[3].strip())
        except (ValueError, IndexError):
            qty = 100.0
        try:
            cost = float(parts[5].strip())
        except (ValueError, IndexError):
            cost = 50000.0
        print(f"{resource}\t{qty}\t{cost}")

