#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 03
Domain: Space Missions
Mapper: 03_missions_mapper.py

Extracts mission metrics grouped by space agency.
Emits:
    key:   agency_name
    value: budget_m,payload_kg,crew_size,duration_days,is_success,1
"""

import sys
import csv

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            reader = csv.reader([line])
            fields = next(reader)
        except Exception:
            fields = line.split(',')

        if not fields or len(fields) < 13:
            continue

        if fields[0].strip().lower() in ('mission_id', 'id'):
            continue

        agency_name = fields[3].strip()
        if not agency_name:
            continue

        try:
            budget = float(fields[8].strip()) if fields[8].strip() else 0.0
            payload = float(fields[9].strip()) if fields[9].strip() else 0.0
            crew = int(float(fields[11].strip())) if fields[11].strip() else 0
            duration = float(fields[12].strip()) if fields[12].strip() else 0.0
            status = fields[10].strip().lower()
            is_success = 1 if status in ('completed', 'successful', 'operational') else 0

            if budget <= 0:
                continue

            sys.stdout.write(
                "{}\t{:.2f},{:.2f},{:d},{:.1f},{:d},1\n".format(
                    agency_name, budget, payload, crew, duration, is_success
                )
            )
        except (ValueError, IndexError):
            continue

if __name__ == '__main__':
    main()

