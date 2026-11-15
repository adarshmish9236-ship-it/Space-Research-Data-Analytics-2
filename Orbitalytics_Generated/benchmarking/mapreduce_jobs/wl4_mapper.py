#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("date") or line.startswith("demand_id"):
        continue
    parts = line.split(",")
    if len(parts) >= 8:
        try:
            year = parts[1].strip()
            eq_type = parts[3].strip()
            units = float(parts[4])
            val = float(parts[6])
            lead_time = float(parts[7])
            key = "{0}#{1}".format(eq_type, year)
            print("{0}\t{1}\t{2}\t{3}\t1".format(key, units, val, lead_time))
        except ValueError:
            continue
