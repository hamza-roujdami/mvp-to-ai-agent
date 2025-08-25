# MVP RAG (Local)

Minimal Retrieval-Augmented Generation demo using local tools.

## Stack
- LLM: qwen3:4b-instruct (Ollama)
- Embeddings: bge-m3 (Ollama)
- Vector DB: Qdrant (Docker)
- UI: Gradio

## Prereqs
- Docker Desktop running (for Qdrant)
- Ollama running (`ollama serve`) with models pulled:
```bash
ollama pull qwen3:4b-instruct
ollama pull bge-m3
```

## Run
```bash
# activate venv
source ../venv/bin/activate

# start qdrant (first time)
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant

# ingest sample docs
python data/ingest.py

# launch UI
python gradio_app.py
```

Open http://localhost:7860 and ask:
- What are the symptoms of diabetes?
- How do I check my blood pressure at home?

## Files
- core/llm_client.py — Ollama client
- core/vector_store.py — Qdrant client
- core/rag_engine.py — RAG orchestration
- data/ingest_data.py — loads sample docs
- gradio_app.py — web UI
- requirements.txt — Python deps
