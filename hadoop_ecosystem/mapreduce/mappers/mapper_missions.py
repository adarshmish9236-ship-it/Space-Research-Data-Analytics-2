#!/usr/bin/env python3
"""
Mapper: Mission and Agency Aggregation
Handles quoted CSV tokens cleanly.
"""
import sys
import csv

def mapper():
    reader = csv.reader(sys.stdin)
    is_header = True
    for row in reader:
        if not row:
            continue
        if is_header:
            is_header = False
            continue
        # Columns: mission_id,mission_name,agency,mission_type,launch_date,year,quarter,budget_million_usd,payload_mass_kg,status,crew_size,duration_days
        if len(row) >= 10:
            agency = row[2].strip()
            status = row[9].strip()
            try:
                budget = float(row[7].strip())
            except (ValueError, IndexError):
                budget = 0.0
            try:
                payload = float(row[8].strip())
            except (ValueError, IndexError):
                payload = 0.0
            
            print(f"{agency}\t1\t{budget}\t{payload}\t{status}")

if __name__ == "__main__":
    mapper()
