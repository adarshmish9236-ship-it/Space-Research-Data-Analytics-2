#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 01
Domain: Equipment Component Demand
Mapper: 01_equipment_demand_mapper.py

Extracts component demand metrics from Silver Equipment Demand dataset.
Handles CSV quotation, header skipping, and null safety.
Emits:
    key:   component_name
    value: units_demanded \t units_manufactured \t units_procured \t total_value_million_usd \t lead_time_days \t 1
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

        if not fields or len(fields) < 17:
            continue

        # Skip CSV header if encountered
        if fields[0].strip().lower() in ('demand_id', 'id'):
            continue

        component_name = fields[6].strip()
        if not component_name:
            continue

        try:
            units_demanded = float(fields[11].strip()) if fields[11].strip() else 0.0
            units_manufactured = float(fields[12].strip()) if fields[12].strip() else 0.0
            units_procured = float(fields[13].strip()) if fields[13].strip() else 0.0
            total_value = float(fields[16].strip()) if fields[16].strip() else 0.0
            lead_time = float(fields[17].strip()) if len(fields) > 17 and fields[17].strip() else 0.0

            if units_demanded < 0:
                continue

            # Emit tab-separated key and comma-delimited numeric vector
            sys.stdout.write(
                "{}\t{:.2f},{:.2f},{:.2f},{:.4f},{:.1f},1\n".format(
                    component_name,
                    units_demanded,
                    units_manufactured,
                    units_procured,
                    total_value,
                    lead_time
                )
            )
        except (ValueError, IndexError):
            continue

if __name__ == '__main__':
    main()
