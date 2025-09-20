# 🤖 Sentient ROMA Health Tracker

**Advanced AI-powered health analysis using the Sentient AGI ROMA framework.**  
This project demonstrates a practical multi-agent system for health tracking using the ROMA pattern:

**Atomizer → Planner → Executors (Ingest / Metrics / Coach / Report) → Aggregator**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688)](#)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](#)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

- **ROMA framework** for recursive task decomposition.
- **Agents**
  - **DataIngestionAgent** – validates and normalizes inputs.
  - **MetricsAnalysisAgent** – computes basic scores (activity, sleep, hydration) and asks an LLM for insights.
  - **CoachingAgent** – personalized tips via GPT (OpenRouter).
  - **ReportingAgent** – structured weekly summary, saved to SQLite.
- **FastAPI service** with clean REST endpoints.
- **SQLite persistence** for saved reports.
- **API key guard** for `/health` and `/reports`.
- **Dockerized** with Compose for one-command deploy.

---

## 🚀 Quick Start

### 1) Clone
```bash
git clone https://github.com/chiefmmorgs/Sentient-health-tracker-.git
cd Sentient-health-tracker-

2) Environment

Create .env in the project root:

OPENROUTER_API_KEY=sk-your-openrouter-key
DEFAULT_MODEL=gpt-3.5-turbo
API_KEY=your-secret-key
DB_PATH=/app/data/db.sqlite


Keep .env private (it’s already in .gitignore).
