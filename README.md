Sentient ROMA Health Tracker

An open-source multi-agent health intelligence system built on the ROMA pattern (Atomizer → Planner → Executors → Aggregator).

This isn’t just a script — it’s a working demonstration of how multi-agent orchestration + LLMs can power real-world applications.

🚩 Why This Matters

Shows how to operationalize multi-agent systems (not just theory).

Demonstrates health intelligence as a practical use case.

Provides a template: swap in new agents for finance, education, productivity, or research.

Fully packaged: FastAPI + SQLite + Docker → easy to run anywhere.

⚙️ What’s Inside

ROMA Framework

Atomizer → decide if a task is simple or complex.

Planner → build a sequence of subtasks.

Executors (Agents):

DataIngestionAgent → validate inputs.

MetricsAnalysisAgent → calculate scores, ask LLM for insights.

CoachingAgent → personalized GPT-based advice.

ReportingAgent → generate structured weekly reports.

Aggregator → merge results and respond.

FastAPI service with endpoints:
/analyze, /weekly-report, /chat, /reports, /health, /roma-info

Persistence → SQLite storage for reports.

Security → API key protection for sensitive endpoints.

Deployment → Docker Compose for one-command setup.

🔮 Use Cases

Personal Health Assistant
Weekly summaries, coaching tips, progress tracking.

Wellness App Backend
Plug wearable or mobile app data into the API.

Research & Experimentation
A sandbox for exploring multi-agent orchestration with GPT.

Community Forks
Adapt ROMA for finance, productivity, study coaches, or team analytics.


Getting Started for Beginners
What you need first

Git installed

Docker Desktop installed and running

Optional alternative without Docker: Python 3.11+, pip, and venv

If you’re on Windows, use PowerShell for the commands below.

1) Clone the repo

Linux/macOS:

cd ~
git clone https://github.com/chiefmmorgs/Sentient-health-tracker-.git
cd Sentient-health-tracker-
ls


Windows PowerShell:

cd $HOME
git clone https://github.com/chiefmmorgs/Sentient-health-tracker-.git
cd Sentient-health-tracker-
dir


You should see files like: docker/, requirements.txt, sentient_roma_api.py, roma_engine/, roma_agents/, storage/.

2) Create your .env file

This app reads secrets from a .env file in the project root.

Create .env with these keys:

# LLM provider key (MV key)
OPENROUTER_API_KEY=sk-your-openrouter-key

# Model to use
DEFAULT_MODEL=gpt-3.5-turbo

# App API key for protected endpoints
API_KEY=your-secret-key

# Database path inside the container
DB_PATH=/app/data/db.sqlite


Notes

OPENROUTER_API_KEY is your “MV key.” Create one in your OpenRouter account and paste it here.

Choose a strong random value for API_KEY. You will send this in the X-API-Key header for protected routes.

.env is already in .gitignore. Do not commit it.

3) Start the API with Docker

Make sure Docker Desktop is running.

Linux/macOS/Windows:

docker compose up -d --build


If your Docker uses the old syntax:

docker-compose up -d --build


Check logs:

docker compose logs -f


You should see Uvicorn running on http://0.0.0.0:8000

Stop later:

docker compose down

4) Open the API docs

Open this in your browser:

http://127.0.0.1:8000/docs


You will see all endpoints with try-it-out buttons.

5) Quick tests from the terminal

Health check (protected)

Replace your-secret-key with the value you put in .env.

Linux/macOS:

curl -H "X-API-Key: your-secret-key" http://127.0.0.1:8000/health


Windows PowerShell:

curl -Headers @{'X-API-Key'='your-secret-key'} http://127.0.0.1:8000/health


Weekly report (runs the full ROMA pipeline)
Linux/macOS:

curl -X POST http://127.0.0.1:8000/weekly-report \
  -H "Content-Type: application/json" \
  -d '{"data":{"steps":72000,"sleep_hours":49,"workouts":4,"water_liters":14}}'


Windows PowerShell:

$body = @{ data = @{ steps = 72000; sleep_hours = 49; workouts = 4; water_liters = 14 } } | ConvertTo-Json
curl -Method Post -Uri http://127.0.0.1:8000/weekly-report -ContentType "application/json" -Body $body


OpenAPI docs try-it-out tips

/health and /reports endpoints need the X-API-Key header. In the docs UI, click Authorize or add the header in each request.

6) Using Postman (optional)

Create a new request to GET http://127.0.0.1:8000/health

Add header:

Key: X-API-Key

Value: your-secret-key

Send. You should get a JSON status.

7) Update to the latest version
cd Sentient-health-tracker-
git pull origin main
docker compose up -d --build

8) Run without Docker (optional)

Use this if you prefer Python locally.

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# keep your .env in the project root
# start the API
uvicorn sentient_roma_api:app --reload --host 127.0.0.1 --port 8000


Windows PowerShell:

python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

uvicorn sentient_roma_api:app --reload --host 127.0.0.1 --port 8000


Then open:

http://127.0.0.1:8000/docs

9) Common errors and fixes

401 Unauthorized on /health or /reports
Add header X-API-Key with the same value as API_KEY in .env.

500 error about missing OPENROUTER_API_KEY
Add OPENROUTER_API_KEY to .env. Restart Docker:

docker compose down && docker compose up -d --build


Port 8000 already in use
Stop the app using the port or change the port:

docker compose down
# edit docker-compose.yml to map a different host port, e.g. "8080:8000"
docker compose up -d --build
# then open http://127.0.0.1:8080/docs


.env not loaded in Docker
Ensure .env is in the project root (same folder as docker-compose.yml). Rebuild:

docker compose up -d --build


Database not persisting
Make sure the data/ folder exists and is mounted by Compose. DB_PATH should be /app/data/db.sqlite.

10) What to do next

Explore endpoints in /docs

Try /analyze and /chat for quick insights and coaching

Check /reports to see saved weekly reports

Secure deployment with HTTPS and a reverse proxy if you expose it on the internet

11) Quick checklist before sharing with others

README explains setup and usage

.env.example added with placeholder keys

MIT license present

Docker works on a fresh machine


