# Mock wildfire alerts data
MOCK_ALERTS = {
    "BC": [
        {
            "location": "Vancouver Island",
            "severity": "moderate",
            "area_ha": 150,
            "status": "active"
        },
        {
            "location": "Okanagan Valley",
            "severity": "high",
            "area_ha": 450,
            "status": "active"
        }
    ],
    "AB": [
        {
            "location": "Banff National Park",
            "severity": "low",
            "area_ha": 25,
            "status": "contained"
        }
    ],
    "ON": [
        {
            "location": "Northern Ontario",
            "severity": "moderate",
            "area_ha": 200,
            "status": "active"
        }
    ]
}

def get_wildfire_alerts(region: str):
    """Get wildfire alerts for a given region."""
    alerts = MOCK_ALERTS.get(region, [])
    return {
        "region": region,
        "alert_count": len(alerts),
        "alerts": alerts
    }
