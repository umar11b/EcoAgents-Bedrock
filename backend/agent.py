import boto3
import json
from typing import Dict, Any
from tools.air_quality import get_air_quality
from tools.trip_emissions import estimate_trip_emissions
from tools.wildfire import get_wildfire_alerts

SYSTEM_PROMPT = """
You are EcoAgents, a simple environmental assistant. You can help with:
- Air quality information for cities
- Trip emissions estimates between cities
- Wildfire alerts for regions

When a user asks about these topics, use the appropriate tool. Otherwise, provide helpful environmental information in a conversational way.

Always respond in a friendly, informative manner and explain what you're doing when using tools.
"""

TOOLS = {
    "get_air_quality": get_air_quality,
    "estimate_trip_emissions": estimate_trip_emissions,
    "get_wildfire_alerts": get_wildfire_alerts,
}

class EcoAgent:
    def __init__(self, model_id="anthropic.claude-3-sonnet-20240229-v1:0"):
        self.bedrock = boto3.client('bedrock-runtime')
        self.model_id = model_id
    
    def route_tool(self, name: str, payload: Dict[str, Any]):
        """Route a tool call to the appropriate function."""
        if name not in TOOLS:
            return {"error": f"Tool {name} not found"}
        
        try:
            fn = TOOLS[name]
            result = fn(**payload)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def chat(self, message: str):
        """Process a user message and return a response."""
        # For now, we'll do simple keyword matching
        # In a real implementation, this would use Bedrock to determine tool usage
        
        message_lower = message.lower()
        
        # Check for air quality queries
        if "air quality" in message_lower or "aqi" in message_lower:
            # Extract city name (simple approach)
            cities = ["Toronto", "Vancouver", "Montreal", "Calgary"]
            for city in cities:
                if city.lower() in message_lower:
                    result = self.route_tool("get_air_quality", {"city": city})
                    return f"Air quality in {city}: AQI {result['aqi']}, PM2.5: {result['pm25']} μg/m³"
            
            return "I can check air quality for Toronto, Vancouver, Montreal, or Calgary. Which city would you like to know about?"
        
        # Check for trip emissions
        elif "emissions" in message_lower or "carbon" in message_lower or "co2" in message_lower:
            cities = ["Toronto", "Vancouver", "Montreal", "Calgary"]
            found_cities = [city for city in cities if city.lower() in message_lower]
            
            if len(found_cities) >= 2:
                result = self.route_tool("estimate_trip_emissions", {
                    "origin": found_cities[0],
                    "destination": found_cities[1],
                    "mode": "car"
                })
                return f"Trip from {result['origin']} to {result['destination']}: {result['distance_km']} km, {result['total_co2_g']} g CO2"
            else:
                return "I can estimate emissions for trips between Toronto, Vancouver, Montreal, and Calgary. Please specify origin and destination cities."
        
        # Check for wildfire alerts
        elif "wildfire" in message_lower or "fire" in message_lower:
            regions = ["BC", "AB", "ON"]
            for region in regions:
                if region.lower() in message_lower or region in message_lower:
                    result = self.route_tool("get_wildfire_alerts", {"region": region})
                    if result["alert_count"] > 0:
                        return f"Wildfire alerts for {region}: {result['alert_count']} active fires. Check the details for more information."
                    else:
                        return f"No active wildfire alerts for {region} at this time."
            
            return "I can check wildfire alerts for BC, AB, or ON. Which region would you like to know about?"
        
        # Default response
        else:
            return "Hello! I'm your environmental assistant. I can help you with air quality information, trip emissions estimates, and wildfire alerts. What would you like to know?"
