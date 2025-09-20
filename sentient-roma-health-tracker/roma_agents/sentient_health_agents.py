"""
ROMA agents for health tracking.
Atomizer, Planner, Executors, Aggregator.
Now: Metrics and Reporting use OpenRouter (GPT-3.5 by default).
"""
from storage.db import save_report
from typing import Any, Dict, List
import os
import json
from litellm import completion

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")

def _ask_llm(prompt: str) -> str:
    if not OPENROUTER_KEY:
        return "Error: Missing OPENROUTER_API_KEY in .env"
    try:
        resp = completion(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            api_key=OPENROUTER_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
        return resp["choices"][0]["message"]["content"]
    except Exception as e:
        return f"LLM error: {e}"

class Atomizer:
    def is_atomic(self, task: Dict[str, Any]) -> bool:
        return task.get("kind") in {"ingest","metrics","coach","report"}

class Planner:
    def plan(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = task.get("data", {})
        return [
            {"kind": "ingest", "data": data},
            {"kind": "metrics", "data": data},
            {"kind": "coach", "data": {"message": task.get("data", {}).get("message", "Weekly health coaching based on user data")}},
            {"kind": "report", "data": data},
        ]

class DataIngestionAgent:
    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        data = task.get("data", {})
        if not isinstance(data, dict) or not data:
            return {"stage":"ingest","ok":False,"error":"No or invalid input data"}
        # Add simple normalization hooks here if needed
        return {"stage":"ingest","ok":True,"data":data}

class MetricsAnalysisAgent:
    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute quick metrics + ask GPT for a brief analysis.
        """
        d = task.get("data", {}) or {}
        steps = int(d.get("steps", 0) or 0)
        sleep_hours = float(d.get("sleep_hours", 0) or 0.0)
        workouts = int(d.get("workouts", 0) or 0)
        water_liters = float(d.get("water_liters", 0) or 0.0)

        # Simple derived scores
        activity_score = min(100, int(steps / 1000) + workouts * 10)
        hydration_score = min(100, int((water_liters / 14.0) * 100))  # 2L/day target for a week
        sleep_score = min(100, int((sleep_hours / 56.0) * 100))       # 8h/day target for a week

        summary = {
            "steps": steps,
            "sleep_hours": sleep_hours,
            "workouts": workouts,
            "water_liters": water_liters,
            "scores": {
                "activity": activity_score,
                "hydration": hydration_score,
                "sleep": sleep_score
            }
        }

        prompt = (
            "You are a health coach. Analyze these weekly metrics and give 5 focused insights with 3 short actions.\n"
            f"JSON metrics:\n{json.dumps(summary)}\n"
            "Keep it practical. Avoid medical claims."
        )
        ai_analysis = _ask_llm(prompt)
        return {"stage":"metrics","ok":True,"summary":summary,"ai_analysis":ai_analysis}

class CoachingAgent:
    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        user_message = task.get("data", {}).get("message", "")
        if not user_message:
            return {"stage": "coach", "ok": False, "error": "No message provided"}
        reply = _ask_llm(f"Give me practical health advice: {user_message}")
        return {"stage":"coach","ok":True,"advice":reply}

class ReportingAgent:
    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        d = task.get("data", {}) or {}
        prompt = (
            "Create a concise weekly health report from this user data.\n"
            "Structure:\n"
            "- Summary (2 lines)\n"
            "- Highlights (3 bullets)\n"
            "- Risks to watch (2 bullets)\n"
            "- Next week plan (4 bullets)\n"
            f"JSON data:\n{json.dumps(d)}"
        )
        report = _ask_llm(prompt)
        try:
            rid = save_report(d, report)
        except Exception as e:
            return {"stage":"report","ok":True,"report":report,"save_error":str(e)}
        return {"stage":"report","ok":True,"report":report,"report_id":rid}

class Aggregator:
    def combine(self, parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"ok": True, "parts": parts}

