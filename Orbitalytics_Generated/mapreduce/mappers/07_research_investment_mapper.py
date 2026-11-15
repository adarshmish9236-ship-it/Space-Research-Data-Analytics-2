#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 07
Domain: Agency Research & Infrastructure Expenditure
Mapper: 07_research_investment_mapper.py

Extracts research and development investment metrics by agency and year.
Emits:
    key:   agency_name::year
    value: rd_m,infra_m,ops_m,total_m,1
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

        if fields[0].strip().lower() in ('expenditure_id', 'id', 'project_id'):
            continue

        agency = fields[6].strip()
        year_str = fields[2].strip()

        if not agency or not year_str:
            continue

        try:
            year = int(year_str)
            if year < 1957 or year > 2035:
                continue

            rd = float(fields[8].strip()) if fields[8].strip() else 0.0
            infra = float(fields[9].strip()) if fields[9].strip() else 0.0
            ops = float(fields[10].strip()) if fields[10].strip() else 0.0
            total = float(fields[11].strip()) if fields[11].strip() else (rd + infra + ops)

            if total <= 0:
                continue

            composite_key = "{}::{:d}".format(agency, year)
            sys.stdout.write(
                "{}\t{:.2f},{:.2f},{:.2f},{:.2f},1\n".format(
                    composite_key, rd, infra, ops, total
                )
            )
        except (ValueError, IndexError):
            continue

if __name__ == '__main__':
    main()
