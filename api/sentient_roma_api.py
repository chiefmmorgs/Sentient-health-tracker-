from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from roma_bridge.roma_config import RomaBridge
from storage.db import HealthDatabase

app = FastAPI(title="Sentient Health Tracker - ROMA Hybrid")
roma_bridge = RomaBridge()
db = HealthDatabase()

@app.get("/roma-info")
async def get_roma_info():
    return {
        "framework": "ROMA (hybrid-local)",
        "version": "hybrid",
        "agents": ["data_ingestion", "metrics_analysis", "coaching", "reporting"],
        "task_flows": ["weekly_health_analysis", "quick_analysis", "coaching_session"]
    }

@app.post("/analyze")
async def quick_analysis(data: Dict[str, Any]):
    try:
        roma_result = await roma_bridge.execute_health_task(
            task_type="quick_analysis",
            data=data or {}
        )
        return roma_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/weekly-report")
async def create_weekly_report(data: Dict[str, Any]):
    try:
        roma_result = await roma_bridge.execute_health_task(
            task_type="weekly_health_analysis",
            data=data or {}
        )
        report_id = await db.save_report(roma_result)
        return {"report_id": report_id, "roma_result": roma_result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def coaching_chat(message: Dict[str, Any]):
    try:
        roma_result = await roma_bridge.execute_health_task(
            task_type="coaching_session",
            data=message or {}
        )
        return roma_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
