#!/usr/bin/env python3
"""
Hadoop Streaming Reducer: Launch Activities
Aggregates launch vehicle metrics by Year and Vehicle.
"""
import sys

def main():
    current_key = None
    launches = 0
    successes = 0
    total_payload = 0.0
    total_cost = 0.0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 5:
            continue

        key, l_cnt, s_cnt, p_mass, c_val = parts[0], parts[1], parts[2], parts[3], parts[4]
        try:
            l = int(l_cnt)
            s = int(s_cnt)
            p = float(p_mass)
            c = float(c_val)
        except ValueError:
            continue

        if current_key == key:
            launches += l
            successes += s
            total_payload += p
            total_cost += c
        else:
            if current_key is not None:
                year, vehicle = current_key.split("::")
                rate = round((successes / max(1, launches)) * 100.0, 1)
                avg_payload = round(total_payload / max(1, launches), 1)
                print(f"{year}\t{vehicle}\t{launches}\t{successes}\t{rate}\t{avg_payload}\t{round(total_cost, 1)}")
            current_key = key
            launches = l
            successes = s
            total_payload = p
            total_cost = c

    if current_key is not None:
        year, vehicle = current_key.split("::")
        rate = round((successes / max(1, launches)) * 100.0, 1)
        avg_payload = round(total_payload / max(1, launches), 1)
        print(f"{year}\t{vehicle}\t{launches}\t{successes}\t{rate}\t{avg_payload}\t{round(total_cost, 1)}")

if __name__ == "__main__":
    main()

