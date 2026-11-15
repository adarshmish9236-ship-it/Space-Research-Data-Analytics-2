import math
from datetime import datetime, timezone
from sgp4.api import Satrec, jday

# Test with ISS (ZARYA) TLE
line1 = "1 25544U 98067A   26318.94812294  .00009771  00000-0  18276-3 0  9993"
line2 = "2 25544  51.6323 274.0377 0007413  26.4902 333.6464 15.49382049595126"

sat = Satrec.twoline2rv(line1, line2)
now = datetime.now(timezone.utc)
jd, fr = jday(now.year, now.month, now.day, now.hour, now.minute, now.second + now.microsecond * 1e-6)

e, r, v = sat.sgp4(jd, fr)
print(f"Error: {e}")
print(f"TEME Pos: {r} km")
print(f"TEME Vel: {v} km/s")

# GMST calculation
t_ut1 = (jd + fr - 2451545.0) / 36525.0
gmst_sec = 24110.54841 + 8640184.812866 * t_ut1 + 0.093104 * (t_ut1**2) - 6.2e-6 * (t_ut1**3)
gmst_rad = ((gmst_sec % 86400.0) / 86400.0) * 2 * math.pi

# ECEF
x, y, z = r
x_ecef = x * math.cos(gmst_rad) + y * math.sin(gmst_rad)
y_ecef = -x * math.sin(gmst_rad) + y * math.cos(gmst_rad)
z_ecef = z

# WGS84 Geodetic
a = 6378.137
f = 1.0 / 298.257223563
e2 = 2 * f - f**2
r_xy = math.sqrt(x_ecef**2 + y_ecef**2)
lon = math.degrees(math.atan2(y_ecef, x_ecef))

b = a * (1.0 - f)
e_prime_sq = (a**2 - b**2) / (b**2)
theta_b = math.atan2(z_ecef * a, r_xy * b)
lat_rad = math.atan2(z_ecef + e_prime_sq * b * (math.sin(theta_b)**3), r_xy - e2 * a * (math.cos(theta_b)**3))
n_val = a / math.sqrt(1.0 - e2 * (math.sin(lat_rad)**2))
alt_km = (r_xy / math.cos(lat_rad)) - n_val
lat = math.degrees(lat_rad)
velocity_km_s = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

print(f"ISS Geodetic: Lat={lat:.4f}°, Lon={lon:.4f}°, Alt={alt_km:.2f} km, Speed={velocity_km_s:.2f} km/s")
