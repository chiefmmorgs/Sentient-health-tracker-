# AI-Powered Multi-Agent Platform Frontend

A modern React + TypeScript frontend for AI systems featuring ROMA Meta-Agent Framework and Sentient Health Tracker.

## 🚀 Tech Stack

- **React 18+** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Zustand** for state management
- **React Query** for data fetching
- **React Router** for navigation
- **Recharts** for data visualization
- **Socket.io** for real-time updates
- **Axios** for HTTP requests
- **Lucide React** for icons

## 🛠️ Setup Instructions

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

## 📖 API Integration

### Primary System: ROMA Meta-Agent Framework
- **Base URL:** `http://localhost:5000`
- **Architecture:** Atomizer → Planner → Executors → Aggregator
- **Agents:** General, Research, Financial
- **Endpoint:** `POST /execute` with `{ agent, task, streaming, options }`

### Secondary System: Sentient Health Tracker
- **Base URL:** `http://localhost:5000`
- **Endpoints:**
  - `GET /health` (requires X-API-Key)
  - `POST /analyze` - Quick health analysis
  - `POST /weekly-report` - Generate weekly reports
  - `POST /chat` - AI coaching chat
  - `GET /reports` - Report management

## 🎯 Features

### ROMA Dashboard (`/roma`)
- Agent selection (General, Research, Financial)
- Task input with complexity slider
- Recursive task breakdown visualization
- Parallel execution timeline
- Results aggregation display
- Agent execution history

### Health Dashboard (`/health`)
- Quick health metrics form
- Weekly report generator
- AI coaching chat interface
- Reports gallery with filtering
- Health trends visualization
- Real-time analysis feedback

### System Hub (`/dashboard`)
- Multi-system status monitoring
- API performance metrics
- Service uptime tracking
- Real-time health checks
- System load monitoring

## 🔧 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🌐 Ports

- **Frontend:** `http://localhost:3000`
- **Backend APIs:** `http://localhost:5000`
