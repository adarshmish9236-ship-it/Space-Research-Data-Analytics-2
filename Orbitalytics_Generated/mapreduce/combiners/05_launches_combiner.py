#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 05
Domain: Launch Activities
Combiner: 05_launches_combiner.py

Associative combiner locally summing launch counts, costs, and success counters.
Emits:
    key:   year
    value: launch_cost_m,payload_kg,is_success,is_commercial,count
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
                sys.stdout.write(
                    "{}\t{:.2f},{:.1f},{:d},{:d},{:d}\n".format(
                        current_key, tot_cost, tot_payload, tot_success, tot_comm, tot_count
                    )
                )
            current_key = key
            tot_cost = cost
            tot_payload = payload
            tot_success = succ
            tot_comm = comm
            tot_count = cnt

    if current_key is not None:
        sys.stdout.write(
            "{}\t{:.2f},{:.1f},{:d},{:d},{:d}\n".format(
                current_key, tot_cost, tot_payload, tot_success, tot_comm, tot_count
            )
        )

if __name__ == '__main__':
    main()
