from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bedrock_agent import BedrockEcoAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="EcoAgents", description="Environmental AI Assistant with AWS Bedrock")

# Initialize the Bedrock agent
try:
    agent = BedrockEcoAgent()
    bedrock_available = True
except Exception as e:
    print(f"Warning: Bedrock not available: {e}")
    print("Falling back to keyword-based agent...")
    from agent import EcoAgent
    agent = EcoAgent()
    bedrock_available = False

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    bedrock_used: bool

@app.get("/")
def read_root():
    return {
        "message": "EcoAgents - Environmental AI Assistant", 
        "status": "running",
        "bedrock_available": bedrock_available
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Chat with the environmental assistant."""
    try:
        response = agent.chat(request.message)
        return ChatResponse(response=response, bedrock_used=bedrock_available)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "agent": "EcoAgents",
        "bedrock_available": bedrock_available
    }

@app.get("/tools")
def list_tools():
    """List available tools."""
    return {
        "tools": [
            {
                "name": "get_air_quality",
                "description": "Get air quality data for cities",
                "parameters": {"city": "string"},
                "supported_cities": ["Toronto", "Vancouver", "Montreal", "Calgary"]
            },
            {
                "name": "estimate_trip_emissions", 
                "description": "Estimate CO2 emissions for trips between cities",
                "parameters": {"origin": "string", "destination": "string", "mode": "string"},
                "supported_cities": ["Toronto", "Vancouver", "Montreal", "Calgary"],
                "supported_modes": ["car", "bus", "rail", "flight"]
            },
            {
                "name": "get_wildfire_alerts",
                "description": "Get wildfire alerts for regions",
                "parameters": {"region": "string"},
                "supported_regions": ["BC", "AB", "ON"]
            }
        ],
        "bedrock_available": bedrock_available
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
