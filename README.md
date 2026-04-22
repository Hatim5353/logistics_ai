# Autonomous Logistics Researcher Agent

An AI agent that researches logistics topics (freight rates, port congestion, supply-chain disruptions) using live web search, then stores reports in a local RAG knowledge base for instant offline querying.

---

## Quick Start

### 1. Prerequisites
- Python 3.10 or 3.11 (Python 3.12 works too)
- A **Google Gemini API key** → https://aistudio.google.com/apikey (free tier available)
- A **Serper.dev API key** → https://serper.dev (free tier available)

### 2. Clone / unzip the project
```bash
unzip Logistic_Researcher_agent.zip
cd Logistic_Researcher_agent-main
```

### 3. Create & activate a virtual environment
```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up your API keys
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

Your `.env` should look like:
```
GOOGLE_API_KEY=AIzaSy...your_actual_key...
SERPER_API_KEY=your_serper_key_here
```

### 6. Run the app
```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

---

## 🐳 Docker

### Option A — Docker Compose (recommended)
```bash
# 1. Make sure your .env file is ready with API keys
# 2. Build and run:
docker compose up --build
```
Open http://localhost:8501 — done! Your reports and vector DB are persisted via volume mounts.

To stop:
```bash
docker compose down
```

### Option B — Plain Docker
```bash
# Build the image
docker build -t logistics-ai .

# Run the container
docker run -d \
  --name logistics-ai \
  -p 8501:8501 \
  --env-file .env \
  -v ./knowledge_repo:/app/knowledge_repo \
  -v ./chroma_db:/app/chroma_db \
  logistics-ai
```

Open http://localhost:8501.

To stop:
```bash
docker stop logistics-ai && docker rm logistics-ai
```

### Docker Notes
- **API keys** are read from your `.env` file via `--env-file` (never baked into the image).
- **Reports & ChromaDB** are mounted as volumes so data persists across container restarts.
- The image uses a multi-stage build for a smaller footprint (~400 MB vs ~1.2 GB).

---

## How It Works

| Mode | What it does |
|------|-------------|
| **Live Research** | Sends your query to two AI agents (Analyst + Writer) who search the web and produce a Markdown report saved in `knowledge_repo/` |
| **Query Knowledge Base** | Answers your question instantly from previously saved reports using RAG (no web call, no API cost) |
| **Re-index** | Scans `knowledge_repo/` and re-embeds all `.md` files into ChromaDB |

---

## Project Structure

```
├── app.py                  # Streamlit UI (main entry point)
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # One-command Docker setup
├── requirements.txt
├── .env.example            # Copy to .env and fill in keys
├── knowledge_repo/         # Saved research reports (.md files)
├── chroma_db/              # Local vector store (auto-created)
└── src/
    ├── agents/
    │   └── logistics_crew.py   # CrewAI agents & crew setup
    └── rag/
        ├── indexer.py          # Embeds reports into ChromaDB
        └── retriever.py        # RAG query chain
```
