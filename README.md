# RecallOps 🧠🚨

**RecallOps** is an intelligent, self-learning incident management platform that helps Site Reliability Engineers (SREs) and DevOps teams dramatically reduce Mean Time to Resolution (MTTR). By capturing chaotic post-mortem notes, structuring them with LLMs, and indexing them semantically, RecallOps acts as a persistent memory bank that tells you exactly how similar alerts were resolved in the past.

---

## ⚡ Key Features

1. **Remember (Log Incident)**: Paste messy logs, raw Slack conversations, or unstructured notes. An LLM (powered by Groq) extracts structured JSON keys (Symptom, Root Cause, Service Affected, Fix Applied, Resolution Time), and indexes them into **Hindsight Cloud** (semantic memory).
2. **Recall (Triage Alert)**: Paste a new incoming alert. RecallOps semantically searches historical incidents (using Hindsight) and utilizes an LLM to generate an actionable, step-by-step **Triage Brief** outlining the most likely cause and immediate resolution steps.
3. **Memory Bank**: A dynamic dashboard to inspect, filter, and review the collective knowledge stored in the vector-embedded memory bank.

---

## 🏗️ Architecture & Data Flow

### 1. Ingestion (Intake Flow)
```
[User Text Input] -> [Groq API (JSON extraction)] -> [Hindsight Cloud API (Vector/Graph index)]
```

### 2. Resolution (Triage Flow)
```
[Incoming Alert] -> [Hindsight Semantic Search] -> [Groq API Context Integration] -> [Actionable Triage Brief]
```

---

## 🛠️ Tech Stack

*   **Frontend**: Streamlit (Python-based Web UI)
*   **LLM Engine**: Groq API (`llama3-8b-8192`)
*   **Semantic Memory Layer**: Hindsight Cloud (Vector, Graph, Keyword & Temporal Search)
*   **Programming Language**: Python 3.10+
*   **Deployment**: Local Dev Server (`localhost:8501`)

---

## ⚙️ Setup and Installation

### 1. Install Dependencies
Run the following command to install required libraries:
```bash
pip install streamlit groq requests python-dotenv
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and input your credentials:
```env
GROQ_API_KEY=your_groq_api_key_here
HINDSIGHT_API_KEY=your_hindsight_api_key_here
HINDSIGHT_PIPELINE_ID=your_hindsight_pipeline_id_here
```

*   **Groq API Key**: Obtain from [groq.com](https://console.groq.com).
*   **Hindsight API Key & Pipeline ID**: Obtain from [hindsight.vectorize.io](https://hindsight.vectorize.io).

### 3. Run the Application
Start the Streamlit development server:
```bash
streamlit run app.py
```

The web interface will open automatically in your browser at `http://localhost:8501`.

---

## 💡 Quick Start Guide
1. Navigate to the **Log Incident** page and click **Load 20 Mock Incidents** to populate the memory bank with realistic, pre-configured incident records.
2. Go to the **Memory Bank** page to verify the records are successfully stored.
3. Open the **Triage Alert** page, paste an alert like `"ALERT: auth-service CPU usage exceeded 90%, connection pool exhausted"`, and click **Analyze & Resolve** to get your triage brief.
