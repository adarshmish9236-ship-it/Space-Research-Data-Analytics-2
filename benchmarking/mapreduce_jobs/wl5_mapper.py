#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split(",")

    if len(parts) >= 12 and not parts[0].startswith("mission_id"):
        try:
            agency = parts[2].strip()
            year = parts[5].strip()
            budget = float(parts[7])
            key = "{0}#{1}".format(agency, year)
            print("{0}\tM\t{1}".format(key, budget))
        except (ValueError, IndexError):
            continue

    elif len(parts) == 8 and not parts[0].startswith("date"):
        try:
            year = parts[1].strip()
            agency = parts[3].strip()
            exp = float(parts[7])
            key = "{0}#{1}".format(agency, year)
            print("{0}\tE\t{1}".format(key, exp))
        except (ValueError, IndexError):
            continue
