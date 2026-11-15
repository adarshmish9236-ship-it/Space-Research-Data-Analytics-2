import sys
from pathlib import Path
sys.path.insert(0, str(Path("backend").resolve()))

from app.services.orbital_service import OrbitalService

service = OrbitalService()
status = service.get_data_status()
print("Data Status:", status)

sats = service.get_satellites_list()
print(f"Total Propagated Satellites: {len(sats)}")
print("Sample Satellite:")
print(f"  Name: {sats[0]['name']}")
print(f"  Orbit: {sats[0]['orbit_class']}")
print(f"  Altitude: {sats[0]['telemetry']['altitude_km']} km")
print(f"  Velocity: {sats[0]['telemetry']['velocity_km_s']} km/s")
print(f"  Lat/Lon: {sats[0]['telemetry']['latitude']}°, {sats[0]['telemetry']['longitude']}°")

iss = service.get_satellite_by_id("25544")
print(f"\nISS Trajectory Points: {len(iss['trajectory'])}")
print(f"  Sample Point 0: {iss['trajectory'][0]}")
print(f"  Sample Point 10: {iss['trajectory'][10]}")
