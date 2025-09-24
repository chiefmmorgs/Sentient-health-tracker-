# Sentient ROMA Health Tracker

## Project Overview
This is an AI-powered health tracking application that uses the Sentient AGI ROMA framework. It provides REST API endpoints for health analysis, weekly reports, and coaching.

## Recent Changes (September 24, 2025)
- Successfully imported from GitHub and configured for Replit environment
- Modified application to run on port 5000 (main app) and port 3001 (ROMA service)
- Set up default environment values for demo purposes
- Created startup script to manage both services
- Configured workflow and deployment settings
- Tested all major endpoints successfully

## Project Architecture
- **FastAPI Application** (`main.py`): Main REST API running on port 5000
- **ROMA Service** (`roma_service.py`): Meta-agent framework running on port 3001
- **SQLite Database**: Persistent storage for health reports
- **Multi-agent System**: Includes DataIngestion, MetricsAnalysis, Coaching, and Reporting agents

## API Endpoints
- `GET /health` - Health check (requires API key)
- `POST /weekly-report` - Generate weekly health analysis
- `POST /analyze` - Quick metrics analysis
- `POST /chat` - AI coaching chat
- `GET /reports` - List saved reports (requires API key)
- `GET /docs` - Interactive API documentation

## Configuration
- Default API key: `demo-key-12345`
- Database: SQLite stored in `./data/health.db`
- ROMA service URL: `http://localhost:3001`

## Deployment
- Configured for autoscale deployment
- Uses `start_services.py` to manage both services
- Ready for production deployment via Replit's deployment feature

## User Preferences
- Backend-focused health tracking application
- No frontend UI needed - REST API only
- Uses fallback logic when ROMA service is unavailable
- Secure API endpoints with key-based authentication