# 🤖 Sentient ROMA Health Tracker

**Advanced AI-powered health analysis using the Sentient AGI ROMA framework.**  
A practical, self-hosted multi-agent system that turns raw weekly metrics into clear human reports, ad-hoc insights, and free-form coaching—**with your data stored locally** and protected by an API key.

**ROMA Pattern:**  
**Atomizer → Planner → Executors (Ingest / Metrics / Coach / Report) → Aggregator**

[![FastAPI](https://img.shields.io/badge/FastAPI-ready-009688)](#)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](#)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ What You Built (and Why)

- **Health Tracker (FastAPI)** – your public API with:
  - `/weekly-report` – concise weekly summaries with daily averages + 2–3 actionable tips
  - `/analyze` – structured insights (flags, score, recommendations)
  - `/chat` – free-form AI coaching (“plan my week”, etc.)
  - `/reports` – saved outputs in **SQLite**, browsable via API (and optional mini admin page)
  - **Security** – API key guard for sensitive routes and (optionally) save actions
  - **Fallbacks** – still works even if the LLM isn’t reachable
- **ROMA Service** – your “sentient rumor”/meta-agent layer that decomposes problems and calls the LLM (OpenRouter). It’s the quiet power under the hood; when it’s unavailable, Health Tracker falls back to local logic so you always get results.
- **Persistence** – reports saved to `./data/health.db` on your machine via a Docker bind mount.

This setup gives you a **private, reliable** health backend you can front with a tiny website or a Telegram bot.

---

## 🏗️ How It Connects

[ Client / Browser / Telegram / cURL ]
|
v
FastAPI "health-tracker" (http://localhost:8000
)
├─ /weekly-report ← generate & (optionally) save weekly summary
├─ /analyze ← structured metrics insights
├─ /chat ← free-form coaching
└─ /reports (key) ← list/get/delete saved outputs (SQLite)
|
v
ROMA service (http://roma:5000/api/simple
)
├─ /status
├─ /execute
└─ /analysis
|
v
OpenRouter LLM (uses your OPENROUTER_API_KEY)

---

## 🔎 What Is ROMA (the undertone)

**ROMA** is a **meta-agent framework** that uses a recursive plan–execute loop. It decides when a request is atomic vs. complex, decomposes tasks, executes subtasks (in parallel where possible), and aggregates results.

 ```python
def solve(task):
    if is_atomic(task):           # Atomizer
        return execute(task)      # Executor (LLM/tool)
    else:
        subtasks = plan(task)     # Planner
        results = [solve(st) for st in subtasks]
        return aggregate(results) # Aggregator

```

In this repo, Health Tracker uses ROMA’s /analysis and /execute for richer language output. If ROMA returns a low-value “echo/placeholder” or is unreachable, Health Tracker falls back to local code.

✨ Features
ROMA-powered recursive task handling for smarter outputs

Agents

DataIngestionAgent – validates/normalizes inputs

MetricsAnalysisAgent – computes basics + queries LLM for insights

CoachingAgent – personalized, actionable tips (via OpenRouter)

ReportingAgent – weekly summary stored to SQLite

FastAPI with clean REST endpoints and Swagger docs

SQLite persistence via Docker volume (./data/health.db)

API Key guard for sensitive routes

Dockerized one-command spin-up

🚀 Quick Start
1) Clone
```
git clone https://github.com/chiefmmorgs/Sentient-health-tracker-.git
cd Sentient-health-tracker-
```
2) Environment
```
Create .env in the project root (keep it private; it’s in .gitignore):
```
# LLM access used by ROMA
```
OPENROUTER_API_KEY=sk-your-openrouter-key

# Protects /reports (and optionally save actions on other endpoints)
API_KEY=your-secret-key

# Health Tracker DB (absolute path inside container)
DB_URL=sqlite:////app/data/health.db

```
Generate a strong key:

openssl rand -hex 32

or python3 -c "import secrets; print(secrets.token_urlsafe(32))"

Note: ROMA_URL is set in compose.yml to http://roma:5000 (internal Docker DNS).

3) Run with Docker Compose
```
docker compose up -d --build
# wait until API is live
until curl -sSf http://127.0.0.1:8000/health >/dev/null; do echo "waiting..."; sleep 1; done
```
4) Test

