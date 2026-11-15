#!/usr/bin/env python3
import sys

current_key = None
mission_count = 0
total_budget = 0.0
payload_sum = 0.0
duration_sum = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 5:
        continue
    key = parts[0]
    cnt, budget, payload, dur = int(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])

    if current_key == key:
        mission_count += cnt
        total_budget += budget
        payload_sum += payload
        duration_sum += dur
    else:
        if current_key is not None:
            avg_pl = payload_sum / mission_count if mission_count > 0 else 0.0
            avg_dur = duration_sum / mission_count if mission_count > 0 else 0.0
            print("{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4:.2f}".format(current_key, mission_count, total_budget, avg_pl, avg_dur))
        current_key = key
        mission_count = cnt
        total_budget = budget
        payload_sum = payload
        duration_sum = dur

if current_key is not None:
    avg_pl = payload_sum / mission_count if mission_count > 0 else 0.0
    avg_dur = duration_sum / mission_count if mission_count > 0 else 0.0
    print("{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4:.2f}".format(current_key, mission_count, total_budget, avg_pl, avg_dur))
