# RecallOps 🧠🚨

**RecallOps** is an intelligent, self-learning incident management platform that helps Site Reliability Engineers (SREs) and DevOps teams dramatically reduce Mean Time to Resolution (MTTR). By capturing chaotic post-mortem notes, structuring them with LLMs, and indexing them semantically via [Hindsight agent memory](https://vectorize.io/what-is-agent-memory), RecallOps acts as a persistent memory bank that tells you exactly how similar alerts were resolved in the past.

🚀 **[Live Demo → recall-ops-72w3c49wtp4s882f6xoxb4.streamlit.app](https://recall-ops-72w3c49wtp4s882f6xoxb4.streamlit.app/)**

---

## ⚡ Key Features

1. **Remember (Log Incident)**: Paste messy logs, raw Slack conversations, or unstructured notes. An LLM (powered by Groq) extracts structured JSON keys (Symptom, Root Cause, Service Affected, Fix Applied, Resolution Time), and indexes them into **[Hindsight Cloud](https://hindsight.vectorize.io/)** (semantic memory).
2. **Recall (Triage Alert)**: Paste a new incoming alert. RecallOps semantically searches historical incidents using [Hindsight](https://github.com/vectorize-io/hindsight) and generates an actionable, step-by-step **Triage Brief** outlining the most likely cause and immediate resolution steps.
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

The key architectural decision: **structured extraction before retain.** Raw text is never dumped directly into memory. The LLM first converts messy notes into a clean schema (`symptom_pattern`, `root_cause`, `service_affected`, `fix_applied`, `time_to_resolve_minutes`) before storing. This makes semantic recall dramatically more precise — you're matching against structured signal, not prose.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Python-based Web UI) |
| LLM Engine | Groq API (`llama3-8b-8192`) |
| Semantic Memory | [Hindsight Cloud](https://hindsight.vectorize.io/) — Vector, Graph, Keyword & Temporal Search |
| Agent Memory Concept | [What is Agent Memory?](https://vectorize.io/what-is-agent-memory) |
| Language | Python 3.10+ |
| Deployment | Streamlit Cloud |

---

## ⚙️ Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/manya296/retrospect-ai.git
cd retrospect-ai
```

### 2. Install Dependencies

```bash
pip install streamlit groq requests python-dotenv
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
HINDSIGHT_API_KEY=your_hindsight_api_key_here
HINDSIGHT_PIPELINE_ID=your_hindsight_pipeline_id_here
```

- **Groq API Key**: Obtain from [console.groq.com](https://console.groq.com)
- **Hindsight API Key & Pipeline ID**: Obtain from [hindsight.vectorize.io](https://hindsight.vectorize.io)

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`. Or visit the live deployment at [recall-ops-72w3c49wtp4s882f6xoxb4.streamlit.app](https://recall-ops-72w3c49wtp4s882f6xoxb4.streamlit.app/).

---

## 💡 Quick Start Guide

1. Navigate to the **Log Incident** page and click **Load 20 Mock Incidents** to populate the memory bank with realistic pre-configured incident records.
2. Go to the **Memory Bank** page to verify the records are successfully stored.
3. Open the **Triage Alert** page, paste an alert like:
   > `ALERT: auth-service CPU usage exceeded 90%, connection pool exhausted`
   
   Click **Analyze & Resolve** to get your triage brief instantly.

---

## 🧠 Why Hindsight?

Most incident response tools treat every alert as a fresh problem. RecallOps is different because of [Hindsight](https://github.com/vectorize-io/hindsight) — an agent memory layer that persists structured knowledge across sessions. Without it, every on-call engineer starts from zero. With it, the system recalls that this exact Redis OOM pattern happened 6 weeks ago, who fixed it, and how long it took.

Read more about the concept of [agent memory](https://vectorize.io/what-is-agent-memory) that powers this approach.

---

## 🔗 Built With

- [Hindsight](https://github.com/vectorize-io/hindsight) — Agent memory by Vectorize
- [Hindsight Docs](https://hindsight.vectorize.io/) — Full documentation
- [What is Agent Memory?](https://vectorize.io/what-is-agent-memory) — The concept behind RecallOps
- [Groq](https://console.groq.com) — Ultra-fast LLM inference
- [Streamlit](https://streamlit.io) — Python web UI framework
