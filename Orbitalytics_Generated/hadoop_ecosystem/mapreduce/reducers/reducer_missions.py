#!/usr/bin/env python3
"""
Hadoop Streaming Reducer: Space Missions
Aggregates Key-Value pairs grouped by Agency:
Outputs: Agency \t TotalMissions \t TotalBudgetMillion \t AvgPayloadKg \t SuccessRatePct
"""
import sys

def main():
    current_agency = None
    mission_count = 0
    total_budget = 0.0
    total_payload = 0.0
    successful_missions = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 5:
            continue

        agency, count_str, budget_str, payload_str, status = parts[0], parts[1], parts[2], parts[3], parts[4]
        try:
            cnt = int(count_str)
            budget = float(budget_str)
            payload = float(payload_str)
        except ValueError:
            continue

        if current_agency == agency:
            mission_count += cnt
            total_budget += budget
            total_payload += payload
            if status in ["Successful", "Operational", "Completed"]:
                successful_missions += cnt
        else:
            if current_agency is not None:
                avg_payload = round(total_payload / max(1, mission_count), 1)
                success_rate = round((successful_missions / max(1, mission_count)) * 100.0, 1)
                print(f"{current_agency}\t{mission_count}\t{round(total_budget, 1)}\t{avg_payload}\t{success_rate}")
            current_agency = agency
            mission_count = cnt
            total_budget = budget
            total_payload = payload
            successful_missions = cnt if status in ["Successful", "Operational", "Completed"] else 0

    if current_agency is not None:
        avg_payload = round(total_payload / max(1, mission_count), 1)
        success_rate = round((successful_missions / max(1, mission_count)) * 100.0, 1)
        print(f"{current_agency}\t{mission_count}\t{round(total_budget, 1)}\t{avg_payload}\t{success_rate}")

if __name__ == "__main__":
    main()

