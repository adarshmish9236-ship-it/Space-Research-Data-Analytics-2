#!/usr/bin/env python3
"""
Reducer: Equipment Demand Aggregation
Input: Year::EquipmentType \t UnitsDemanded \t DemandValueMillion
Output: Year \t EquipmentType \t TotalUnits \t TotalDemandValueMillion
"""
import sys

def reducer():
    current_key = None
    total_units = 0
    total_val = 0.0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        
        key, units_str, val_str = parts[0], parts[1], parts[2]
        try:
            units = int(units_str)
            val = float(val_str)
        except ValueError:
            continue

        if current_key == key:
            total_units += units
            total_val += val
        else:
            if current_key is not None:
                year, eq_type = current_key.split("::")
                print(f"{year}\t{eq_type}\t{total_units}\t{round(total_val, 2)}")
            current_key = key
            total_units = units
            total_val = val

    if current_key is not None:
        year, eq_type = current_key.split("::")
        print(f"{year}\t{eq_type}\t{total_units}\t{round(total_val, 2)}")

if __name__ == "__main__":
    reducer()

