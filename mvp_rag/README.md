# MVP RAG (Local)

Minimal Retrieval‑Augmented Generation demo using local tools.

## Stack
- LLM: qwen3:4b-instruct (Ollama)
- Embeddings: nomic-embed-text (Ollama)
- Vector DB: Qdrant (Docker)
- UI: Gradio (streaming)
- Retrieval: top_k=3, score_threshold≈0.38
- Answers: concise (3–5 sentences) + one actionable step + citations

## Prereqs
- Docker Desktop running
- Ollama running (`ollama serve`) and models pulled:
```
ollama pull qwen3:4b-instruct
ollama pull nomic-embed-text
```

## Run
```
# activate venv
source ../venv/bin/activate

# start qdrant (first time)
docker rm -f qdrant 2>/dev/null || true
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant

# ingest sample docs
python data/ingest.py

# launch UI
python app.py
```

Open http://localhost:7860

## Files
- core/llm_client.py — Ollama client
- core/vector_store.py — Qdrant client (auto-adjusts vector size)
- core/rag_engine.py — RAG orchestration
- data/ingest.py — sample healthcare docs
- app.py — Gradio UI (streaming + citations)
- requirements.txt — Python deps

## Flow
```mermaid
flowchart TD
    U[User Question] --> UI[Gradio UI]
    UI --> EMB[Ollama Embeddings\n(nomic-embed-text)]
    EMB -->|vector| VS[(Qdrant\nhealthcare_docs)]
    VS -->|top_k=3, score>=0.38| CTX[Retrieved Context]
    CTX --> LLM[Ollama LLM\n(qwen3:4b-instruct)]
    UI -->|controls| LLM
    LLM --> RESP[Streaming Response]
    CTX --> CITES[Citations]
    RESP --> UI
    CITES --> UI
```

Legend:
- Embeddings: nomic-embed-text (fast)
- Vector DB: Qdrant (Docker)
- LLM: qwen3:4b-instruct
- Retrieval: top 3 docs, cosine threshold ~0.38
- UI: streams response and shows citations
