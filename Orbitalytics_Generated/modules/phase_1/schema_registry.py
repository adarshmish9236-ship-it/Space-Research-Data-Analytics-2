"""
ORBITALYTICS - Phase 1 Schema Registry
Defines canonical schemas, data types, primary keys, foreign keys, and validation rules
across the 5 formal space research data domains and 9 core datasets.
"""

from typing import Dict, List, Any

# Five Formal Data Domains
DOMAINS = {
    "DOMAIN_1": "Satellite Component Demand",
    "DOMAIN_2": "Space Research Resource Consumption",
    "DOMAIN_3": "Satellite Manufacturing Requirements",
    "DOMAIN_4": "Launch and Mission Requirements",
    "DOMAIN_5": "Infrastructure and Research Investment"
}

# Canonical Schema Specifications for the 9 Core Datasets
CORE_DATASET_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "space_missions": {
        "domain": "DOMAIN_4",
        "description": "Historical space missions, flight objectives, and programmatic parameters.",
        "primary_key": "mission_id",
        "foreign_keys": {
            "agency_id": ("dim_agencies", "agency_id")
        },
        "required_columns": [
            "mission_id", "mission_name", "agency_id", "agency_name", "mission_type",
            "launch_date", "year", "quarter", "budget_million_usd", "payload_mass_kg",
            "status", "crew_size", "duration_days", "data_origin"
        ],
        "column_types": {
            "mission_id": "string",
            "mission_name": "string",
            "agency_id": "string",
            "agency_name": "string",
            "mission_type": "string",
            "launch_date": "date_iso",
            "year": "integer",
            "quarter": "string",
            "budget_million_usd": "float",
            "payload_mass_kg": "float",
            "status": "string",
            "crew_size": "integer",
            "duration_days": "integer",
            "data_origin": "string"
        },
        "valid_categories": {
            "mission_type": [
                "Earth Observation", "Satellite Communications", "Planetary Exploration",
                "Deep Space Astrophysics", "Human Spaceflight", "Technology Demonstration",
                "Space Weather & Heliophysics"
            ],
            "status": ["Successful", "Operational", "In-Flight", "Completed", "Partial Failure", "Retired", "Failed"],
            "data_origin": ["real", "synthetic"]
        }
    },
    "satellites_orbital": {
        "domain": "DOMAIN_4",
        "description": "Orbital mechanics, spacecraft mass, power, and operational characteristics.",
        "primary_key": "satellite_id",
        "foreign_keys": {
            "operator_agency_id": ("dim_agencies", "agency_id"),
            "associated_mission_id": ("space_missions", "mission_id")
        },
        "required_columns": [
            "satellite_id", "satellite_name", "operator_agency_id", "operator_agency_name",
            "associated_mission_id", "orbit_type", "altitude_km", "inclination_deg",
            "launch_year", "expected_lifetime_years", "dry_mass_kg", "power_consumption_w",
            "telemetry_band", "operational_status", "data_origin"
        ],
        "column_types": {
            "satellite_id": "string",
            "satellite_name": "string",
            "operator_agency_id": "string",
            "operator_agency_name": "string",
            "associated_mission_id": "string",
            "orbit_type": "string",
            "altitude_km": "float",
            "inclination_deg": "float",
            "launch_year": "integer",
            "expected_lifetime_years": "integer",
            "dry_mass_kg": "float",
            "power_consumption_w": "float",
            "telemetry_band": "string",
            "operational_status": "string",
            "data_origin": "string"
        },
        "valid_categories": {
            "orbit_type": [
                "LEO (Low Earth Orbit)", "MEO (Medium Earth Orbit)", "GEO (Geostationary)",
                "SSO (Sun-Synchronous)", "Deep Space / Lunar", "Lagrange Points (L1/L2)"
            ],
            "operational_status": ["Active", "Decommissioned", "Decayed", "Standby"],
            "data_origin": ["real", "synthetic"]
        }
    },
    "launch_activities": {
        "domain": "DOMAIN_4",
        "description": "Orbital space launches, rocket vehicle classes, spaceports, and outcomes.",
        "primary_key": "launch_id",
        "foreign_keys": {
            "mission_id": ("space_missions", "mission_id")
        },
        "required_columns": [
            "launch_id", "mission_id", "launch_date", "year", "month", "vehicle",
            "launch_site", "country", "launch_outcome", "commercial_flag",
            "launch_cost_million_usd", "payload_to_orbit_kg", "data_origin"
        ],
        "column_types": {
            "launch_id": "string",
            "mission_id": "string",
            "launch_date": "date_iso",
            "year": "integer",
            "month": "integer",
            "vehicle": "string",
            "launch_site": "string",
            "country": "string",
            "launch_outcome": "string",
            "commercial_flag": "boolean",
            "launch_cost_million_usd": "float",
            "payload_to_orbit_kg": "float",
            "data_origin": "string"
        },
        "valid_categories": {
            "launch_outcome": ["Success", "Partial Failure", "Launch Abort", "Catastrophic Failure"],
            "data_origin": ["real", "synthetic"]
        }
    },
    "equipment_component_demand": {
        "domain": "DOMAIN_1",
        "description": "Discrete equipment and flight hardware demand observations for forecasting.",
        "primary_key": "demand_id",
        "foreign_keys": {
            "component_id": ("reference_components", "component_id"),
            "agency_id": ("reference_agencies", "agency_id")
        },
        "required_columns": [
            "demand_id", "date", "year", "month", "quarter", "component_id", "component_name",
            "component_category", "agency_id", "agency_name", "target_satellite_class",
            "units_demanded", "units_manufactured", "units_procured", "unit_of_measure",
            "avg_unit_cost_thousand_usd", "total_demand_value_million_usd", "lead_time_days",
            "shortage_risk", "data_origin"
        ],
        "column_types": {
            "demand_id": "string",
            "date": "date_iso",
            "year": "integer",
            "month": "integer",
            "quarter": "string",
            "component_id": "string",
            "component_name": "string",
            "component_category": "string",
            "agency_id": "string",
            "agency_name": "string",
            "target_satellite_class": "string",
            "units_demanded": "integer",
            "units_manufactured": "integer",
            "units_procured": "integer",
            "unit_of_measure": "string",
            "avg_unit_cost_thousand_usd": "float",
            "total_demand_value_million_usd": "float",
            "lead_time_days": "integer",
            "shortage_risk": "string",
            "data_origin": "string"
        },
        "valid_categories": {
            "component_category": [
                "Power Systems", "Avionics", "Propulsion", "Communications",
                "Attitude Control", "Navigation", "Payload Instruments"
            ],
            "shortage_risk": ["Low", "Medium", "High", "Critical"],
            "data_origin": ["real", "synthetic"]
        }
    },
    "agency_research_expenditures": {
        "domain": "DOMAIN_5",
        "description": "Macro-economic monthly R&D, infrastructure, and operations expenditures.",
        "primary_key": "expenditure_id",
        "foreign_keys": {
            "agency_id": ("reference_agencies", "agency_id")
        },
        "required_columns": [
            "expenditure_id", "date", "year", "month", "quarter", "agency_id", "agency_name",
            "country", "rd_expenditure_million_usd", "infrastructure_expenditure_million_usd",
            "mission_operations_million_usd", "total_monthly_expenditure_million_usd",
            "currency", "data_origin"
        ],
        "column_types": {
            "expenditure_id": "string",
            "date": "date_iso",
            "year": "integer",
            "month": "integer",
            "quarter": "string",
            "agency_id": "string",
            "agency_name": "string",
            "country": "string",
            "rd_expenditure_million_usd": "float",
            "infrastructure_expenditure_million_usd": "float",
            "mission_operations_million_usd": "float",
            "total_monthly_expenditure_million_usd": "float",
            "currency": "string",
            "data_origin": "string"
        },
        "valid_categories": {
            "currency": ["USD"],
            "data_origin": ["real", "synthetic"]
        }
    },
    "resource_consumption": {
        "domain": "DOMAIN_2",
        "description": "Propellants, power, shielding, and telemetry consumption for forecasting.",
        "primary_key": "consumption_id",
        "foreign_keys": {
            "resource_id": ("reference_resources", "resource_id"),
            "agency_id": ("reference_agencies", "agency_id"),
            "mission_id": ("space_missions", "mission_id")
        },
        "required_columns": [
            "consumption_id", "date", "year", "month", "quarter", "resource_id", "resource_name",
            "resource_category", "agency_id", "agency_name", "mission_id", "quantity_consumed",
            "unit_of_measure", "procurement_cost_k_usd", "data_origin"
        ],
        "column_types": {
            "consumption_id": "string",
            "date": "date_iso",
            "year": "integer",
            "month": "integer",
            "quarter": "string",
            "resource_id": "string",
            "resource_name": "string",
            "resource_category": "string",
            "agency_id": "string",
            "agency_name": "string",
            "mission_id": "string",
            "quantity_consumed": "float",
            "unit_of_measure": "string",
            "procurement_cost_k_usd": "float",
            "data_origin": "string"
        },
        "valid_categories": {
            "resource_category": [
                "Propellant & Oxidizer", "Liquid Fuel", "Cryogenic Fuel",
                "Storable Propellant", "Spacecraft Materials", "Bandwidth & Communications",
                "Power & Energy"
            ],
            "data_origin": ["real", "synthetic"]
        }
    },
    "satellite_manufacturing_requirements": {
        "domain": "DOMAIN_3",
        "description": "Cleanroom production orders, vibration tests, and manufacturing throughput.",
        "primary_key": "order_id",
        "foreign_keys": {
            "agency_id": ("reference_agencies", "agency_id")
        },
        "required_columns": [
            "order_id", "agency_id", "agency_client", "satellite_class", "units_ordered",
            "delivery_year", "cleanroom_hours_required", "vibration_testing_pass",
            "contract_value_million_usd", "data_origin"
        ],
        "column_types": {
            "order_id": "string",
            "agency_id": "string",
            "agency_client": "string",
            "satellite_class": "string",
            "units_ordered": "integer",
            "delivery_year": "integer",
            "cleanroom_hours_required": "integer",
            "vibration_testing_pass": "boolean",
            "contract_value_million_usd": "float",
            "data_origin": "string"
        },
        "valid_categories": {
            "satellite_class": [
                "CubeSat (1U-12U)", "SmallSat (<500kg)",
                "Medium Satellite (500-2000kg)", "Heavy Geosynchronous Bus (>2000kg)"
            ],
            "data_origin": ["real", "synthetic"]
        }
    },
    "space_infrastructure_requirements": {
        "domain": "DOMAIN_5",
        "description": "Deep space network antenna time, cryogenic vacuum chambers, and facility utilization.",
        "primary_key": "infrastructure_record_id",
        "foreign_keys": {
            "agency_id": ("reference_agencies", "agency_id")
        },
        "required_columns": [
            "infrastructure_record_id", "date", "year", "month", "facility_name",
            "facility_type", "agency_id", "agency_name", "location", "utilization_rate_pct",
            "queued_backlog_hours", "maintenance_downtime_days", "data_origin"
        ],
        "column_types": {
            "infrastructure_record_id": "string",
            "date": "date_iso",
            "year": "integer",
            "month": "integer",
            "facility_name": "string",
            "facility_type": "string",
            "agency_id": "string",
            "agency_name": "string",
            "location": "string",
            "utilization_rate_pct": "float",
            "queued_backlog_hours": "integer",
            "maintenance_downtime_days": "integer",
            "data_origin": "string"
        },
        "valid_categories": {
            "facility_type": [
                "Ground Station Network", "Cryogenic Testing", "High-Performance Compute",
                "Radar Tracking", "Environmental Testing"
            ],
            "data_origin": ["real", "synthetic"]
        }
    },
    "research_investment_future_projects": {
        "domain": "DOMAIN_5",
        "description": "Strategic future projects, technology readiness levels (TRL), and planned investments.",
        "primary_key": "project_id",
        "foreign_keys": {
            "agency_id": ("reference_agencies", "agency_id")
        },
        "required_columns": [
            "project_id", "project_title", "agency_id", "lead_agency", "country",
            "research_theme", "target_commencement_year", "estimated_investment_million_usd",
            "priority_tier", "technology_readiness_level", "project_status", "data_origin"
        ],
        "column_types": {
            "project_id": "string",
            "project_title": "string",
            "agency_id": "string",
            "lead_agency": "string",
            "country": "string",
            "research_theme": "string",
            "target_commencement_year": "integer",
            "estimated_investment_million_usd": "float",
            "priority_tier": "string",
            "technology_readiness_level": "integer",
            "project_status": "string",
            "data_origin": "string"
        },
        "valid_categories": {
            "priority_tier": ["Critical Strategic", "High Priority", "Scientific Discovery", "Exploratory"],
            "project_status": ["Proposed", "Funded - Phase A", "Phase B Development", "Approved"],
            "data_origin": ["real", "synthetic"]
        }
    }
}

class SchemaRegistry:
    @staticmethod
    def get_schema(dataset_name: str) -> Dict[str, Any]:
        if dataset_name not in CORE_DATASET_SCHEMAS:
            raise KeyError(f"Dataset '{dataset_name}' not registered in SchemaRegistry.")
        return CORE_DATASET_SCHEMAS[dataset_name]

    @staticmethod
    def list_datasets() -> List[str]:
        return list(CORE_DATASET_SCHEMAS.keys())

    @staticmethod
    def get_domain(dataset_name: str) -> str:
        schema = SchemaRegistry.get_schema(dataset_name)
        return DOMAINS.get(schema["domain"], "Unknown Domain")
