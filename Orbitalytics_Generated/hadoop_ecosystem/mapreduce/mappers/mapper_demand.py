#!/usr/bin/env python3
"""
Hadoop Streaming Mapper: Equipment Demand
Reads equipment_component_demand.csv, outputs: Year::EquipmentType \t Units \t ValueMillion
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
        # date,year,month,equipment_type,equipment_category,units_demanded,avg_unit_cost_thousand_usd,total_demand_value_million_usd,lead_time_days,shortage_risk,agency,country,data_source,is_synthetic
        if len(row) >= 8:
            year = row[1].strip()
            eq_type = row[3].strip()
            try:
                units = int(row[5].strip())
                val = float(row[7].strip())
            except (ValueError, IndexError):
                continue
            print(f"{year}::{eq_type}\t{units}\t{val}")

if __name__ == "__main__":
    main()

