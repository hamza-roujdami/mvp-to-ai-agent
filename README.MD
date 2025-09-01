# 🚀 MVP to Production Agentic RAG System

This repository demonstrates the evolution from a **local MVP RAG system** to a **production-ready agentic RAG system** using Azure AI Foundry services.

## 🏗️ Project Overview

We're building **two complementary systems** to showcase AI evolution:

### 1. 🏥 **MVP RAG Healthcare AI Assistant**
**Location**: `mvp_rag/`  

**What it demonstrates:**
- **Local AI Stack**: Ollama + Qdrant + Gradio
- **Healthcare Domain**: Specialized medical AI assistant
- **Production Patterns**: Proper architecture, error handling, monitoring
- **Cost-Effective Development**: Local models for rapid prototyping

**Key Features:**
- 🔍 **Smart Retrieval**: Semantic search with similarity thresholds
- 🤖 **AI Responses**: Medical disclaimers and professional guidance
- 📊 **Performance Metrics**: Real-time timing and analytics
- 🎯 **Example Queries**: 6 pre-built healthcare test cases
- 📚 **Citations**: Proper source attribution for medical information

**Tech Stack:**
- **LLM**: qwen3:4b-instruct (Ollama)
- **Embeddings**: nomic-embed-text (Ollama)
- **Vector DB**: Qdrant (Docker)
- **UI**: Gradio (streaming responses)
- **Domain**: Healthcare with medical safety guidelines

### 2. 🤖 **Healthcare Agentic RAG System**
**Location**: `agentic_rag/`  

**What it demonstrates:**
- **Enterprise AI Stack**: Azure AI Foundry + Azure AI Agent Service
- **Multi-Agent Architecture**: Coordinator, Research, Analysis, and Synthesis agents
- **Azure AI Search Integration**: Enterprise-grade knowledge retrieval
- **Production Scalability**: Auto-scaling, security, observability
- **Complete Workflow**: End-to-end multi-agent healthcare information pipeline

**Key Features:**
- 🎯 **Multi-Agent Orchestration**: Intelligent workflow coordination
- 🔍 **Research Agent**: Azure AI Search for healthcare document retrieval
- 📊 **Analysis Agent**: Code Interpreter for data analysis and visualization
- 📝 **Synthesis Agent**: Patient-friendly healthcare response generation
- 🚀 **Complete Pipeline**: Research → Analysis → Synthesis workflow
- 🧪 **Testing Framework**: CLI and Gradio UI testing capabilities

**Tech Stack:**
- **Azure AI Foundry**: Agent Service and Model Catalog
- **Azure AI Agent Service**: Multi-agent orchestration
- **Azure AI Search**: Enterprise vector search and knowledge retrieval
- **Code Interpreter**: Data analysis and visualization tools
- **Gradio UI**: Beautiful web interface for end users
- **Domain**: Healthcare with comprehensive medical information

## 🎯 **Demonstration Goals**

### **MVP RAG**
- **Local Development**: Cost-effective AI prototyping
- **Domain Expertise**: Healthcare-specific AI assistant
- **Production Patterns**: Proper architecture and monitoring
- **Easy Deployment**: Docker + local models

### **Healthcare Agentic RAG**
- **Enterprise Scale**: Azure AI Foundry services
- **Multi-Agent Intelligence**: Coordinated AI workflows
- **Tool Integration**: Azure AI Search and Code Interpreter
- **Production Security**: Enterprise-grade security
- **Complete Workflow**: End-to-end healthcare information pipeline

## 📁 **Repository Structure**

```
h100-growthx-fy26/
├── mvp_rag/                    # Local MVP RAG
│   ├── core/                   # RAG engine components
│   ├── data/                   # Healthcare documents
│   ├── app.py                  # Gradio web interface
│   └── README.md              # Complete setup guide
├── agentic_rag/                # Azure AI Foundry
│   ├── agents/                 # Multi-agent system
│   ├── tests/                  # Testing framework
│   ├── app.py                  # Gradio web interface
│   ├── test_complete_workflow.py # End-to-end workflow test
│   └── README.md              # Comprehensive testing guide
├── README.MD                   # This overview file
└── venv/                       # Python virtual environment
```

## 🚀 **Quick Start**

### **For MVP RAG:**
```bash
# Clone and setup
git clone <your-repo-url>
cd h100-growthx-fy26

# Follow complete setup guide
cd mvp_rag
# See README.md for detailed instructions
```

### **For Healthcare Agentic RAG:**
```bash
# Azure AI Foundry setup
cd agentic_rag

# Configure environment variables
cp config.env.example .env
# Edit .env with your Azure credentials

# Test the complete system
python3 test_complete_workflow.py

# Launch the Gradio UI
python3 app.py
```

## 🎭 **Demo Scenarios**

### **MVP RAG Demo:**
- **Healthcare Queries**: Diabetes symptoms, blood pressure, heart attack signs
- **Real-time Responses**: AI-generated with medical disclaimers
- **Performance Metrics**: Embedding, search, and generation timing
- **Document Retrieval**: Relevant healthcare documents with citations

### **Healthcare Agentic RAG Demo:**
- **Multi-Agent Workflows**: Research → Analysis → Synthesis pipeline
- **Azure AI Search**: Enterprise knowledge retrieval with citations
- **Data Analysis**: Code Interpreter for insights and visualizations
- **Patient-Friendly Responses**: Comprehensive healthcare information
- **Real-time Workflow**: Watch agents work together in the Gradio UI

## 🔄 **Evolution Path**

```
Local MVP RAG → Production Agentic RAG
     ↓                    ↓
Ollama + Qdrant    Azure AI Foundry
     ↓                    ↓
Single Agent       Multi-Agent System
     ↓                    ↓
Local Tools        Azure AI Services Integration
     ↓                    ↓
Basic Monitoring   Enterprise Observability
     ↓                    ↓
Local Deployment   Cloud-Scale Production
```

## 🎯 **Learning Outcomes**

This repository demonstrates:
1. **AI Evolution**: From local MVP to production enterprise systems
2. **Architecture Patterns**: Scalable, secure, observable AI systems
3. **Multi-Agent Systems**: Coordinated AI workflows and orchestration
4. **Azure AI Services**: Enterprise-grade AI infrastructure
5. **Production Readiness**: Security, monitoring, and deployment
6. **Domain Expertise**: Healthcare AI with proper safety guidelines

---

**Built with ❤️ for demonstrating AI evolution from MVP to production**
