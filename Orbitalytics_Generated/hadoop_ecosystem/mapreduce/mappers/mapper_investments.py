#!/usr/bin/env python3
"""
Hadoop Streaming Mapper: Research Investment
Emits: agency \t investment_amount \t count \t trl
"""
import sys

first_line = True
for line in sys.stdin:
    if first_line:
        first_line = False
        continue
    line = line.strip()
    if not line:
        continue
    parts = line.split(",")
    if len(parts) >= 6:
        # agency, country, domain, budget_usd, trl...
        agency = parts[1].strip() if len(parts) > 1 else parts[0].strip()
        try:
            budget = float(parts[4].strip())
        except (ValueError, IndexError):
            budget = 1000000.0
        try:
            trl = float(parts[5].strip())
        except (ValueError, IndexError):
            trl = 6.0
        print(f"{agency}\t{budget}\t1\t{trl}")

