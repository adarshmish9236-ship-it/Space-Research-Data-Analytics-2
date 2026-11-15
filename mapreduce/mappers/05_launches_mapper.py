#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 05
Domain: Launch Activities
Mapper: 05_launches_mapper.py

Extracts launch mission activity metrics grouped by year.
Emits:
    key:   year
    value: launch_cost_m,payload_kg,is_success,is_commercial,1
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

        if not fields or len(fields) < 12:
            continue

        if fields[0].strip().lower() in ('launch_id', 'id'):
            continue

        year_str = fields[3].strip()
        if not year_str:
            continue

        try:
            year = int(year_str)
            if year < 1957 or year > 2035:
                continue

            cost = float(fields[10].strip()) if fields[10].strip() else 0.0
            payload = float(fields[11].strip()) if fields[11].strip() else 0.0
            outcome = fields[8].strip().lower()
            is_success = 1 if outcome in ('success', 'successful') else 0
            comm_flag = fields[9].strip().lower()
            is_comm = 1 if comm_flag in ('1', 'true', 'commercial', 'yes') else 0

            if cost <= 0:
                continue

            sys.stdout.write(
                "{:d}\t{:.2f},{:.1f},{:d},{:d},1\n".format(
                    year, cost, payload, is_success, is_comm
                )
            )
        except (ValueError, IndexError):
            continue

if __name__ == '__main__':
    main()

