"""
ORBITALYTICS - Phase 1 Data Source Registry
Maintains a formal catalog of all external public data sources and synthetic models,
including publisher, licence, coverage, API links, and data gap disclosures.
"""

from typing import Dict, Any, List

DATA_SOURCES: Dict[str, Dict[str, Any]] = {
    "NASA_OPEN_DATA": {
        "source_id": "SRC-001",
        "publisher": "National Aeronautics and Space Administration (NASA)",
        "name": "NASA Open Data Portal & NSSDC Master Catalog",
        "url": "https://data.nasa.gov/",
        "api": "https://api.nasa.gov/",
        "licence": "Public Domain / CC0",
        "coverage": "1958 - Present",
        "format": "JSON / CSV / REST",
        "domains": ["Missions", "Satellites", "Planetary Trajectories"],
        "origin_type": "real",
        "data_gap_note": "Macro programmatic and orbital information only. Does not publish discrete component BOMs or procurement invoices."
    },
    "ESA_SCIENCE_PORTAL": {
        "source_id": "SRC-002",
        "publisher": "European Space Agency (ESA)",
        "name": "ESA Science Exploration Portal & Copernicus Hub",
        "url": "https://www.esa.int/Science_Exploration",
        "api": "https://scihub.copernicus.eu/",
        "licence": "CC BY-SA 3.0 IGO / Open Access",
        "coverage": "1975 - Present",
        "format": "XML / JSON / GeoTIFF",
        "domains": ["Earth Observation", "Space Science"],
        "origin_type": "real",
        "data_gap_note": "Scientific telemetry and mission milestones only."
    },
    "ISRO_OFFICIAL": {
        "source_id": "SRC-003",
        "publisher": "Indian Space Research Organisation (ISRO)",
        "name": "ISRO Missions & Launch Manifest Archives",
        "url": "https://www.isro.gov.in/",
        "api": "https://www.isro.gov.in/Missions.html",
        "licence": "Government of India Open Access",
        "coverage": "1969 - Present",
        "format": "HTML / Tabular Press Releases",
        "domains": ["Missions", "Launch Activities", "Lunar Exploration"],
        "origin_type": "real",
        "data_gap_note": "Vehicle manifests and mission payloads; no low-level component inventory."
    },
    "UNOOSA_REGISTRY": {
        "source_id": "SRC-004",
        "publisher": "United Nations Office for Outer Space Affairs (UNOOSA)",
        "name": "Register of Objects Launched into Outer Space",
        "url": "https://www.unoosa.org/oosa/en/spaceobjectregister/index.html",
        "api": "https://www.unoosa.org/oosa/osoindex/search-ng.jspx",
        "licence": "UN Treaty Public Domain",
        "coverage": "1962 - Present",
        "format": "CSV / Web Registry",
        "domains": ["Satellites", "Orbital Parameters", "State of Registry"],
        "origin_type": "real",
        "data_gap_note": "International orbital parameters; does not capture hardware consumption."
    },
    "ORBITALYTICS_SYNTHETIC_GENERATOR": {
        "source_id": "SRC-005",
        "publisher": "Orbitalytics Research Big Data Engineering Team",
        "name": "Physics-Informed Reproducible Aerospace Demand Simulator",
        "url": "https://github.com/orbitalytics/demand-simulator",
        "api": "modules.phase_1.synthetic_data_generator",
        "licence": "Apache-2.0 / Academic Research Use",
        "coverage": "2010 - 2026 (Monthly & Event-level)",
        "format": "CSV / Apache Parquet",
        "domains": ["Component Demand", "Resource Consumption", "Manufacturing", "Expenditures"],
        "origin_type": "synthetic",
        "data_gap_note": "Developed specifically to bridge the defense/ITAR secrecy gap in aerospace component supply chains."
    }
}

class DataSourceRegistry:
    @staticmethod
    def get_source(source_key: str) -> Dict[str, Any]:
        if source_key not in DATA_SOURCES:
            raise KeyError(f"Data source '{source_key}' not found in registry.")
        return DATA_SOURCES[source_key]

    @staticmethod
    def list_sources() -> List[Dict[str, Any]]:
        return list(DATA_SOURCES.values())
