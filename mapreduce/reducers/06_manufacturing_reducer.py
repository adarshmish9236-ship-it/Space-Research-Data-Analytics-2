#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 06
Domain: Manufacturing Requirements
Reducer: 06_manufacturing_reducer.py

Aggregates manufacturing quantities by component.
Outputs tab-separated analytical records:
    component_name \t total_units_manufactured \t avg_units_per_order \t total_cost_k \t total_cost_m \t total_orders
"""

import sys

def main():
    current_key = None
    tot_units = 0.0
    tot_cost_k = 0.0
    tot_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split('\t', 1)
        if len(parts) != 2:
            continue

        key, val_str = parts[0], parts[1]
        try:
            u_s, c_s, cnt_s = val_str.split(',')
            units = float(u_s)
            cost_k = float(c_s)
            cnt = int(cnt_s)
        except (ValueError, IndexError):
            continue

        if current_key == key:
            tot_units += units
            tot_cost_k += cost_k
            tot_count += cnt
        else:
            if current_key is not None:
                emit_aggregation(current_key, tot_units, tot_cost_k, tot_count)
            current_key = key
            tot_units = units
            tot_cost_k = cost_k
            tot_count = cnt

    if current_key is not None:
        emit_aggregation(current_key, tot_units, tot_cost_k, tot_count)

def emit_aggregation(key, units, cost_k, count):
    avg_units = (units / count) if count > 0 else 0.0
    cost_m = cost_k / 1000.0

    sys.stdout.write(
        "{}\t{:.1f}\t{:.2f}\t{:.2f}\t{:.4f}\t{:d}\n".format(
            key,
            units,
            avg_units,
            cost_k,
            cost_m,
            count
        )
    )

if __name__ == '__main__':
    main()

