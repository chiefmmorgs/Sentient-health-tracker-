"""
FastAPI entrypoint wired to ROMA engine and agents.
"""

from fastapi import FastAPI, Body, Header, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import os

# local imports
from roma_engine.sentient_roma_runner import ROMARunner
from storage.db import list_reports, get_report   # persistence

app = FastAPI(title="Sentient ROMA Health Tracker", version="0.1.0")
runner = ROMARunner()

API_KEY = os.getenv("API_KEY")

def require_key(x_api_key: str | None = Header(default=None)):
    if not API_KEY:  # if not set in .env, auth is disabled
        return
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

class WeeklyPayload(BaseModel):
    data: Dict[str, Any]

@app.get("/")
def root():
    return {"ok": True, "service": "sentient-roma-health-tracker"}

@app.get("/roma-info")
def roma_info():
    return {"roma": "Atomizer -> Planner -> Executor -> Aggregator"}

@app.get("/health")
def health(x_api_key: str | None = Header(default=None)):
    require_key(x_api_key)
    try:
        reports = list_reports(limit=1)
        db_ok = True
    except Exception:
        db_ok = False
    return {"ok": True, "api": "running", "db": "ok" if db_ok else "unavailable"}

@app.post("/analyze")
def analyze(payload: Dict[str, Any] = Body(...)):
    result = runner.analyze_single(payload)
    return {"analysis": result}

@app.post("/weekly-report")
def weekly_report(payload: WeeklyPayload):
    result = runner.run_weekly(payload.data)
    return {"report": result}

@app.post("/chat")
def chat(message: Dict[str, Any] = Body(...)):
    reply = runner.chat(message)
    return {"reply": reply}

@app.get("/example")
def example():
    return {"steps": 72000, "sleep_hours": 49, "workouts": 4, "water_liters": 14}

# -------------------------------
# Report persistence endpoints (protected)
# -------------------------------
@app.get("/reports")
def reports_list(limit: int = 10, x_api_key: str | None = Header(default=None)):
    require_key(x_api_key)
    return {"reports": list_reports(limit)}

@app.get("/reports/{report_id}")
def reports_get(report_id: int, x_api_key: str | None = Header(default=None)):
    require_key(x_api_key)
    r = get_report(report_id)
    if not r:
        return {"error": "not found"}
    return r

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sentient_roma_api:app",
                host=os.getenv("HOST","0.0.0.0"),
                port=int(os.getenv("PORT","8000")),
                reload=True)

