# EcoAgents – Basic Case Study with Amazon Bedrock AgentCore

> **One‑liner:** A simple case study to explore Amazon Bedrock AgentCore by creating an environmental assistant with basic mock tools.

---

## 📖 Purpose

This project is designed as a **learning case study**. It follows the AWS HQ workshop on Bedrock AgentCore but keeps the scope small and approachable. Instead of general tools like a calculator, it introduces **simple environmental tools** to practice wiring Bedrock models to custom logic.

The focus is on **understanding the flow**: model → agent runtime → tool → response. It’s not meant to be production-grade or overly complex.

---

## 🛠️ Tech Stack

- **Amazon Bedrock** (LLMs)
- **AgentCore Runtime** (agent orchestration)
- **Python (AWS SDK / boto3)**
- **FastAPI** (for local API testing)
- **Mock Data Sources** (simple JSON/cached data)

---

## ✨ Example Tools

1. `get_air_quality(city)` → returns simple AQI values from a mock table
2. `estimate_trip_emissions(origin, destination, mode)` → rough CO₂ estimate using distance × factor
3. `get_wildfire_alerts(region)` → mock wildfire alerts

> All tools are **mocked first**. You can later replace them with real APIs if you want to go deeper.

---

## 🗂️ Project Structure

```
agentops-ecoagents/
  ├─ backend/
  │  ├─ app.py           # FastAPI app
  │  ├─ agent.py         # Runtime wiring to Bedrock + tools
  │  ├─ tools/
  │  │  ├─ air_quality.py
  │  │  ├─ trip_emissions.py
  │  │  └─ wildfire.py
  │  └─ requirements.txt
  ├─ docs/
  │  └─ workshop-notes.md
  └─ README.md
```

---

## 🔧 Example Tool (Mock)

```python
# backend/tools/air_quality.py
MOCK = {
  "Toronto": {"aqi": 42, "pm25": 7.1},
  "Vancouver": {"aqi": 55, "pm25": 10.2}
}

def get_air_quality(city: str):
    return MOCK.get(city, {"aqi": 50, "pm25": 9.0})
```

---

## 🤖 Agent Runtime (Skeleton)

```python
# backend/agent.py
SYSTEM_PROMPT = """
You are EcoAgents, a simple environmental assistant.
Use tools when possible, otherwise explain with text.
"""

TOOLS = {
  "get_air_quality": get_air_quality,
  "estimate_trip_emissions": estimate_trip_emissions,
}

def route_tool(name, payload):
    fn = TOOLS[name]
    return fn(**payload)
```

---

## 🏁 Local Dev

```
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app:app --reload
```

---

## 🧭 Roadmap (Keep It Simple)

- ✅ Add mock tools (air quality, emissions, wildfire)
- ✅ Run locally with FastAPI
- 🔜 Try calling Bedrock AgentCore
- 🔜 Swap in one real dataset/API

---

## 🎯 Takeaway

This project is a **basic case study** to get hands-on with Bedrock AgentCore. It shows recruiters and peers that you:

- Experimented with **AWS Bedrock**
- Understood **agent → tool integration**
- Applied it to a meaningful theme (**environmental insights**)
