#!/usr/bin/env python3
"""
Hadoop Streaming Mapper: Launch Activities
Outputs: Year::Vehicle \t 1 \t SuccessFlag \t PayloadKg \t CostMillion
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
        # launch_id,launch_date,year,agency,country,launch_site,vehicle,payload_to_orbit_kg,launch_cost_million_usd,launch_outcome,commercial_flag,mission_category,data_source,is_synthetic
        if len(row) >= 10:
            year = row[2].strip()
            vehicle = row[6].strip()
            outcome = row[9].strip()
            try:
                payload = float(row[7].strip())
            except ValueError:
                payload = 0.0
            try:
                cost = float(row[8].strip())
            except ValueError:
                cost = 0.0

            succ = 1 if outcome == "Success" else 0
            print(f"{year}::{vehicle}\t1\t{succ}\t{payload}\t{cost}")

if __name__ == "__main__":
    main()

