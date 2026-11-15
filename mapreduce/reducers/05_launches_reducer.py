#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 05
Domain: Launch Activities
Reducer: 05_launches_reducer.py

Aggregates launch activity intelligence by year.
Outputs tab-separated analytical records:
    year \t total_launches \t successful_launches \t success_rate_pct \t commercial_launches \t comm_rate_pct \t total_cost_m \t avg_cost_m \t total_payload_kg \t avg_payload_kg
"""

import sys

def main():
    current_key = None
    tot_cost = 0.0
    tot_payload = 0.0
    tot_success = 0
    tot_comm = 0
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
            c_s, p_s, s_s, cm_s, cnt_s = val_str.split(',')
            cost = float(c_s)
            payload = float(p_s)
            succ = int(s_s)
            comm = int(cm_s)
            cnt = int(cnt_s)
        except (ValueError, IndexError):
            continue

        if current_key == key:
            tot_cost += cost
            tot_payload += payload
            tot_success += succ
            tot_comm += comm
            tot_count += cnt
        else:
            if current_key is not None:
                emit_aggregation(current_key, tot_cost, tot_payload, tot_success, tot_comm, tot_count)
            current_key = key
            tot_cost = cost
            tot_payload = payload
            tot_success = succ
            tot_comm = comm
            tot_count = cnt

    if current_key is not None:
        emit_aggregation(current_key, tot_cost, tot_payload, tot_success, tot_comm, tot_count)

def emit_aggregation(key, cost, payload, success, comm, count):
    success_rate = ((success / count) * 100.0) if count > 0 else 0.0
    comm_rate = ((comm / count) * 100.0) if count > 0 else 0.0
    avg_cost = (cost / count) if count > 0 else 0.0
    avg_payload = (payload / count) if count > 0 else 0.0

    sys.stdout.write(
        "{}\t{:d}\t{:d}\t{:.2f}\t{:d}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.1f}\t{:.1f}\n".format(
            key,
            count,
            success,
            success_rate,
            comm,
            comm_rate,
            cost,
            avg_cost,
            payload,
            avg_payload
        )
    )

if __name__ == '__main__':
    main()

