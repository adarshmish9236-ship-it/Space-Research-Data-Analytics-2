#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("date") or line.startswith("demand_id"):
        continue
    parts = line.split(",")
    if len(parts) >= 7:
        try:
            eq_type = parts[3].strip()
            units = float(parts[4])
            cost = float(parts[5])
            val = float(parts[6])
            print("{0}\t{1}\t{2}\t{3}\t1".format(eq_type, units, cost, val))
        except ValueError:
            continue
