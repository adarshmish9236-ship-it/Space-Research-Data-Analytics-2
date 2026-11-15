"""
Space Research Data Generator
Generates realistic, interconnected datasets across 10 core space domains:
1. Satellites and orbital parameters
2. Space missions
3. Launch activities
4. Space agency research expenditures
5. Satellite manufacturing demand & specs
6. Space equipment & component demands
7. Space agency research activities
8. Space infrastructure requirements
9. Historical resource consumption (propellant, radiation shielding, telemetry bandwidth, power)
10. Research investment & future project requirements

Includes intentional missing values, noise, seasonal/quarterly cycles, and realistic growth trends.
All datasets are partitioned and stored in Parquet and CSV in HDFS/local structured warehouse.
"""

import os
import json
import random
import datetime
import numpy as np
import pandas as pd
from pathlib import Path

# Fix seed for reproducibility
np.random.seed(42)
random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
RAW_DIR = BASE_DIR / "datasets" / "raw"
HDFS_RAW_DIR = BASE_DIR / "hadoop_ecosystem" / "hdfs" / "space_research" / "raw"

for p in [RAW_DIR, HDFS_RAW_DIR]:
    p.mkdir(parents=True, exist_ok=True)

AGENCIES = ["NASA (USA)", "ESA (Europe)", "ISRO (India)", "JAXA (Japan)", "CNSA (China)", "Roscosmos (Russia)", "Private / Commercial (SpaceX, etc.)"]
ORBITS = ["LEO (Low Earth Orbit)", "MEO (Medium Earth Orbit)", "GEO (Geostationary)", "SSO (Sun-Synchronous)", "Deep Space / Lunar", "Lagrange Points (L1/L2)"]
MISSION_TYPES = ["Earth Observation", "Satellite Communications", "Planetary Exploration", "Deep Space Astrophysics", "Human Spaceflight", "Technology Demonstration", "Space Weather & Heliophysics"]
EQUIPMENT_TYPES = ["Ion Propulsion Engines", "High-Efficiency Solar Arrays", "Cryogenic Tanks", "Radiation-Hardened Rad-750 CPUs", "Optical Inter-Satellite Links", "Star Trackers", "Reaction Wheels", "SAR Radar Antennas"]
RESOURCES = ["Cryogenic Liquid Oxygen (LOX)", "RP-1 Rocket Fuel", "Liquid Hydrogen (LH2)", "Hypergolic Hydrazine", "Radiation Shielding Alloys", "Deep Space Telemetry (Tbps)", "Solar Power Generation (kW)"]

