from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import EcoAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="EcoAgents", description="Environmental AI Assistant")

# Initialize the agent
agent = EcoAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"message": "EcoAgents - Environmental AI Assistant", "status": "running"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Chat with the environmental assistant."""
    try:
        response = agent.chat(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "EcoAgents"}

@app.get("/tools")
def list_tools():
    """List available tools."""
    return {
        "tools": [
            {
                "name": "get_air_quality",
                "description": "Get air quality data for cities",
                "parameters": {"city": "string"}
            },
            {
                "name": "estimate_trip_emissions", 
                "description": "Estimate CO2 emissions for trips between cities",
                "parameters": {"origin": "string", "destination": "string", "mode": "string"}
            },
            {
                "name": "get_wildfire_alerts",
                "description": "Get wildfire alerts for regions",
                "parameters": {"region": "string"}
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
