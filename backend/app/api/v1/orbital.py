"""
ORBITALYTICS Phase 11 & Advanced Aerospace Visualization
API v1: Live Orbital Trajectory, SGP4 Ephemeris & Satellite Tracking Router
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from app.services.orbital_service import OrbitalService

router = APIRouter(prefix="/orbital", tags=["Orbital Mechanics & Satellite Ephemeris"])
orbital_service = OrbitalService()


@router.get("/satellites")
def get_propagated_satellites(
    orbit_type: Optional[str] = Query(None, description="Filter by orbit class: LEO, MEO, GEO, SSO, or ALL"),
    search: Optional[str] = Query(None, description="Search by name, NORAD ID, operator, or category")
):
    """
    Returns real-time SGP4 propagated positions, velocities, and geodetic coordinates
    for all tracked active satellites.
    """
    try:
        return orbital_service.get_satellites_list(orbit_class=orbit_type, search=search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orbital propagation failed: {str(e)}")


@router.get("/satellites/{satellite_id}")
def get_satellite_details(satellite_id: str):
    """
    Returns comprehensive ephemeris, orbital parameters, and complete 3D trajectory points
    for a specific satellite by NORAD ID or object name.
    """
    sat = orbital_service.get_satellite_by_id(satellite_id)
    if not sat:
        raise HTTPException(status_code=404, detail=f"Satellite with ID or name '{satellite_id}' not found in active catalog")
    return sat


@router.get("/positions")
def get_satellite_positions(
    orbit_type: Optional[str] = Query(None, description="Optional orbit filter: LEO, MEO, GEO, SSO")
):
    """
    Returns streamlined position packets (lat, lon, alt_km, velocity_km_s)
    optimized for high-frequency frontend rendering loops.
    """
    try:
        sats = orbital_service.get_satellites_list(orbit_class=orbit_type)
        return [
            {
                "norad_id": s["norad_id"],
                "name": s["name"],
                "orbit_class": s["orbit_class"],
                "latitude": s["telemetry"]["latitude"],
                "longitude": s["telemetry"]["longitude"],
                "altitude_km": s["telemetry"]["altitude_km"],
                "velocity_km_s": s["telemetry"]["velocity_km_s"],
                "timestamp_utc": s["timestamp_utc"]
            }
            for s in sats
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trajectories")
def get_all_orbital_trajectories(
    orbit_type: Optional[str] = Query(None, description="Filter by orbit class: LEO, MEO, GEO, SSO")
):
    """
    Returns precalculated 3D orbital trajectories for one full revolution period.
    """
    try:
        return orbital_service.get_all_trajectories(orbit_class=orbit_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/catalog")
def get_satellite_catalog():
    """
    Returns metadata catalog of all registered authentic space objects,
    including international designators (COSPAR), operators, and launch history.
    """
    return [
        {
            "norad_id": s["norad_id"],
            "cospar_id": s.get("cospar_id", "N/A"),
            "name": s["name"],
            "operator": s["operator"],
            "orbit_class": s["orbit_class"],
            "category": s.get("category", "Satellite"),
            "launch_year": s.get("launch_year", 2020)
        }
        for s in orbital_service.catalog
    ]


@router.get("/data-status")
def get_orbital_data_status():
    """
    Returns data provenance metadata, SGP4 engine health, catalog breakdown,
    and telemetry synchronization status.
    """
    return orbital_service.get_data_status()


@router.post("/sync")
def sync_celestrak_elements(group: str = Query("stations", description="CelesTrak group: stations, visual, gps-ops, geo, resource")):
    """
    Triggers an on-demand refresh of orbital elements from the CelesTrak GP API.
    Falls back gracefully to cached data if external network is unavailable.
    """
    return orbital_service.refresh_from_celestrak(group=group)
