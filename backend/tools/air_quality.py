MOCK = {
    "Toronto": {"aqi": 42, "pm25": 7.1},
    "Vancouver": {"aqi": 55, "pm25": 10.2},
    "Montreal": {"aqi": 38, "pm25": 6.8},
    "Calgary": {"aqi": 45, "pm25": 8.3}
}

def get_air_quality(city: str):
    """Get air quality data for a given city."""
    return MOCK.get(city, {"aqi": 50, "pm25": 9.0})
