from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import httpx, os, logging

log = logging.getLogger("health")

app = FastAPI(title="Health Tracker")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Use docker service name in compose; if running locally, set ROMA_URL=http://localhost:5000
ROMA_BASE = os.getenv("ROMA_URL", "http://roma:5000") + "/api/simple"

class HealthData(BaseModel):
    data: Dict[str, Any]

def _bad(text: Optional[str]) -> bool:
    if not isinstance(text, str):
        return True
    t = text.strip().lower()
    return (t == "" or t.startswith("echo:") or t == "placeholder" or t == "ok")

async def _roma_analysis(data: Dict[str, Any], desc: str, goal: Optional[str] = None) -> Optional[str]:
    payload: Dict[str, Any] = {"data": data, "data_description": desc}
    if goal:
        payload["goal"] = goal
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{ROMA_BASE}/analysis", json=payload)
            if r.status_code == 200:
                js = r.json()
                if isinstance(js, dict):
                    out = js.get("final_output") or js.get("analysis") or js.get("summary")
                    if isinstance(out, str) and not _bad(out):
                        return out
                    if out and not isinstance(out, str):
                        return str(out)
    except Exception as e:
        log.debug(f"/analysis failed: {e}")
    return None

async def _roma_execute(goal: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{ROMA_BASE}/execute", json={"goal": goal})
            if r.status_code == 200:
                js = r.json()
                out = js.get("final_output")
                if isinstance(out, str) and not _bad(out):
                    return out
    except Exception as e:
        log.debug(f"/execute failed: {e}")
    return None

def analyze_health_locally(d: dict) -> dict:
    """Return structured insights for typical metrics."""
    out = {"insights": [], "flags": [], "summary": {}}

    # Resting heart rate (rHR)
    rhr = d.get("resting_hr")
    if isinstance(rhr, (int, float)):
        if rhr < 50:
            out["insights"].append("Very low resting HR; could be athletic or bradycardia—interpret in context.")
        elif 50 <= rhr <= 60:
            out["insights"].append("Excellent resting HR (well-trained range).")
        elif 61 <= rhr <= 70:
            out["insights"].append("Good resting HR.")
        elif 71 <= rhr <= 80:
            out["insights"].append("Slightly elevated resting HR—watch stress, sleep, hydration.")
        else:
            out["insights"].append("High resting HR—consider recovery, hydration, or check with a clinician if persistent.")
            out["flags"].append("resting_hr_high")
        out["summary"]["resting_hr"] = rhr

    # HRV
    hrv = d.get("hrv")
    if isinstance(hrv, (int, float)):
        if hrv >= 70:
            out["insights"].append("HRV looks strong—good recovery signal.")
        elif 50 <= hrv < 70:
            out["insights"].append("HRV is moderate—keep sleep and stress in check.")
        else:
            out["insights"].append("Low HRV—prioritize sleep, light activity, and hydration.")
            out["flags"].append("hrv_low")
        out["summary"]["hrv"] = hrv

    # Calories
    cals = d.get("calories")
    if isinstance(cals, (int, float)):
        out["summary"]["calories_week"] = cals
        if cals < 10000:
            out["insights"].append("Weekly calorie burn seems low—more daily movement or longer sessions could help.")
            out["flags"].append("calories_low")

    # Runs
    runs = d.get("runs")
    if isinstance(runs, (int, float)):
        runs = int(runs)
        out["summary"]["runs"] = runs
        if runs >= 3:
            out["insights"].append("Great running frequency—maintain 1 easy + 1 quality + 1 long structure.")
        else:
            out["insights"].append("Consider aiming for 3 runs/week (easy, quality, long).")
            out["flags"].append("runs_low")

    # Score: reward positives, penalize flags
    positives = 0
    if isinstance(rhr, (int, float)) and 50 <= rhr <= 60: positives += 1
    if isinstance(hrv, (int, float)) and hrv >= 70: positives += 1
    if isinstance(runs, int) and runs >= 3: positives += 1
    score = 70 + 5*positives - 10*len(out["flags"])
    score = max(0, min(100, score))
    out["score"] = score

    # Recommendations: de-dup and fill to 3
    recs = []
    if "hrv_low" in out["flags"]:
        recs.append("Prioritize 7–8h sleep, add a 10–15 min evening wind-down.")
    if "resting_hr_high" in out["flags"]:
        recs.append("Add low-intensity walks and hydration; check caffeine late-day.")
    if "calories_low" in out["flags"]:
        recs.append("Sneak in 2k extra steps/day with short walks.")
    if "runs_low" in out["flags"]:
        recs.append("Block 3 runs in your calendar to build consistency.")

    generic = [
        "Keep up hydration and consistent bed/wake times.",
        "Add 5–10 minutes of mobility after workouts.",
        "Take a short walk after meals when possible."
    ]
    for g in generic:
        if len(recs) >= 3: break
        if g not in recs: recs.append(g)

    out["recommendations"] = recs[:3]
    return out

def _fallback_weekly(data: Dict[str, Any]) -> str:
    steps = float(data.get("steps", 0))
    sleep = float(data.get("sleep_hours", 0))
    workouts = int(data.get("workouts", 0))
    water = float(data.get("water_liters", 0))
    avg_steps = steps / 7 if steps else 0
    avg_sleep = sleep / 7 if sleep else 0
    assess_steps = "✅ On track" if avg_steps >= 10000 else "⚠️ Aim for 10k/day"
    assess_sleep = "✅ On track" if avg_sleep >= 7 else "⚠️ Target 7–8h/night"
    assess_ex = "✅ ≥3 sessions" if workouts >= 3 else "⚠️ Try to reach 3+/week"

    rec1 = "Maintain your walking habit" if avg_steps >= 10000 else "Add a 15–20 min brisk walk after lunch"
    rec2 = "Keep consistent bedtime" if avg_sleep >= 7 else "Move bedtime earlier by ~30 minutes"
    rec3 = "Nice training cadence" if workouts >= 3 else "Schedule workouts on calendar to lock them in"

    return (
        "Weekly Health Report\n"
        "--------------------\n"
        f"• Daily Steps Avg: {avg_steps:.0f}\n"
        f"• Daily Sleep Avg: {avg_sleep:.1f}h\n"
        f"• Workouts: {workouts}\n"
        f"• Water: {water} L/week\n\n"
        "Assessment:\n"
        f"- Steps: {assess_steps}\n"
        f"- Sleep: {assess_sleep}\n"
        f"- Exercise: {assess_ex}\n\n"
        "Recommendations:\n"
        f"1) {rec1}\n"
        f"2) {rec2}\n"
        f"3) {rec3}\n"
    )

@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{ROMA_BASE}/status")
            roma_ok = r.status_code == 200
    except Exception:
        roma_ok = False
    return {"status": "healthy", "roma_available": roma_ok, "timestamp": datetime.utcnow().isoformat()}

@app.post("/weekly-report")
async def weekly_report(request: HealthData):
    d = request.data

    # Try ROMA /analysis first
    goal = ("Summarize the week, compute daily averages, give a short health assessment, "
            "and 2–3 specific, actionable recommendations. Keep it concise. Do NOT repeat my prompt.")
    a1 = await _roma_analysis(d, "weekly health metrics", goal=goal)
    if a1:
        text = a1
    else:
        # Fallback to ROMA /execute
        goal_exec = f"""
You are a helpful health coach. Do NOT echo my instructions.
Using the following weekly data, write a brief report with:
- Daily averages
- Health assessment
- 2–3 concrete recommendations

Data:
- Steps: {d.get('steps', 0)} total
- Sleep: {d.get('sleep_hours', 0)} hours total
- Workouts: {d.get('workouts', 0)} sessions
- Water: {d.get('water_liters', 0)} liters
"""
        a2 = await _roma_execute(goal_exec)
        text = a2 if a2 else _fallback_weekly(d)

    metrics = {
        "daily_steps_avg": round(d.get("steps", 0)/7, 0) if d.get("steps") else 0,
        "daily_sleep_avg": round(d.get("sleep_hours", 0)/7, 1) if d.get("sleep_hours") else 0.0,
        "workouts": int(d.get("workouts", 0) or 0),
        "water_liters": float(d.get("water_liters", 0) or 0.0),
    }
    return {"status": "success", "report": text, "metrics": metrics, "data_analyzed": d}

@app.post("/analyze")
async def analyze(request: HealthData):
    d = request.data

    # Try ROMA first
    a1 = await _roma_analysis(d, "health metrics",
                              goal="Provide key observations, areas of concern, positive trends. Return brief text.")
    if a1 and isinstance(a1, str):
        return {"status": "success", "analysis": a1}

    a2 = await _roma_execute(f"You are a health data analyst. Analyze these metrics (concise, no echo): {d}")
    if a2 and isinstance(a2, str):
        return {"status": "success", "analysis": a2}

    # Structured local fallback
    struct = analyze_health_locally(d)
    return {"status": "success", "analysis": struct}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
