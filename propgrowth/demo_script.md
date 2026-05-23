# 🎙️ PropGrowth AI — 5-Minute Hackathon Demo Script

This guide provides a structured, step-by-step walkthrough to demonstrate the core value, architecture, and observability features of PropGrowth AI to hackathon judges and stakeholders.

---

## ⏱️ Timeline Allocation

| Section | Duration | Key Focus |
| :--- | :--- | :--- |
| **1. Hook & Problem Statement** | 0:30 | Indian Real Estate analysis is complex and lacks transparency. |
| **2. LangGraph State Machine & Orchestration** | 1:15 | Asynchronous 6-node flow, memory checkpointing, and execution state. |
| **3. ChromaDB Grounding** | 1:00 | RAG-driven validation against local zoning and development master plans. |
| **4. Human-in-the-Loop (HITL) Flow** | 1:15 | Analyst review boundary, manual adjustments, and state resumption. |
| **5. Arize Phoenix Observability** | 1:00 | OpenTelemetry traces, latency analysis, and LLM prompt/response inspection. |

---

## 🎭 Step-by-Step Walkthrough

### 1. Hook & Introduction (30 seconds)
- **Visuals**: Show the **PropGrowth AI Dark Luxury Terminal** in the browser.
- **Narrative**:
  > "Hello judges! Today, real estate investment calculations in India's rapid commercial hubs are done using scattered spreadsheets, guesswork, and outdated brochures. We present PropGrowth AI—a dark luxury investment terminal that uses state-of-the-art AI orchestration and grounded planning documentation to deliver risk-aware investment reports."

---

### 2. LangGraph Orchestration & Seeding (1 minute 15 seconds)
- **Visuals**: Point to the text input screen. Type in:
  - **Address/Locality**: `Hinjewadi Phase 1`
  - **City**: `Pune`
  - **Budget**: `₹120 Lakhs`
  - **Bhk Type**: `3BHK`
  - **Horizon**: `7 Years`
- **Action**: Click the **Start Analysis** button. Notice the typewriter log updates stream in:
  - 🏘️ *Fetching comparable properties...*
  - 📋 *Retrieving zoning laws and infrastructure master plans...*
  - ⚙ *Calculating preliminary growth score...*
- **Narrative**:
  > "Behind the scenes, we've built a 6-node StateGraph using LangGraph. When we click submit, it initiates the `fetch_market_data` node, pulling dynamic listings and deterministically resolving locality ratings based on our custom datasets. It manages this asynchronously using memory checkpointers, keeping the execution trace preserved in a secure, resumeable thread state."

---

### 3. ChromaDB Grounding (1 minute)
- **Visuals**: Show the preliminary scores and locality insights. Point out the grounding text box containing regulatory warnings.
- **Narrative**:
  > "Rather than letting a generative model hallucinate pricing trends, we ground our score. We queried a vectorized ChromaDB database containing localized urban planning records. Because our query found development details on the Hinjewadi Metro line and Rajiv Gandhi Infotech Park, the agent automatically injected this context and awarded a +5 bonus to the property's preliminary score."

---

### 4. Human-in-the-Loop (HITL) Analyst Review (1 minute 15 seconds)
- **Visuals**: Highlight the **Analyst Verification Screen**.
  - Check the boxes to approve 3 of the 4 comparable properties.
  - In the Analyst Notes box, write:
    > "Strong micro-market demand, metro line 3 work is highly bullish for appreciation."
  - Click **Approve & Resume**.
- **Action**: Watch the typewriter terminal stream logs:
  - ✅ *Analyst review received...*
  - 📊 *Calculating final weighted investment score...*
  - 📝 *Generating investment analysis report...*
- **Narrative**:
  > "Here is our core innovation: the Human-in-the-Loop (HITL) interrupt. Before the AI generates a final recommendation, it pauses execution and waits for human sign-off. We can filter the comparable listings and write feedback. Notice that when we write 'bullish', our backend mathematical engine detects it, adjusts the score upwards, resumes the graph execution, and invokes the Gemini API to compile the final JSON report."

---

### 5. Arize Phoenix & OpenTelemetry Walkthrough (1 minute)
- **Visuals**: Expand the **SYSTEM TELEMETRY** drawer at the bottom right. Show the latencies and execution logs. Then, transition to the Arize Phoenix Dashboard (running at `http://localhost:6006`).
- **Narrative**:
  > "Observability is a first-class citizen in PropGrowth AI. In our System Telemetry drawer, we see exact latency times for each tool and RAG call. In the Arize Phoenix dashboard, we see a complete tracing log. We can zoom into the LangGraph spans, verify token counts for the Gemini-1.5-Flash call, inspect the prompt templates, and analyze exact call execution graphs. This guarantees our system is production-ready, highly debuggable, and completely transparent. Thank you!"
