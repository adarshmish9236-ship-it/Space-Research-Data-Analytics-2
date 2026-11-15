#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 02
Domain: Resource Consumption
Reducer: 02_resource_consumption_reducer.py

Aggregates resource consumption by (year, resource_name).
Outputs tab-separated analytical records:
    year \t resource_name \t total_quantity \t total_cost_k_usd \t total_cost_m_usd \t avg_quantity \t event_count
"""

import sys

def main():
    current_key = None
    tot_qty = 0.0
    tot_cost = 0.0
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
            qty_str, cost_str, cnt_str = val_str.split(',')
            qty = float(qty_str)
            cost = float(cost_str)
            cnt = int(cnt_str)
        except (ValueError, IndexError):
            continue

        if current_key == key:
            tot_qty += qty
            tot_cost += cost
            tot_count += cnt
        else:
            if current_key is not None:
                emit_aggregation(current_key, tot_qty, tot_cost, tot_count)
            current_key = key
            tot_qty = qty
            tot_cost = cost
            tot_count = cnt

    if current_key is not None:
        emit_aggregation(current_key, tot_qty, tot_cost, tot_count)

def emit_aggregation(key, qty, cost, count):
    if "::" in key:
        year, resource = key.split("::", 1)
    else:
        year, resource = "UNKNOWN", key

    cost_m = cost / 1000.0
    avg_qty = (qty / count) if count > 0 else 0.0

    sys.stdout.write(
        "{}\t{}\t{:.2f}\t{:.2f}\t{:.4f}\t{:.2f}\t{:d}\n".format(
            year,
            resource,
            qty,
            cost,
            cost_m,
            avg_qty,
            count
        )
    )

if __name__ == '__main__':
    main()
