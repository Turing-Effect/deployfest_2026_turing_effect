# 🏢 PropGrowth AI — Observability & Real Estate Analytics Terminal

PropGrowth AI is a state-of-the-art dark luxury real estate investment analysis application designed for Indian tech micro-markets. It orchestrates multi-agent tasks, pulls zoning constraints via a vectorized retrieval-augmented generation (RAG) system, resolves human-in-the-loop (HITL) analyst approvals, and instruments rich OpenTelemetry tracing with Arize Phoenix.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: FastAPI, Uvicorn, Python 3.10+, ChromaDB (Vector Search), SentenceTransformers (`all-MiniLM-L6-v2`), Google Generative AI SDK (`gemini-1.5-flash`), LangGraph (State Orchestration with Memory Checkpointing).
- **Frontend**: React (Vite, HSL-tailored Dark Luxury glassmorphism layout, SVG radial rings, typewriter streaming logs).
- **Observability**: OpenTelemetry SDK, OpenInference LangChain instrumentation, Arize Phoenix tracing dashboard.

---

## 📋 Prerequisites

Make sure you have the following installed:
1. **Python 3.10+**
2. **Node.js 18+ & npm**
3. **C++ Build Tools** (needed for ChromaDB and other vector/embedding dependencies during python package installation)

---

## ⚙️ Environment Configuration

1. Copy the environment configuration template:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Open `backend/.env` and fill in your Gemini API key:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key
   PORT=8000
   ```

---

## 🚀 Installation & Startup

### 1. Run the Backend Core

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

Upon starting, the server will:
- Automatically seed ChromaDB with local zoning and master plans for micro-markets (Hinjewadi, Whitefield, Bandra, etc.) if it is empty.
- Launch the **Arize Phoenix Observability** session. Traces will begin streaming to the local Phoenix collector.
- Expose the API on [http://localhost:8000](http://localhost:8000).

### 2. Run the Frontend Luxury UI

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Start the Vite React development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to [http://localhost:5173](http://localhost:5173).

---

## 📈 Observability & Telemetry Walkthrough

At the bottom-right corner of the frontend dashboard, you will find a floating **SYSTEM TELEMETRY** drawer. 

When you run an analysis:
1. **Live Traces**: The drawer updates with live OTel traces mapping execution steps (e.g. `search_properties`, `calculate_roi`, `rag_search`, `gemini_inference`).
2. **Latency Tracking**: Observe exact microsecond/millisecond performance overheads.
3. **Arize Phoenix UI**: Open the URL printed in the backend logs (usually [http://localhost:6006](http://localhost:6006)) to view the full OpenTelemetry trace visualization DAG, explore span details, inspect prompts, and evaluate model performance.

---

## 🎯 Demo Guide

For a structured walkthrough to show hackathon judges or stakeholders, refer to the [demo_script.md](demo_script.md) file. It includes sample inputs, verification commands, and key architectural highlights.
