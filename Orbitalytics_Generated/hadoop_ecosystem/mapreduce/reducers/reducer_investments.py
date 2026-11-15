#!/usr/bin/env python3
"""
Hadoop Streaming Reducer: Research Investment
Aggregates total investment and average TRL per agency.
"""
import sys

current_agency = None
total_budget = 0.0
total_projects = 0
total_trl = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) < 4:
        continue
    agency, budget_str, cnt_str, trl_str = parts[0], parts[1], parts[2], parts[3]
    try:
        b = float(budget_str)
        c = int(cnt_str)
        t = float(trl_str)
    except ValueError:
        continue

    if current_agency == agency:
        total_budget += b
        total_projects += c
        total_trl += t
    else:
        if current_agency:
            avg_trl = round(total_trl / max(1, total_projects), 1)
            b_billion = round(total_budget / 1e9, 2)
            print(f"{current_agency}\t{total_projects}\t{b_billion}\t{avg_trl}")
        current_agency = agency
        total_budget = b
        total_projects = c
        total_trl = t

if current_agency:
    avg_trl = round(total_trl / max(1, total_projects), 1)
    b_billion = round(total_budget / 1e9, 2)
    print(f"{current_agency}\t{total_projects}\t{b_billion}\t{avg_trl}")

