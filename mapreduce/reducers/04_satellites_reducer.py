#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Job 04
Domain: Satellites & Orbital Mechanics
Reducer: 04_satellites_reducer.py

Aggregates satellite deployment metrics by orbit type.
Outputs tab-separated analytical records:
    orbit_type \t satellite_count \t avg_altitude_km \t avg_inclination_deg \t avg_lifetime_years \t total_dry_mass_kg \t avg_dry_mass_kg \t avg_power_w \t total_power_kw
"""

import sys

def main():
    current_key = None
    tot_alt = 0.0
    tot_inc = 0.0
    tot_life = 0.0
    tot_mass = 0.0
    tot_power = 0.0
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
            alt_s, inc_s, life_s, mass_s, pow_s, cnt_s = val_str.split(',')
            alt = float(alt_s)
            inc = float(inc_s)
            life = float(life_s)
            mass = float(mass_s)
            power = float(pow_s)
            cnt = int(cnt_s)
        except (ValueError, IndexError):
            continue

        if current_key == key:
            tot_alt += alt
            tot_inc += inc
            tot_life += life
            tot_mass += mass
            tot_power += power
            tot_count += cnt
        else:
            if current_key is not None:
                emit_aggregation(current_key, tot_alt, tot_inc, tot_life, tot_mass, tot_power, tot_count)
            current_key = key
            tot_alt = alt
            tot_inc = inc
            tot_life = life
            tot_mass = mass
            tot_power = power
            tot_count = cnt

    if current_key is not None:
        emit_aggregation(current_key, tot_alt, tot_inc, tot_life, tot_mass, tot_power, tot_count)

def emit_aggregation(key, alt, inc, life, mass, power, count):
    avg_alt = (alt / count) if count > 0 else 0.0
    avg_inc = (inc / count) if count > 0 else 0.0
    avg_life = (life / count) if count > 0 else 0.0
    avg_mass = (mass / count) if count > 0 else 0.0
    avg_power = (power / count) if count > 0 else 0.0
    total_power_kw = (power / 1000.0)

    sys.stdout.write(
        "{}\t{:d}\t{:.1f}\t{:.2f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.2f}\n".format(
            key,
            count,
            avg_alt,
            avg_inc,
            avg_life,
            mass,
            avg_mass,
            avg_power,
            total_power_kw
        )
    )

if __name__ == '__main__':
    main()

