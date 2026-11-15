#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("mission_id"):
        continue
    parts = line.split(",")
    if len(parts) >= 12:
        try:
            agency = parts[2].strip()
            budget = float(parts[7])
            payload = float(parts[8])
            duration = float(parts[11])
            print("{0}\t1\t{1}\t{2}\t{3}".format(agency, budget, payload, duration))
        except ValueError:
            continue