Health (protected by key):
```
curl -s http://127.0.0.1:8000/health -H "X-API-Key: $API_KEY" | jq .

```
Weekly report:
```
# compute only (no save)
curl -s -X POST http://127.0.0.1:8000/weekly-report \
  -H "Content-Type: application/json" \
  -d '{"data":{"steps":72000,"sleep_hours":49,"workouts":4,"water_liters":14}}' | jq .

# compute + save (requires API key)
curl -s -X POST "http://127.0.0.1:8000/weekly-report?save=true" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"data":{"steps":72000,"sleep_hours":49,"workouts":4,"water_liters":14}}' | jq .
```

Open docs:
http://127.0.0.1:8000/docs

🔗 Endpoints

GET /health – API + ROMA heartbeat (requires X-API-Key)

GET /roma-info – (optional) ROMA architecture summary

POST /analyze – quick metrics analysis (JSON insights)

POST /weekly-report – full ROMA pipeline (ingest → metrics → coach → report)

POST /chat – AI coaching on an input message

GET /reports – list saved reports (requires key)

GET /reports/{id} – get a saved report (requires key)

DELETE /reports/{id} – delete (requires key)

(optional) GET /reports/export?fmt=json|csv – export (requires key)

Save semantics: add ?save=true on /weekly-report, /analyze, /chat to persist the output.
(You can require the key only when saving—see “Security Hardening” below.)

🧠 How It Works (ROMA inside this app)
```
flowchart LR
    A[User Request] --> B{Atomizer}
    B -- atomic --> E[Executor]
    B -- complex --> C[Planner]
    C --> E1[Ingest Agent]
    E1 --> E2[Metrics Agent]
    E2 --> E3[Coaching Agent]
    E3 --> E4[Reporting Agent]
    E & E1 & E2 & E3 & E4 --> F[Aggregator]
    F --> G[Response + (optional) Save to SQLite]

```
Atomizer: decides atomic vs. complex

Planner: orders subtasks (ingest → metrics → coach → report)

Executors: domain agents (Metrics/Coach may invoke GPT via OpenRouter)

Aggregator: merges outputs into the final response

If ROMA returns a low-value “echo/placeholder” or errors, Health Tracker falls back to local logic:

_fallback_weekly() – computes daily averages + short text summary

analyze_health_locally() – structured JSON (flags, score, recommendations)

🧪 Example Use Cases

Personal Health Assistant – weekly summaries & advice

Wellness App Backend – mobile/web clients call the endpoints

Multi-agent Reference – concrete example of ROMA orchestration

Fork & Repurpose – swap health agents for finance, study, productivity, etc.

🛠️ For Developers

Agents live in roma_agents/ (extend for new workflows)

Planner/Aggregator in roma_engine/ (customize pipelines)

Persistence via SQLite mounted at ./data

Guard sensitive endpoints with X-API-Key

Easy to wire to a Telegram bot or small web front-end

📦 Project Structure (core)
```
.
├── compose.yml                    # docker-compose (roma + health-tracker)
├── Dockerfile                     # health-tracker image
├── Dockerfile.roma                # ROMA image
├── main.py                        # FastAPI app (endpoints, fallbacks, DB)
├── roma_service.py                # ROMA Flask/ASGI service
├── roma_engine/                   # ROMA runner/orchestration
├── roma_agents/                   # Domain agents (ingest/metrics/coach/report)
├── requirements.txt
├── env.example                    # template for .env
├── data/                          # host-mounted DB folder (health.db)
└── static/                        # optional: reports.html admin page

```

🔐 Security & Persistence

API key protects /reports (and /health if enabled).

Optional hardening: require key for save actions on /weekly-report, /analyze, /chat.

.env is not committed; rotate keys periodically.

SQLite database persists at ./data/health.db (bind mount).

Hardening example (save-only lock) in main.py:

```

from fastapi import Header, HTTPException

@app.post("/weekly-report")
async def weekly_report(..., save: bool = False, x_api_key: str = Header(None, alias="X-API-Key")):
    if save and API_KEY and x_api_key != API_KEY:
        raise HTTPException(401, "Invalid or missing API key")
    ...
# Do the same for /analyze and /chat
```

