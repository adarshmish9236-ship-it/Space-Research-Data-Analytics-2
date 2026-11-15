"""
ORBITALYTICS - Phase 1 Controlled Synthetic Data Generator
Generates realistic, scientifically grounded, reproducible datasets across the 5 formal space domains
and 9 core datasets.
Features:
- Fixed random seeds for strict reproducibility.
- Explicit data_origin = 'synthetic' and is_synthetic = True.
- Strict referential integrity: foreign keys reference valid agency, component, resource, and mission IDs.
- Configurable scale profiles: 'small' (~10k records), 'medium' (~100k records), 'large' (~1M records).
- Realistic temporal dynamics: multi-year industry growth trends, seasonal cycles, and realistic volatility.
"""

import json
import random
import datetime
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import pandas as pd

class SyntheticDataGenerator:
    def __init__(self, base_dir: Path = None, seed: int = 42):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).resolve().parent.parent.parent
        self.synthetic_raw_dir = self.base_dir / "datasets" / "raw" / "synthetic"
        self.reference_dir = self.base_dir / "datasets" / "reference"
        self.metadata_dir = self.base_dir / "datasets" / "metadata"
        self.seed = seed

        self.synthetic_raw_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

        # Set deterministic seeds
        np.random.seed(self.seed)
        random.seed(self.seed)

        # Load reference master data
        self.agencies = self._load_reference_agencies()
        self.components = self._load_reference_components()
        self.resources = self._load_reference_resources()

    def _load_reference_agencies(self) -> List[Dict[str, str]]:
        ref_file = self.reference_dir / "agencies" / "agencies.csv"
        if ref_file.exists():
            df = pd.read_csv(ref_file)
            return df.to_dict(orient="records")
        return [
            {"agency_id": "AGY-001", "agency_name": "NASA", "agency_code": "NASA", "country": "United States"},
            {"agency_id": "AGY-002", "agency_name": "ESA", "agency_code": "ESA", "country": "Europe"},
            {"agency_id": "AGY-003", "agency_name": "ISRO", "agency_code": "ISRO", "country": "India"},
            {"agency_id": "AGY-004", "agency_name": "JAXA", "agency_code": "JAXA", "country": "Japan"},
            {"agency_id": "AGY-005", "agency_name": "CNSA", "agency_code": "CNSA", "country": "China"},
            {"agency_id": "AGY-006", "agency_name": "Roscosmos", "agency_code": "Roscosmos", "country": "Russia"},
            {"agency_id": "AGY-007", "agency_name": "Commercial Space Operators", "agency_code": "COMMERCIAL", "country": "United States"}
        ]

    def _load_reference_components(self) -> List[Dict[str, Any]]:
        ref_file = self.reference_dir / "components" / "components.csv"
        if ref_file.exists():
            df = pd.read_csv(ref_file)
            return df.to_dict(orient="records")
        return [
            {"component_id": "CMP-001", "component_name": "Solar Panels", "component_category": "Power Systems", "typical_lead_time_days": 270},
            {"component_id": "CMP-002", "component_name": "Rad-750 CPUs", "component_category": "Avionics", "typical_lead_time_days": 360},
            {"component_id": "CMP-003", "component_name": "Ion Thrusters", "component_category": "Propulsion", "typical_lead_time_days": 300},
            {"component_id": "CMP-004", "component_name": "Laser Links", "component_category": "Communications", "typical_lead_time_days": 210}
        ]

    def _load_reference_resources(self) -> List[Dict[str, Any]]:
        ref_file = self.reference_dir / "resources" / "resources.csv"
        if ref_file.exists():
            df = pd.read_csv(ref_file)
            return df.to_dict(orient="records")
        return [
            {"resource_id": "RES-001", "resource_name": "Liquid Oxygen (LOX)", "resource_category": "Propellant & Oxidizer", "unit_of_measure": "Metric Tons", "base_cost_usd_per_unit": 800.0},
            {"resource_id": "RES-002", "resource_name": "RP-1 Kerosene", "resource_category": "Liquid Fuel", "unit_of_measure": "Metric Tons", "base_cost_usd_per_unit": 1200.0},
            {"resource_id": "RES-003", "resource_name": "Liquid Hydrogen (LH2)", "resource_category": "Cryogenic Fuel", "unit_of_measure": "Metric Tons", "base_cost_usd_per_unit": 2500.0}
        ]

    def generate_profile(self, profile: str = "small") -> Dict[str, Any]:
        """
        Generates complete 9 datasets according to scale profile.
        Profiles:
          'small': multiplier = 1.0 (~10,000 total records)
          'medium': multiplier = 10.0 (~100,000 total records)
          'large': multiplier = 100.0 (~1,000,000+ total records)
        """
        profile_multipliers = {
            "small": 1.0,
            "medium": 10.0,
            "large": 100.0
        }
        multiplier = profile_multipliers.get(profile.lower(), 1.0)
        print(f"[INFO] Generating synthetic space research data with profile='{profile}' (multiplier={multiplier})...")

        start_date = datetime.date(2010, 1, 1)
        end_date = datetime.date(2026, 10, 1)

        # 1. Space Missions (DOMAIN 4)
        num_missions = int(1500 * multiplier)
        missions = []
        mission_types = [
            "Earth Observation", "Satellite Communications", "Planetary Exploration",
            "Deep Space Astrophysics", "Human Spaceflight", "Technology Demonstration",
            "Space Weather & Heliophysics"
        ]
        statuses = ["Successful", "Operational", "In-Flight", "Completed", "Partial Failure", "Retired"]
        status_probs = [0.45, 0.25, 0.10, 0.12, 0.03, 0.05]

        for i in range(num_missions):
            m_id = f"MSN-{2010 + (i % 17)}-{1000 + i}"
            agency_obj = random.choice(self.agencies)
            m_type = random.choice(mission_types)
            delta_days = random.randint(0, (end_date - start_date).days)
            m_date = start_date + datetime.timedelta(days=delta_days)
            budget = round(random.uniform(45.0, 3200.0), 2)
            payload_mass = round(random.uniform(150.0, 18500.0), 1)
            status = np.random.choice(statuses, p=status_probs)
            crew = random.choice([0, 0, 0, 2, 3, 4, 6]) if "Human" in m_type else 0

            missions.append({
                "mission_id": m_id,
                "mission_name": f"{m_type.split()[0]} Discovery {i + 1}",
                "agency_id": agency_obj["agency_id"],
                "agency_name": agency_obj["agency_name"],
                "mission_type": m_type,
                "launch_date": m_date.isoformat(),
                "year": m_date.year,
                "quarter": f"Q{(m_date.month - 1) // 3 + 1}",
                "budget_million_usd": budget,
                "payload_mass_kg": payload_mass,
                "status": status,
                "crew_size": crew,
                "duration_days": random.randint(30, 3650),
                "data_origin": "synthetic"
            })
        df_missions = pd.DataFrame(missions)
        df_missions.to_csv(self.synthetic_raw_dir / "space_missions.csv", index=False)

        # 2. Satellites and Orbital (DOMAIN 4)
        num_sats = int(2400 * multiplier)
        satellites = []
        orbits = [
            "LEO (Low Earth Orbit)", "MEO (Medium Earth Orbit)", "GEO (Geostationary)",
            "SSO (Sun-Synchronous)", "Deep Space / Lunar", "Lagrange Points (L1/L2)"
        ]
        sat_statuses = ["Active", "Decommissioned", "Decayed", "Standby"]
        sat_probs = [0.70, 0.15, 0.10, 0.05]

        for i in range(num_sats):
            s_id = f"SAT-{2012 + (i % 15)}-{2000 + i}"
            orbit = random.choice(orbits)
            alt = 550.0 if "LEO" in orbit else (20200.0 if "MEO" in orbit else (35786.0 if "GEO" in orbit else round(random.uniform(400.0, 120000.0), 1)))
            inc = round(random.uniform(0.0, 98.6), 2)
            agency_obj = random.choice(self.agencies)
            matched_mission = random.choice(missions)["mission_id"]

            satellites.append({
                "satellite_id": s_id,
                "satellite_name": f"AstroSat-{i + 100}",
                "operator_agency_id": agency_obj["agency_id"],
                "operator_agency_name": agency_obj["agency_name"],
                "associated_mission_id": matched_mission,
                "orbit_type": orbit,
                "altitude_km": alt,
                "inclination_deg": inc,
                "launch_year": random.randint(2010, 2026),
                "expected_lifetime_years": random.randint(3, 18),
                "dry_mass_kg": round(random.uniform(50.0, 6500.0), 1),
                "power_consumption_w": round(random.uniform(200.0, 15000.0), 1),
                "telemetry_band": random.choice(["X-band", "Ka-band", "Ku-band", "S-band", "Optical Laser"]),
                "operational_status": np.random.choice(sat_statuses, p=sat_probs),
                "data_origin": "synthetic"
            })
        df_satellites = pd.DataFrame(satellites)
        df_satellites.to_csv(self.synthetic_raw_dir / "satellites_orbital.csv", index=False)

        # 3. Launch Activities (DOMAIN 4)
        num_launches = int(1200 * multiplier)
        launches = []
        vehicles = ["Falcon 9", "Atlas V", "Ariane 6", "PSLV", "GSLV Mk III", "Long March 5", "Soyuz-2", "Starship Heavy", "Vulcan Centaur", "H3 Launch Vehicle"]
        launch_sites = [
            ("Cape Canaveral SLC-40", "United States"),
            ("Kennedy Space Center LC-39A", "United States"),
            ("Kourou ELA-4", "Europe"),
            ("Satish Dhawan SHAR", "India"),
            ("Jiuquan SLS", "China"),
            ("Baikonur Cosmodrome", "Russia"),
            ("Tanegashima Space Center", "Japan")
        ]
        launch_outcomes = ["Success", "Partial Failure", "Launch Abort", "Catastrophic Failure"]
        outcome_probs = [0.93, 0.03, 0.02, 0.02]

        for i in range(num_launches):
            delta_days = random.randint(0, (end_date - start_date).days)
            l_date = start_date + datetime.timedelta(days=delta_days)
            site_info = random.choice(launch_sites)
            outcome = np.random.choice(launch_outcomes, p=outcome_probs)
            matched_mission = random.choice(missions)["mission_id"]

            launches.append({
                "launch_id": f"LNCH-{l_date.year}-{100 + i}",
                "mission_id": matched_mission,
                "launch_date": l_date.isoformat(),
                "year": l_date.year,
                "month": l_date.month,
                "vehicle": random.choice(vehicles),
                "launch_site": site_info[0],
                "country": site_info[1],
                "launch_outcome": outcome,
                "commercial_flag": random.choice([True, False, True]),
                "launch_cost_million_usd": round(random.uniform(40.0, 180.0), 2),
                "payload_to_orbit_kg": round(random.uniform(1200.0, 24000.0), 1),
                "data_origin": "synthetic"
            })
        df_launches = pd.DataFrame(launches)
        df_launches.to_csv(self.synthetic_raw_dir / "launch_activities.csv", index=False)

        # 4. Equipment Component Demand (DOMAIN 1 - Primary Forecasting Target)
        demand_records = []
        sat_classes = ["CubeSat (1U-12U)", "SmallSat (<500kg)", "Medium Satellite (500-2000kg)", "Heavy Geosynchronous Bus (>2000kg)"]
        current = start_date
        d_idx = 0

        while current <= end_date:
            month_idx = (current.year - 2010) * 12 + current.month
            quarter_str = f"Q{(current.month - 1) // 3 + 1}"

            for comp in self.components:
                for agency in self.agencies:
                    d_idx += 1
                    base = 15 if "Rad" in comp["component_name"] or "Power" in comp["component_category"] else 8
                    growth = (month_idx ** 1.12) * 0.22
                    seasonal = np.sin(month_idx * (2 * np.pi / 12)) * 4.5
                    noise = np.random.normal(0, 2.5)
                    demanded = max(2, int(round(base + growth + seasonal + noise)))

                    mfg_qty = max(0, int(round(demanded * random.uniform(0.75, 1.15))))
                    proc_qty = max(0, int(round(demanded * random.uniform(0.80, 1.20))))
                    avg_cost_k = round(random.uniform(85.0, 920.0), 1)
                    lead_time = int(comp.get("typical_lead_time_days", random.randint(120, 360)) * random.uniform(0.85, 1.25))

                    risk = "Critical" if demanded > (base + growth + 12) else ("High" if demanded > (base + growth + 5) else ("Medium" if demanded > (base + growth) else "Low"))

                    demand_records.append({
                        "demand_id": f"DEM-{current.year}-{d_idx:05d}",
                        "date": f"{current.year:04d}-{current.month:02d}-01",
                        "year": current.year,
                        "month": current.month,
                        "quarter": quarter_str,
                        "component_id": comp["component_id"],
                        "component_name": comp["component_name"],
                        "component_category": comp["component_category"],
                        "agency_id": agency["agency_id"],
                        "agency_name": agency["agency_name"],
                        "target_satellite_class": random.choice(sat_classes),
                        "units_demanded": demanded,
                        "units_manufactured": mfg_qty,
                        "units_procured": proc_qty,
                        "unit_of_measure": "Units",
                        "avg_unit_cost_thousand_usd": avg_cost_k,
                        "total_demand_value_million_usd": round((demanded * avg_cost_k) / 1000.0, 3),
                        "lead_time_days": lead_time,
                        "shortage_risk": risk,
                        "data_origin": "synthetic"
                    })

            # Advance 1 month
            year = current.year + (1 if current.month == 12 else 0)
            month = 1 if current.month == 12 else current.month + 1
            current = datetime.date(year, month, 1)

        df_demand = pd.DataFrame(demand_records)
        df_demand.to_csv(self.synthetic_raw_dir / "equipment_component_demand.csv", index=False)

        # 5. Agency Research Expenditures (DOMAIN 5)
        exp_records = []
        current = start_date
        e_idx = 0

        while current <= end_date:
            month_idx = (current.year - 2010) * 12 + current.month
            quarter_str = f"Q{(current.month - 1) // 3 + 1}"

            for agency in self.agencies:
                e_idx += 1
                base_exp = 380.0 if "NASA" in agency["agency_code"] else (190.0 if agency["agency_code"] in ["ESA", "CNSA"] else 95.0)
                trend = 1.0 + ((current.year - 2010) * 0.062)
                seasonality = 1.15 if current.month in [11, 12] else (0.94 if current.month in [1, 2] else 1.0)
                noise = random.uniform(0.94, 1.06)

                rd = round(base_exp * trend * seasonality * noise * 0.48, 2)
                infra = round(base_exp * trend * seasonality * noise * 0.28, 2)
                ops = round(base_exp * trend * seasonality * noise * 0.24, 2)
                tot = round(rd + infra + ops, 2)

                exp_records.append({
                    "expenditure_id": f"EXP-{current.year}-{e_idx:05d}",
                    "date": f"{current.year:04d}-{current.month:02d}-01",
                    "year": current.year,
                    "month": current.month,
                    "quarter": quarter_str,
                    "agency_id": agency["agency_id"],
                    "agency_name": agency["agency_name"],
                    "country": agency["country"],
                    "rd_expenditure_million_usd": rd,
                    "infrastructure_expenditure_million_usd": infra,
                    "mission_operations_million_usd": ops,
                    "total_monthly_expenditure_million_usd": tot,
                    "currency": "USD",
                    "data_origin": "synthetic"
                })

            year = current.year + (1 if current.month == 12 else 0)
            month = 1 if current.month == 12 else current.month + 1
            current = datetime.date(year, month, 1)

        df_exp = pd.DataFrame(exp_records)
        df_exp.to_csv(self.synthetic_raw_dir / "agency_research_expenditures.csv", index=False)

        # 6. Resource Consumption (DOMAIN 2 - Primary Forecasting Target)
        res_records = []
        current = start_date
        c_idx = 0

        while current <= end_date:
            month_idx = (current.year - 2010) * 12 + current.month
            quarter_str = f"Q{(current.month - 1) // 3 + 1}"

            for res in self.resources:
                for agency in self.agencies:
                    c_idx += 1
                    base_c = 110.0 if "Oxygen" in res["resource_name"] or "RP-1" in res["resource_name"] else 35.0
                    trend = (month_idx ** 1.06) * 0.65
                    seasonal = np.cos(month_idx * (2 * np.pi / 12)) * 8.5
                    consumed = round(max(5.0, base_c + trend + seasonal + random.uniform(-6, 6)), 2)
                    cost_base = res.get("base_cost_usd_per_unit", 1000.0)
                    proc_cost_k = round((consumed * cost_base * random.uniform(0.9, 1.2)) / 1000.0, 2)
                    matched_m = random.choice(missions)["mission_id"]

                    res_records.append({
                        "consumption_id": f"CNS-{current.year}-{c_idx:05d}",
                        "date": f"{current.year:04d}-{current.month:02d}-01",
                        "year": current.year,
                        "month": current.month,
                        "quarter": quarter_str,
                        "resource_id": res["resource_id"],
                        "resource_name": res["resource_name"],
                        "resource_category": res["resource_category"],
                        "agency_id": agency["agency_id"],
                        "agency_name": agency["agency_name"],
                        "mission_id": matched_m,
                        "quantity_consumed": consumed,
                        "unit_of_measure": res["unit_of_measure"],
                        "procurement_cost_k_usd": proc_cost_k,
                        "data_origin": "synthetic"
                    })

            year = current.year + (1 if current.month == 12 else 0)
            month = 1 if current.month == 12 else current.month + 1
            current = datetime.date(year, month, 1)

        df_res = pd.DataFrame(res_records)
        df_res.to_csv(self.synthetic_raw_dir / "resource_consumption.csv", index=False)

        # 7. Satellite Manufacturing Requirements (DOMAIN 3)
        num_mfg = int(600 * multiplier)
        mfg_records = []
        for i in range(num_mfg):
            agency = random.choice(self.agencies)
            mfg_records.append({
                "order_id": f"ORD-MFG-{2018 + (i % 9)}-{1000 + i}",
                "agency_id": agency["agency_id"],
                "agency_client": agency["agency_name"],
                "satellite_class": random.choice(sat_classes),
                "units_ordered": random.randint(1, 24),
                "delivery_year": random.randint(2021, 2028),
                "cleanroom_hours_required": random.randint(400, 7500),
                "vibration_testing_pass": random.choice([True, True, True, False]),
                "contract_value_million_usd": round(random.uniform(5.5, 320.0), 2),
                "data_origin": "synthetic"
            })
        df_mfg = pd.DataFrame(mfg_records)
        df_mfg.to_csv(self.synthetic_raw_dir / "satellite_manufacturing_requirements.csv", index=False)

        # 8. Space Infrastructure Requirements (DOMAIN 5)
        infra_records = []
        infra_facilities = [
            ("Deep Space Network (DSN) Antenna Time", "Ground Station Network", "Goldstone / Madrid / Canberra"),
            ("Cryogenic Spacecraft Testing Chambers", "Cryogenic Testing", "ESTEC Noordwijk / Glenn Research"),
            ("High-Performance Orbital Compute Cluster", "High-Performance Compute", "Ames Research Supercomputing"),
            ("Autonomous Global Radar Tracking Facility", "Radar Tracking", "Kwajalein Atoll / Svalbard"),
            ("Thermal Vacuum & Acoustic Vibration Lab", "Environmental Testing", "ISRO Satellite Integration Centre")
        ]
        current = start_date
        inf_idx = 0

        while current <= end_date:
            for fac in infra_facilities:
                inf_idx += 1
                agency = random.choice(self.agencies)
                util = round(min(98.5, max(45.0, 62.0 + ((current.year - 2010) * 1.6) + random.uniform(-6.0, 6.0))), 1)
                queue = int(max(15, (util - 50) * 22 + random.randint(0, 120)))

                infra_records.append({
                    "infrastructure_record_id": f"INF-{current.year}-{inf_idx:05d}",
                    "date": f"{current.year:04d}-{current.month:02d}-01",
                    "year": current.year,
                    "month": current.month,
                    "facility_name": fac[0],
                    "facility_type": fac[1],
                    "agency_id": agency["agency_id"],
                    "agency_name": agency["agency_name"],
                    "location": fac[2],
                    "utilization_rate_pct": util,
                    "queued_backlog_hours": queue,
                    "maintenance_downtime_days": random.randint(0, 5),
                    "data_origin": "synthetic"
                })

            year = current.year + (1 if current.month == 12 else 0)
            month = 1 if current.month == 12 else current.month + 1
            current = datetime.date(year, month, 1)

        df_infra = pd.DataFrame(infra_records)
        df_infra.to_csv(self.synthetic_raw_dir / "space_infrastructure_requirements.csv", index=False)

        # 9. Future Research Investment Projects (DOMAIN 5)
        num_proj = int(160 * multiplier)
        proj_records = []
        themes = [
            ("NextGen Artemis Lunar Base", "Deep Space Exploration"),
            ("Lunar Gateway Orbital Habitation Node", "Orbital Infrastructure"),
            ("Mars Sample Return Logistics", "Planetary Science"),
            ("Deep Space Exoplanet Infrared Spectroscopy", "Astrophysics"),
            ("Quantum Optical Satellite Communications Grid", "Advanced Communications")
        ]

        for i in range(num_proj):
            agency = random.choice(self.agencies)
            p_year = random.randint(2025, 2035)
            theme_choice = random.choice(themes)
            inv = round(random.uniform(0.5, 18.5) * 1000.0, 1)
            trl = random.randint(3, 8)
            priority = random.choice(["Critical Strategic", "High Priority", "Scientific Discovery", "Exploratory"])
            status = random.choice(["Proposed", "Funded - Phase A", "Phase B Development", "Approved"])

            proj_records.append({
                "project_id": f"PRJ-{p_year}-{200 + i}",
                "project_title": f"{theme_choice[0]} Phase {1 + (i % 4)}",
                "agency_id": agency["agency_id"],
                "lead_agency": agency["agency_name"],
                "country": agency["country"],
                "research_theme": theme_choice[1],
                "target_commencement_year": p_year,
                "estimated_investment_million_usd": inv,
                "priority_tier": priority,
                "technology_readiness_level": trl,
                "project_status": status,
                "data_origin": "synthetic"
            })

        df_proj = pd.DataFrame(proj_records)
        df_proj.to_csv(self.synthetic_raw_dir / "research_investment_future_projects.csv", index=False)

        summary = {
            "profile": profile,
            "seed": self.seed,
            "data_origin": "synthetic",
            "is_synthetic": True,
            "counts": {
                "space_missions": len(df_missions),
                "satellites_orbital": len(df_satellites),
                "launch_activities": len(df_launches),
                "equipment_component_demand": len(df_demand),
                "agency_research_expenditures": len(df_exp),
                "resource_consumption": len(df_res),
                "satellite_manufacturing_requirements": len(df_mfg),
                "space_infrastructure_requirements": len(df_infra),
                "research_investment_future_projects": len(df_proj)
            },
            "total_records": (
                len(df_missions) + len(df_satellites) + len(df_launches) +
                len(df_demand) + len(df_exp) + len(df_res) +
                len(df_mfg) + len(df_infra) + len(df_proj)
            )
        }

        with open(self.metadata_dir / f"synthetic_generation_profile_{profile}.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        print(f"[SUCCESS] Synthetic generation completed: {summary['total_records']} total records generated for profile='{profile}'.")
        return summary

if __name__ == "__main__":
    gen = SyntheticDataGenerator()
    gen.generate_profile("small")
