#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 01
Domain: Equipment Component Demand
Combiner: 01_equipment_demand_combiner.py

Demonstrates MapReduce Combiner optimization for associative operations.
Locally pre-aggregates emitted sums and counts before network shuffle.
"""

import sys

def main():
    current_key = None
    tot_demanded = 0.0
    tot_mfg = 0.0
    tot_proc = 0.0
    tot_val = 0.0
    tot_lead = 0.0
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
            vals = [float(x) for x in val_str.split(',')]
            if len(vals) < 6:
                continue
            demanded, mfg, proc, val, lead, cnt = vals[0], vals[1], vals[2], vals[3], vals[4], int(vals[5])
        except (ValueError, IndexError):
            continue

        if current_key == key:
            tot_demanded += demanded
            tot_mfg += mfg
            tot_proc += proc
            tot_val += val
            tot_lead += lead
            tot_count += cnt
        else:
            if current_key is not None:
                sys.stdout.write(
                    "{}\t{:.2f},{:.2f},{:.2f},{:.4f},{:.1f},{:d}\n".format(
                        current_key, tot_demanded, tot_mfg, tot_proc, tot_val, tot_lead, tot_count
                    )
                )
            current_key = key
            tot_demanded = demanded
            tot_mfg = mfg
            tot_proc = proc
            tot_val = val
            tot_lead = lead
            tot_count = cnt

    if current_key is not None:
        sys.stdout.write(
            "{}\t{:.2f},{:.2f},{:.2f},{:.4f},{:.1f},{:d}\n".format(
                current_key, tot_demanded, tot_mfg, tot_proc, tot_val, tot_lead, tot_count
            )
        )

if __name__ == '__main__':
    main()

