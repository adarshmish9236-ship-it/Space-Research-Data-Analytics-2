#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 02
Domain: Resource Consumption
Mapper: 02_resource_consumption_mapper.py

Extracts annual resource consumption metrics.
Emits:
    key:   year::resource_name
    value: quantity_consumed,procurement_cost_k_usd,1
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

        if not fields or len(fields) < 14:
            continue

        if fields[0].strip().lower() in ('consumption_id', 'id'):
            continue

        year_str = fields[2].strip()
        resource_name = fields[6].strip()

        if not year_str or not resource_name:
            continue

        try:
            year = int(year_str)
            if year < 1957 or year > 2035:
                continue

            qty = float(fields[11].strip()) if fields[11].strip() else 0.0
            cost_k = float(fields[13].strip()) if fields[13].strip() else 0.0

            if qty <= 0:
                continue

            composite_key = "{}::{}".format(year, resource_name)
            sys.stdout.write("{}\t{:.2f},{:.2f},1\n".format(composite_key, qty, cost_k))
        except (ValueError, IndexError):
            continue

if __name__ == '__main__':
    main()
