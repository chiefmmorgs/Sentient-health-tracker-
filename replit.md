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
- **NEW:** Created modern React + TypeScript frontend with complete project structure
- Frontend includes routing, state management, API clients, and responsive UI components
- Configured for development on port 3000 with proper Replit environment support

## Project Architecture
- **FastAPI Application** (`main.py`): Main REST API running on port 5000
- **ROMA Service** (`roma_service.py`): Meta-agent framework running on port 3001
- **React Frontend** (`frontend/`): Modern TypeScript UI running on port 3000
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

## Frontend Architecture (New)
- **Technology Stack**: React 18+ with TypeScript, Vite, Tailwind CSS
- **State Management**: Zustand stores for app, ROMA, and health data
- **Data Fetching**: React Query with Axios interceptors
- **Routing**: React Router with Landing, ROMA Dashboard, Health Dashboard, System Hub
- **Design**: Responsive layout with dark/light theme support
- **API Integration**: Configured clients for both ROMA and Health APIs

## Development Status
- **Backend**: Fully functional REST API with all endpoints working
- **Frontend**: Project structure and UI components completed, needs API integration
- **Next Steps**: Wire frontend components to actual API calls and add real-time features

## User Preferences
- Full-stack application with both REST API and modern web interface
- Secure API endpoints with key-based authentication
- Uses fallback logic when ROMA service is unavailable
- Development-ready with proper port configuration (frontend: 3000, backend: 5000)