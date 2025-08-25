# MVP to AI Agent

This repo shows the journey from a local MVP RAG to a production agentic system.

## Structure
```
.
├─ mvp_rag/        # Local MVP RAG (Ollama + Qdrant + Gradio)
├─ agentic_rag/    # Placeholder for the production agent (Azure)
├─ README.MD       # This file
├─ show_script.md  # Presentation notes
└─ venv/           # Python virtual environment (ignored by git)
```

## MVP RAG (ready to demo)
- LLM: qwen3:4b-instruct (Ollama)
- Embeddings: nomic-embed-text (Ollama)
- Vector DB: Qdrant (Docker)
- UI: Gradio (streaming responses)
- Retrieval: top_k=3, score_threshold≈0.38
- Answers: concise (3–5 sentences) + one actionable step + citations

### Prerequisites
- Docker Desktop running (for Qdrant)
- Ollama running (`ollama serve`) and models pulled:
```
ollama pull qwen3:4b-instruct
ollama pull nomic-embed-text
```

### Run (macOS/Linux)
```
# activate env
source venv/bin/activate

# start qdrant (first time)
docker rm -f qdrant 2>/dev/null || true
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant

# ingest and launch
/Users/hamza/projects/h100-growthx-fy26/venv/bin/python mvp_rag/data/ingest.py
/Users/hamza/projects/h100-growthx-fy26/venv/bin/python mvp_rag/app.py
```

### Run (PowerShell)
```
docker rm -f qdrant 2>$null; docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
& /Users/hamza/projects/h100-growthx-fy26/venv/bin/python /Users/hamza/projects/h100-growthx-fy26/mvp_rag/data/ingest.py
& /Users/hamza/projects/h100-growthx-fy26/venv/bin/python /Users/hamza/projects/h100-growthx-fy26/mvp_rag/app.py
```

Open http://localhost:7860 and try:
- "What are the symptoms of diabetes?"
- "How do I check my blood pressure at home?"

## Data
Sample healthcare snippets are defined inline in `mvp_rag/data/ingest.py` and stored in Qdrant as vectors + payload.

## Next (agentic_rag)
The production folder will add Azure OpenAI, Azure AI Search, Content Safety, and agentic workflows.
