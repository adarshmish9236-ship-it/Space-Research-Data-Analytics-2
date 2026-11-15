#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 06
Domain: Manufacturing Requirements
Mapper: 06_manufacturing_mapper.py

Extracts manufacturing quantities by component / subsystem.
Supports both equipment demand manufacturing records and satellite manufacturing orders.
Emits:
    key:   component_name
    value: units_manufactured,cost_k_usd,1
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

        if not fields:
            continue

        header_candidate = fields[0].strip().lower()
        if header_candidate in ('demand_id', 'order_id', 'id'):
            continue

        component_name = None
        units_mfg = 0.0
        cost_k = 0.0

        if len(fields) >= 16:
            # Equipment component demand format
            component_name = fields[6].strip()
            try:
                units_mfg = float(fields[12].strip()) if fields[12].strip() else 0.0
                cost_k = float(fields[15].strip()) if fields[15].strip() else 0.0
            except ValueError:
                continue
        elif len(fields) >= 9:
            # Satellite manufacturing requirements format
            component_name = fields[3].strip()
            try:
                units_mfg = float(fields[4].strip()) if fields[4].strip() else 0.0
                cost_m = float(fields[8].strip()) if fields[8].strip() else 0.0
                cost_k = cost_m * 1000.0
            except ValueError:
                continue

        if not component_name or units_mfg < 0:
            continue

        sys.stdout.write(
            "{}\t{:.1f},{:.2f},1\n".format(
                component_name, units_mfg, cost_k
            )
        )

if __name__ == '__main__':
    main()

