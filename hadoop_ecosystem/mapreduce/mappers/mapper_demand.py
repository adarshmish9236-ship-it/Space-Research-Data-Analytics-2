#!/usr/bin/env python3
"""
Mapper: Equipment Demand Aggregation
Input: CSV lines of equipment_component_demand.csv
Output: Year-EquipmentType \t UnitsDemanded \t DemandValueMillion
"""
import sys

def mapper():
    is_header = True
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if is_header:
            is_header = False
            continue
        
        parts = [p.strip() for p in line.split(",")]
        # Columns: date,year,month,equipment_type,units_demanded,avg_unit_cost_thousand_usd,total_demand_value_million_usd,lead_time_days,shortage_risk
        if len(parts) >= 7:
            year = parts[1]
            eq_type = parts[3]
            try:
                units = int(parts[4])
                val = float(parts[6])
            except ValueError:
                continue
            
            key = f"{year}::{eq_type}"
            print(f"{key}\t{units}\t{val}")

if __name__ == "__main__":
    mapper()

