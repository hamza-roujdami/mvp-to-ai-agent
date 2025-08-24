# AI Agent Evolution Demo: From MVP to Production

This project demonstrates the journey from a simple MVP (Healthcare AI Assistant) to a production-ready AI agentic product using Microsoft Azure services.

## 🎯 Project Overview
The demo showcases two key phases:
1. **MVP Phase**: Simple Healthcare AI Assistant with RAG (Retrieval-Augmented Generation) system ✅ **COMPLETE**
2. **Production Phase**: Full AI agent with Azure AI Search, Content Safety, and observability 🚧 **NEXT**

## 🏗️ Repository Structure
```
h100-growthx-fy26/
├── mvp_rag/           # 🏥 MVP RAG System (Local AI Tools)
├── agentic_rag/       # 🚀 Production AI Agent (Azure Services)
├── README.MD          # 📖 Project documentation
├── show_script.md     # 🎭 Demo presentation script
├── .env               # 🔐 Environment variables (create from env.example)
└── env.example        # 📋 Environment variables template
```

## 🏥 MVP RAG Healthcare AI Assistant (COMPLETE)
**What it shows:**
- Real RAG system with local AI tools (Ollama + Qdrant)
- Semantic search with embeddings
- Dynamic LLM responses
- Performance metrics and monitoring

**What it demonstrates:**
- The starting point for AI agents
- Local development and testing capabilities
- Basic RAG pattern that can be enhanced

**Current capabilities:**
- Answer health questions from vector database
- Semantic understanding and retrieval
- Beautiful Gradio web interface
- Real-time performance metrics

**Tech Stack:**
- **LLM**: Ollama (phi4-mini)
- **Embeddings**: Ollama (bge-m3)
- **Vector DB**: Qdrant (Docker)
- **UI**: Gradio
- **Framework**: LangChain

## 🚀 Production AI Agent (NEXT)
**What it will show:**
- Full Azure-based AI agentic system
- Multi-agent collaboration
- Enterprise-grade security and compliance
- Scalable cloud architecture

**What it will demonstrate:**
- Evolution from local tools to Azure services
- Advanced agentic workflows
- Enterprise observability and monitoring

**Tech Stack (Planned):**
- **LLM**: Azure OpenAI
- **Vector Search**: Azure AI Search
- **Orchestration**: Azure Agent Service
- **Safety**: Azure Content Safety
- **Monitoring**: Azure Monitor

## 🚀 Quick Start

### 1. MVP RAG Demo
```bash
# Navigate to MVP folder
cd mvp_rag

# Install dependencies
pip install -r requirements.txt

# Ingest sample data
python data/ingest_data.py

# Launch beautiful Gradio UI
python gradio_app.py

# Or run CLI demo
python main.py
```

### 2. Production Agent (Coming Soon)
```bash
# Navigate to production folder
cd agentic_rag

# Setup Azure services
# (Implementation coming soon)
```

## 📊 Demo Scenarios

### MVP Demo (Current)
1. **Data Ingestion**: Load healthcare documents into vector database
2. **RAG Query**: Ask health questions and see semantic retrieval
3. **Performance Metrics**: Monitor response times and accuracy
4. **Beautiful UI**: Interactive Gradio web interface

### Production Demo (Future)
1. **Multi-Agent Workflow**: Collaborative AI agents
2. **Tool Calling**: AI agents using external tools
3. **Enterprise Security**: Compliance and safety monitoring
4. **Scalability**: Cloud-based deployment

## 🎯 Key Metrics

### MVP Metrics
- Response time
- Documents retrieved
- Similarity scores
- LLM generation time

### Production Metrics
- Agent success rate
- Tool execution accuracy
- Compliance scores
- System scalability metrics

## 🔄 Evolution Path

### Phase 1: MVP RAG ✅
- [x] Local AI tools (Ollama + Qdrant)
- [x] Basic RAG workflow
- [x] Healthcare knowledge base
- [x] Performance monitoring
- [x] Beautiful Gradio UI

### Phase 2: Production Agent 🚧
- [ ] Azure OpenAI integration
- [ ] Azure AI Search
- [ ] Azure Agent Service
- [ ] Content Safety
- [ ] Enterprise monitoring
- [ ] Multi-agent workflows

## 🛠️ Development

### Prerequisites
- Python 3.9+
- Docker (for Qdrant)
- Ollama (for local LLM)
- Azure subscription (for production)

### Local Setup
```bash
# Clone repository
git clone <repo-url>
cd h100-growthx-fy26

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd mvp_rag
pip install -r requirements.txt
```

## 📚 Resources
- [Gradio Documentation](https://www.gradio.app/)
- [Ollama Documentation](https://ollama.ai/)
- [Qdrant Documentation](https://qdrant.tech/)
- [Azure AI Services](https://azure.microsoft.com/en-us/products/ai-services)

## 🤝 Contributing
This is a demo project showcasing AI agent evolution. Feel free to explore and learn from the implementation!

## 📄 License
This project is for educational and demonstration purposes.
