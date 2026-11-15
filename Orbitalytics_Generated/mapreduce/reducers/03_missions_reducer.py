#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 03
Domain: Space Missions
Reducer: 03_missions_reducer.py

Aggregates space mission intelligence by space agency.
Outputs tab-separated analytical records:
    agency_name \t total_missions \t successful_missions \t success_rate_pct \t total_budget_m \t avg_budget_m \t total_payload_kg \t avg_payload_kg \t total_crew \t avg_duration_days
"""

import sys

def main():
    current_key = None
    tot_budget = 0.0
    tot_payload = 0.0
    tot_crew = 0
    tot_duration = 0.0
    tot_success = 0
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
            b_s, p_s, c_s, d_s, succ_s, cnt_s = val_str.split(',')
            budget = float(b_s)
            payload = float(p_s)
            crew = int(c_s)
            duration = float(d_s)
            succ = int(succ_s)
            cnt = int(cnt_s)
        except (ValueError, IndexError):
            continue

        if current_key == key:
            tot_budget += budget
            tot_payload += payload
            tot_crew += crew
            tot_duration += duration
            tot_success += succ
            tot_count += cnt
        else:
            if current_key is not None:
                emit_aggregation(current_key, tot_budget, tot_payload, tot_crew, tot_duration, tot_success, tot_count)
            current_key = key
            tot_budget = budget
            tot_payload = payload
            tot_crew = crew
            tot_duration = duration
            tot_success = succ
            tot_count = cnt

    if current_key is not None:
        emit_aggregation(current_key, tot_budget, tot_payload, tot_crew, tot_duration, tot_success, tot_count)

def emit_aggregation(key, budget, payload, crew, duration, success, count):
    success_rate = ((success / count) * 100.0) if count > 0 else 0.0
    avg_budget = (budget / count) if count > 0 else 0.0
    avg_payload = (payload / count) if count > 0 else 0.0
    avg_duration = (duration / count) if count > 0 else 0.0

    sys.stdout.write(
        "{}\t{:d}\t{:d}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.1f}\t{:.1f}\t{:d}\t{:.1f}\n".format(
            key,
            count,
            success,
            success_rate,
            budget,
            avg_budget,
            payload,
            avg_payload,
            crew,
            avg_duration
        )
    )

if __name__ == '__main__':
    main()
