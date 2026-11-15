#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("date") or line.startswith("consumption_id"):
        continue
    parts = line.split(",")
    if len(parts) >= 7:
        try:
            year = parts[1].strip()
            qty = float(parts[4])
            cost = float(parts[6])
            print("{0}\t{1}\t{2}\t1".format(year, qty, cost))
        except ValueError:
            continue
