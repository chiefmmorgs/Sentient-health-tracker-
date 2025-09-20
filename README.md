Fixed README snippet for Quick Start
## 🚀 Quick Start

### 1) Clone
```bash
git clone https://github.com/chiefmmorgs/Sentient-health-tracker-.git
cd Sentient-health-tracker-

2) Environment

Create a .env in the project root:

OPENROUTER_API_KEY=sk-your-openrouter-key
DEFAULT_MODEL=gpt-3.5-turbo
API_KEY=your-secret-key
DB_PATH=/app/data/db.sqlite


Keep .env private (it’s already in .gitignore).

3) Run with Docker Compose
docker compose up -d --build

4) Test

Health (protected):

curl -H "X-API-Key: your-secret-key" http://127.0.0.1:8000/health


Weekly report:

curl -X POST http://127.0.0.1:8000/weekly-report \
  -H "Content-Type: application/json" \
  -d '{"data":{"steps":72000,"sleep_hours":49,"workouts":4,"water_liters":14}}'


---

### How to Update README

1. Open the file:
```bash
nano README.md


Replace the Quick Start section with the cleaned-up snippet above.

Save + exit (CTRL+O, Enter, then CTRL+X).

Commit and push:

git add README.md
git commit -m "docs: fix README formatting for Quick Start"
git push origin main
