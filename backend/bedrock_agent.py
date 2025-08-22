import boto3
import json
from typing import Dict, Any, List
from tools.air_quality import get_air_quality
from tools.trip_emissions import estimate_trip_emissions
from tools.wildfire import get_wildfire_alerts

SYSTEM_PROMPT = """
You are EcoAgents, an environmental assistant. You have access to these tools:

1. get_air_quality(city) - Get air quality data for cities like Toronto, Vancouver, Montreal, Calgary
2. estimate_trip_emissions(origin, destination, mode) - Calculate CO2 emissions for trips between cities
3. get_wildfire_alerts(region) - Get wildfire alerts for regions like BC, AB, ON

When a user asks about these topics, determine which tool to use and call it with the appropriate parameters.
Always respond in a helpful, conversational manner.

Available cities: Toronto, Vancouver, Montreal, Calgary
Available regions: BC, AB, ON
Available travel modes: car, bus, rail, flight
"""

TOOLS = {
    "get_air_quality": get_air_quality,
    "estimate_trip_emissions": estimate_trip_emissions,
    "get_wildfire_alerts": get_wildfire_alerts,
}

class BedrockEcoAgent:
    def __init__(self, model_id="anthropic.claude-3-haiku-20240307-v1:0"):
        self.bedrock = boto3.client('bedrock-runtime')
        self.model_id = model_id
    
    def call_bedrock(self, messages: List[Dict[str, str]]) -> str:
        """Call AWS Bedrock with a conversation."""
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "temperature": 0.7,
                "system": SYSTEM_PROMPT,
                "messages": messages
            }
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            
            # Log token usage for free tier monitoring
            usage = response_body.get('usage', {})
            print(f"Tokens used - Input: {usage.get('input_tokens', 0)}, Output: {usage.get('output_tokens', 0)}")
            
            return response_body['content'][0]['text'].strip()
            
        except Exception as e:
            return f"Error calling Bedrock: {str(e)}"
    
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
    
    def chat(self, message: str) -> str:
        """Process a user message using Bedrock for understanding and tool routing."""
        try:
            # First, let's try to use Bedrock to understand the intent
            messages = [
                {"role": "user", "content": f"User asks: {message}\n\nDetermine if this requires a tool call. If yes, respond with JSON format: {{\"tool\": \"tool_name\", \"params\": {{...}}}}. If no, respond naturally."}
            ]
            
            bedrock_response = self.call_bedrock(messages)
            
            # Try to parse as JSON for tool calls
            try:
                tool_call = json.loads(bedrock_response)
                if "tool" in tool_call and "params" in tool_call:
                    # Execute the tool
                    result = self.route_tool(tool_call["tool"], tool_call["params"])
                    
                    # Format the response
                    if tool_call["tool"] == "get_air_quality":
                        city = tool_call["params"].get("city", "Unknown")
                        return f"Air quality in {city}: AQI {result['aqi']}, PM2.5: {result['pm25']} μg/m³"
                    
                    elif tool_call["tool"] == "estimate_trip_emissions":
                        return f"Trip from {result['origin']} to {result['destination']}: {result['distance_km']} km, {result['total_co2_g']} g CO2"
                    
                    elif tool_call["tool"] == "get_wildfire_alerts":
                        if result["alert_count"] > 0:
                            return f"Wildfire alerts for {result['region']}: {result['alert_count']} active fires."
                        else:
                            return f"No active wildfire alerts for {result['region']} at this time."
                    
                    else:
                        return f"Tool result: {result}"
                
            except json.JSONDecodeError:
                # Not a tool call, return the natural response
                return bedrock_response
            
        except Exception as e:
            # Fallback to simple keyword matching if Bedrock fails
            return self._fallback_chat(message)
    
    def _fallback_chat(self, message: str) -> str:
        """Fallback method using simple keyword matching."""
        message_lower = message.lower()
        
        # Check for air quality queries
        if "air quality" in message_lower or "aqi" in message_lower:
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
                        return f"Wildfire alerts for {region}: {result['alert_count']} active fires."
                    else:
                        return f"No active wildfire alerts for {region} at this time."
            
            return "I can check wildfire alerts for BC, AB, or ON. Which region would you like to know about?"
        
        # Default response
        else:
            return "Hello! I'm your environmental assistant. I can help you with air quality information, trip emissions estimates, and wildfire alerts. What would you like to know?"
