#!/usr/bin/env python3
"""
Hadoop Streaming Mapper: Space Missions
Reads space_missions.csv lines, outputs Key-Value pairs: Agency \t 1 \t Budget \t Payload \t Status
"""
import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    is_header = True
    for row in reader:
        if not row:
            continue
        if is_header:
            is_header = False
            continue
        # Columns: mission_id,mission_name,agency,country,mission_type,launch_date,launch_year,mission_status,mission_budget_million_usd,payload_mass_kg,mission_duration_days,orbit_type,destination,data_source,is_synthetic
        if len(row) >= 10:
            agency = row[2].strip()
            status = row[7].strip()
            try:
                budget = float(row[8].strip())
            except (ValueError, IndexError):
                budget = 0.0
            try:
                payload = float(row[9].strip())
            except (ValueError, IndexError):
                payload = 0.0
            
            print(f"{agency}\t1\t{budget}\t{payload}\t{status}")

if __name__ == "__main__":
    main()

