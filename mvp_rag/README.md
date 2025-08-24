# MVP RAG Healthcare AI Assistant

A production-ready RAG (Retrieval-Augmented Generation) system built with local AI tools, demonstrating the journey from MVP to enterprise Azure services.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   Embeddings    │───▶│   Vector DB     │
│                 │    │   (bge-m3)      │    │   (Qdrant)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LLM Response  │◀───│   Context       │◀───│   Similarity    │
│   (phi4-mini)   │    │   Retrieval     │    │   Search        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Tech Stack

### **Local AI Tools:**
- **LLM**: Ollama (phi4-mini for responses)
- **Embeddings**: Ollama (bge-m3 for vector embeddings)
- **Vector DB**: Qdrant (local Docker container)
- **Framework**: LangChain (RAG orchestration)

### **Production Evolution Path:**
- **LLM**: Ollama → Azure OpenAI (GPT-4)
- **Embeddings**: bge-m3 → Azure OpenAI (text-embedding-ada-002)
- **Vector DB**: Qdrant → Azure AI Search
- **Safety**: Basic → Azure Content Safety

## 📁 Project Structure

```
mvp_rag/
├── README.md                 # This file
├── requirements.txt          # Dependencies
├── config.py                 # Configuration
├── main.py                   # Main demo script
├── core/                     # Core RAG components
│   ├── __init__.py
│   ├── rag_engine.py         # Main RAG orchestration
│   ├── llm_client.py         # Ollama LLM client
│   └── vector_store.py       # Qdrant vector operations
├── data/                     # Healthcare data
│   ├── documents/            # Source documents
│   ├── embeddings/           # Pre-computed embeddings
│   └── knowledge_base.py     # Data management
├── embeddings/               # Embedding utilities
│   ├── __init__.py
│   ├── embedder.py           # Text embedding logic
│   └── chunker.py            # Document chunking
├── models/                   # Data models
│   ├── __init__.py
│   ├── document.py           # Document structure
│   └── response.py           # Response models
└── utils/                    # Utilities
    ├── __init__.py
    ├── logger.py             # Logging
    └── metrics.py            # Performance metrics
```

## 🔄 RAG Flow

### **1. Document Ingestion**
```
Healthcare Documents → Chunking → Embedding → Storage in Qdrant
```

### **2. Query Processing**
```
User Query → Embed Query → Vector Search → Retrieve Top-K → LLM Generation
```

### **3. Response Generation**
```
Context + Query → LLM Prompt → Generated Response → Safety Check → Final Answer
```

## 🎯 Key Features

### **Current MVP:**
- ✅ Real RAG with local AI tools
- ✅ Semantic search with embeddings
- ✅ Dynamic LLM responses
- ✅ Healthcare knowledge base
- ✅ Performance metrics

### **Production Ready:**
- ✅ Clean architecture
- ✅ Modular design
- ✅ Easy Azure migration path
- ✅ Comprehensive logging
- ✅ Error handling

## 🚀 Quick Start

### **1. Prerequisites**
```bash
# Start Qdrant
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant

# Start Ollama
ollama serve

# Install models
ollama pull phi4-mini
ollama pull bge-m3
```

### **2. Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the MVP
python main.py
```

## 📊 Performance Metrics

- **Query Response Time**: End-to-end latency
- **Vector Search Quality**: Relevance scores
- **LLM Generation Time**: Response generation latency
- **Memory Usage**: Resource consumption
- **Accuracy**: Response quality assessment

## 🔮 Evolution Path

### **Week 1**: ✅ Local RAG MVP
- Ollama + Qdrant working
- Healthcare knowledge base
- Real RAG responses

### **Week 2**: 🚧 Azure Integration
- Azure OpenAI for LLM
- Azure AI Search for vectors
- Content Safety integration

### **Week 3**: 🚧 Production Features
- Agentic workflow
- Tool calling
- Observability

## 🎭 Demo Scenarios

1. **Basic Health Q&A**: "What are diabetes symptoms?"
2. **Complex Queries**: "How do I manage stress with exercise?"
3. **Context Retrieval**: Show retrieved documents
4. **Performance Metrics**: Response times, search quality
5. **Limitations**: What local tools can't do
6. **Azure Benefits**: What production brings

## 🤝 Contributing

This MVP demonstrates local AI capabilities and provides a clear path to production Azure services.
