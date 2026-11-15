#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 07
Domain: Agency Research & Infrastructure Expenditure
Reducer: 07_research_investment_reducer.py

Aggregates research investment intelligence by agency and year.
Outputs tab-separated analytical records:
    agency_name \t year \t total_rd_m \t total_infra_m \t total_ops_m \t grand_total_m \t rd_share_pct \t months_count
"""

import sys

def main():
    current_key = None
    tot_rd = 0.0
    tot_infra = 0.0
    tot_ops = 0.0
    tot_total = 0.0
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
            rd_s, inf_s, ops_s, tot_s, cnt_s = val_str.split(',')
            rd = float(rd_s)
            infra = float(inf_s)
            ops = float(ops_s)
            total = float(tot_s)
            cnt = int(cnt_s)
        except (ValueError, IndexError):
            continue

        if current_key == key:
            tot_rd += rd
            tot_infra += infra
            tot_ops += ops
            tot_total += total
            tot_count += cnt
        else:
            if current_key is not None:
                emit_aggregation(current_key, tot_rd, tot_infra, tot_ops, tot_total, tot_count)
            current_key = key
            tot_rd = rd
            tot_infra = infra
            tot_ops = ops
            tot_total = total
            tot_count = cnt

    if current_key is not None:
        emit_aggregation(current_key, tot_rd, tot_infra, tot_ops, tot_total, tot_count)

def emit_aggregation(key, rd, infra, ops, total, count):
    if "::" in key:
        agency, year = key.split("::", 1)
    else:
        agency, year = key, "UNKNOWN"

    rd_share = ((rd / total) * 100.0) if total > 0 else 0.0

    sys.stdout.write(
        "{}\t{}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:d}\n".format(
            agency,
            year,
            rd,
            infra,
            ops,
            total,
            rd_share,
            count
        )
    )

if __name__ == '__main__':
    main()
