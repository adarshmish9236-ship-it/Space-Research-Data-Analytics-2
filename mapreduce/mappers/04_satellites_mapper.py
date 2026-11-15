#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 04
Domain: Satellites & Orbital Mechanics
Mapper: 04_satellites_mapper.py

Extracts satellite deployment records grouped by orbit type.
Emits:
    key:   orbit_type
    value: altitude_km,inclination_deg,lifetime_years,dry_mass_kg,power_w,1
"""

import sys
import csv

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            reader = csv.reader([line])
            fields = next(reader)
        except Exception:
            fields = line.split(',')

        if not fields or len(fields) < 12:
            continue

        if fields[0].strip().lower() in ('satellite_id', 'id'):
            continue

        orbit_type = fields[5].strip()
        if not orbit_type:
            continue

        try:
            alt = float(fields[6].strip()) if fields[6].strip() else 0.0
            inc = float(fields[7].strip()) if fields[7].strip() else 0.0
            life = float(fields[9].strip()) if fields[9].strip() else 0.0
            mass = float(fields[10].strip()) if fields[10].strip() else 0.0
            power = float(fields[11].strip()) if fields[11].strip() else 0.0

            if alt <= 0 or mass <= 0:
                continue

            sys.stdout.write(
                "{}\t{:.1f},{:.2f},{:.1f},{:.1f},{:.1f},1\n".format(
                    orbit_type, alt, inc, life, mass, power
                )
            )
        except (ValueError, IndexError):
            continue

if __name__ == '__main__':
    main()