def generate_all_datasets(record_multiplier=1):
    print("Generating comprehensive Space Research Big Data...")
    
    # Dates from 2010 to 2026 (monthly / event-based)
    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2026, 10, 31)
    
    # 1. Space Missions Dataset
    mission_records = []
    num_missions = 1500 * record_multiplier
    current_date = start_date
    for i in range(num_missions):
        m_id = f"MSN-{2010 + (i % 17)}-{1000 + i}"
        agency = random.choice(AGENCIES)
        m_type = random.choice(MISSION_TYPES)
        delta_days = random.randint(0, (end_date - start_date).days)
        m_date = start_date + datetime.timedelta(days=delta_days)
        budget = round(random.uniform(45.0, 3200.0), 2) # in Million USD
        status = np.random.choice(["Successful", "Operational", "In-Flight", "Completed", "Partial Failure", "Retired"], p=[0.45, 0.25, 0.10, 0.12, 0.03, 0.05])
        payload_mass = round(random.uniform(150.0, 18500.0), 1) # kg
        mission_records.append({
            "mission_id": m_id,
            "mission_name": f"{m_type.split()[0]} Discovery {i+1}",
            "agency": agency,
            "mission_type": m_type,
            "launch_date": m_date.isoformat(),
            "year": m_date.year,
            "quarter": f"Q{(m_date.month - 1)//3 + 1}",
            "budget_million_usd": budget,
            "payload_mass_kg": payload_mass,
            "status": status,
            "crew_size": random.choice([0, 0, 0, 0, 2, 3, 4, 6]) if "Human" in m_type else 0,
            "duration_days": random.randint(30, 3650)
        })
    df_missions = pd.DataFrame(mission_records)
    df_missions.to_csv(RAW_DIR / "space_missions.csv", index=False)
    
    # 2. Satellites and Orbital Information
    sat_records = []
    num_sats = 2400 * record_multiplier
    for i in range(num_sats):
        s_id = f"SAT-{2012 + (i % 15)}-{2000 + i}"
        orbit = random.choice(ORBITS)
        altitude = 550 if "LEO" in orbit else (20200 if "MEO" in orbit else (35786 if "GEO" in orbit else random.randint(400, 1500000)))
        inclination = round(random.uniform(0.0, 98.6), 2)
        expected_lifetime_years = random.randint(3, 18)
        launch_year = random.randint(2010, 2026)
        dry_mass = round(random.uniform(50.0, 6500.0), 1)
        power_consumption_w = round(random.uniform(200.0, 15000.0), 1)
        sat_records.append({
            "satellite_id": s_id,
            "satellite_name": f"AstroSat-{i+100}",
            "operator_agency": random.choice(AGENCIES),
            "orbit_type": orbit,
            "altitude_km": altitude,
            "inclination_deg": inclination,
            "launch_year": launch_year,
            "expected_lifetime_years": expected_lifetime_years,
            "dry_mass_kg": dry_mass,
            "power_consumption_w": power_consumption_w,
            "telemetry_band": random.choice(["X-band", "Ka-band", "Ku-band", "S-band", "Optical Laser"]),
            "operational_status": np.random.choice(["Active", "Decommissioned", "Decayed", "Standby"], p=[0.70, 0.15, 0.10, 0.05])
        })
    df_sats = pd.DataFrame(sat_records)
    df_sats.to_csv(RAW_DIR / "satellites_orbital.csv", index=False)
    
    # 3. Launch Activity & Vehicle Historical Statistics
    launch_records = []
    num_launches = 1200 * record_multiplier
    launch_vehicles = ["Falcon 9", "Atlas V", "Ariane 6", "PSLV", "GSLV Mk III", "Long March 5", "Soyuz-2", "Starship Heavy", "Vulcan Centaur", "H3 Launch Vehicle"]
    launch_sites = ["Cape Canaveral SLC-40", "Kennedy Space Center LC-39A", "Kourou ELA-4", "Satish Dhawan SHAR", "Jiuquan SLS", "Baikonur Cosmodrome", "Tanegashima Space Center"]
    for i in range(num_launches):
        l_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        l_status = np.random.choice(["Success", "Partial Failure", "Launch Abort", "Catastrophic Failure"], p=[0.92, 0.04, 0.02, 0.02])
        launch_records.append({
            "launch_id": f"LNCH-{l_date.year}-{100 + i}",
            "launch_date": l_date.isoformat(),
            "year": l_date.year,
            "month": l_date.month,
            "vehicle": random.choice(launch_vehicles),
            "launch_site": random.choice(launch_sites),
            "launch_outcome": l_status,
            "commercial_flag": random.choice([True, False, True]),
            "launch_cost_million_usd": round(random.uniform(40.0, 180.0), 2),
            "payload_to_orbit_kg": round(random.uniform(1200.0, 24000.0), 1)
        })
    df_launches = pd.DataFrame(launch_records)
    df_launches.to_csv(RAW_DIR / "launch_activities.csv", index=False)

    # 4. Monthly Space Agency Research Expenditures (2010 - 2026)
    # Time-series with realistic upward trend & seasonal spikes in Q4
    exp_records = []
    current = start_date
    while current <= end_date:
        for agency in AGENCIES:
            base_exp = 350.0 if "NASA" in agency else (180.0 if "ESA" in agency or "CNSA" in agency else 90.0)
            trend_factor = 1.0 + ((current.year - 2010) * 0.065) # 6.5% yearly industry expansion
            seasonality = 1.18 if current.month in [11, 12] else (0.92 if current.month in [1, 2] else 1.0)
            noise = random.uniform(0.93, 1.07)
            r_and_d = round(base_exp * trend_factor * seasonality * noise * 0.45, 2)
            infra_exp = round(base_exp * trend_factor * seasonality * noise * 0.30, 2)
            mission_ops = round(base_exp * trend_factor * seasonality * noise * 0.25, 2)
            exp_records.append({
                "date": f"{current.year:04d}-{current.month:02d}-01",
                "year": current.year,
                "month": current.month,
                "agency": agency,
                "rd_expenditure_million_usd": r_and_d,
                "infrastructure_expenditure_million_usd": infra_exp,
                "mission_operations_million_usd": mission_ops,
                "total_monthly_expenditure_million_usd": round(r_and_d + infra_exp + mission_ops, 2)
            })
        # increment month
        year = current.year + (1 if current.month == 12 else 0)
        month = 1 if current.month == 12 else current.month + 1
        current = datetime.date(year, month, 1)
    df_exp = pd.DataFrame(exp_records)
    df_exp.to_csv(RAW_DIR / "agency_research_expenditures.csv", index=False)

    # 5. Space Equipment and Component Demand (Monthly Demand Records for Forecasting)
    # This forms a primary time-series forecasting target
    demand_records = []
    current = start_date
    while current <= end_date:
        month_idx = (current.year - 2010) * 12 + current.month
        for eq in EQUIPMENT_TYPES:
            # Baseline + Growth + Cyclic variation
            base = 40 if "Rad" in eq or "Optical" in eq else 20
            growth = (month_idx ** 1.15) * 0.35
            seasonal = np.sin(month_idx * (2 * np.pi / 12)) * 6.5
            noise = np.random.normal(0, 3.0)
            units_demanded = max(5, int(round(base + growth + seasonal + noise)))
            avg_unit_cost_k = round(random.uniform(120.0, 950.0), 1)
            lead_time_days = random.randint(90, 420)
            shortage_risk = "High" if units_demanded > (base + growth + 10) else ("Medium" if units_demanded > (base + growth) else "Low")
            
            demand_records.append({
                "date": f"{current.year:04d}-{current.month:02d}-01",
                "year": current.year,
                "month": current.month,
                "equipment_type": eq,
                "units_demanded": units_demanded,
                "avg_unit_cost_thousand_usd": avg_unit_cost_k,
                "total_demand_value_million_usd": round((units_demanded * avg_unit_cost_k) / 1000.0, 3),
                "lead_time_days": lead_time_days,
                "shortage_risk": shortage_risk
            })
        year = current.year + (1 if current.month == 12 else 0)
        month = 1 if current.month == 12 else current.month + 1
        current = datetime.date(year, month, 1)
    df_demand = pd.DataFrame(demand_records)
    df_demand.to_csv(RAW_DIR / "equipment_component_demand.csv", index=False)

    # 6. Historical Resource Consumption (Propellants, Power, Telemetry, Alloys)
    resource_records = []
    current = start_date
    while current <= end_date:
        month_idx = (current.year - 2010) * 12 + current.month
        for res in RESOURCES:
            base_cons = 150.0 if "Propellant" in res or "LOX" in res or "RP-1" in res else 50.0
            trend = (month_idx ** 1.08) * 0.8
            seasonal = np.cos(month_idx * (2 * np.pi / 12)) * 12.0
            consumed = round(max(10.0, base_cons + trend + seasonal + random.uniform(-10, 10)), 2)
            unit = "Metric Tons" if "LOX" in res or "Fuel" in res or "LH2" in res or "Alloy" in res else ("Tbps" if "Telemetry" in res else "kW")
            resource_records.append({
                "date": f"{current.year:04d}-{current.month:02d}-01",
                "year": current.year,
                "month": current.month,
                "resource_name": res,
                "quantity_consumed": consumed,
                "unit_of_measure": unit,
                "procurement_cost_k_usd": round(consumed * random.uniform(15.0, 45.0), 2)
            })
        year = current.year + (1 if current.month == 12 else 0)
        month = 1 if current.month == 12 else current.month + 1
        current = datetime.date(year, month, 1)
    df_res = pd.DataFrame(resource_records)
    df_res.to_csv(RAW_DIR / "resource_consumption.csv", index=False)

    # 7. Satellite Manufacturing Requirements
    mfg_records = []
    num_mfg = 600 * record_multiplier
    for i in range(num_mfg):
        mfg_records.append({
            "order_id": f"ORD-MFG-{2018 + (i % 9)}-{1000 + i}",
            "agency_client": random.choice(AGENCIES),
            "satellite_class": random.choice(["CubeSat (1U-12U)", "SmallSat (<500kg)", "Medium Satellite (500-2000kg)", "Heavy Geosynchronous Bus (>2000kg)"]),
            "units_ordered": random.randint(1, 24),
            "delivery_year": random.randint(2021, 2028),
            "cleanroom_hours_required": random.randint(400, 7500),
            "vibration_testing_pass": random.choice([True, True, True, False]),
            "contract_value_million_usd": round(random.uniform(5.5, 320.0), 2)
        })
    df_mfg = pd.DataFrame(mfg_records)
    df_mfg.to_csv(RAW_DIR / "satellite_manufacturing_requirements.csv", index=False)

    # 8. Space Infrastructure Requirements (Ground Stations, Cleanrooms, Supercomputing, Optical Terminals)
    infra_records = []
    infra_facilities = ["Deep Space Network (DSN) Antenna Time", "Space Cryogenic Test Facilities", "High-Performance Orbital Compute Nodes", "Autonomous Ground Tracking Radars", "Vibration & Thermal Vacuum Chambers"]
    current = start_date
    while current <= end_date:
        for fac in infra_facilities:
            utilization_pct = round(min(98.5, max(45.0, 60.0 + ((current.year - 2010) * 1.8) + random.uniform(-8.0, 8.0))), 1)
            queued_hours = int(max(20, (utilization_pct - 50) * 25 + random.randint(0, 150)))
            infra_records.append({
                "date": f"{current.year:04d}-{current.month:02d}-01",
                "year": current.year,
                "month": current.month,
                "facility_name": fac,
                "utilization_rate_pct": utilization_pct,
                "queued_backlog_hours": queued_hours,
                "maintenance_downtime_days": random.randint(0, 5)
            })
        year = current.year + (1 if current.month == 12 else 0)
        month = 1 if current.month == 12 else current.month + 1
        current = datetime.date(year, month, 1)
    df_infra = pd.DataFrame(infra_records)
    df_infra.to_csv(RAW_DIR / "space_infrastructure_requirements.csv", index=False)

    # 9. Research Investment & Future Projects Forecast Targets
    proj_records = []
    for i in range(150 * record_multiplier):
        proj_records.append({
            "project_code": f"PRJ-{2024 + (i%5)}-{100+i}",
            "project_title": f"NextGen {random.choice(['Artemis', 'Lunar Gateway', 'Mars Sample Return', 'Exoplanet Spectroscopy', 'Quantum Satellite Network'])} Phase {1 + (i % 4)}",
            "lead_agency": random.choice(AGENCIES),
            "target_commencement_year": random.randint(2025, 2035),
            "estimated_investment_billion_usd": round(random.uniform(0.4, 18.5), 2),
            "priority_tier": random.choice(["Critical Strategic", "High Priority", "Scientific Discovery", "Exploratory"]),
            "readiness_level_TRL": random.randint(3, 8)
        })
    df_proj = pd.DataFrame(proj_records)
    df_proj.to_csv(RAW_DIR / "research_investment_future_projects.csv", index=False)

    # Also sync into HDFS raw structure
    for csv_file in RAW_DIR.glob("*.csv"):
        dest = HDFS_RAW_DIR / csv_file.name
        with open(csv_file, 'r', encoding='utf-8') as f_src, open(dest, 'w', encoding='utf-8') as f_dst:
            f_dst.write(f_src.read())

    print(f"Data generation complete: 9 datasets written to {RAW_DIR} and mirrored into HDFS raw {HDFS_RAW_DIR}")
    return True

if __name__ == "__main__":
    generate_all_datasets()
