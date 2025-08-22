import math

# Simple emission factors (g CO2 per km)
EMISSION_FACTORS = {
    "car": 171.0,
    "bus": 104.0,
    "rail": 41.0,
    "flight": 255.0
}

# Mock city coordinates
CITY_COORDS = {
    "Toronto": (43.651, -79.347),
    "Vancouver": (49.282, -123.120),
    "Montreal": (45.501, -73.567),
    "Calgary": (51.044, -114.072)
}

def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula."""
    R = 6371  # Earth's radius in km
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def estimate_trip_emissions(origin: str, destination: str, mode: str = "car"):
    """Estimate CO2 emissions for a trip between two cities."""
    if origin not in CITY_COORDS or destination not in CITY_COORDS:
        return {"error": "City not found in database"}
    
    lat1, lon1 = CITY_COORDS[origin]
    lat2, lon2 = CITY_COORDS[destination]
    
    distance_km = haversine_km(lat1, lon1, lat2, lon2)
    factor = EMISSION_FACTORS.get(mode, EMISSION_FACTORS["car"])
    total_co2 = distance_km * factor
    
    return {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "distance_km": round(distance_km, 1),
        "emission_factor_g_per_km": factor,
        "total_co2_g": round(total_co2, 1)
    }
