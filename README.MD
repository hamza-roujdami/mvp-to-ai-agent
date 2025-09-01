# 🚀 MVP to Production Agentic RAG System

This repository demonstrates the evolution from a **local MVP RAG system** to a **production-ready agentic RAG system** using Azure AI Foundry services.

## 🏗️ Project Overview

**Two complementary AI systems showcasing AI evolution:**

### 🏥 **MVP RAG Healthcare AI Assistant**
**Location**: `mvp_rag/`  
- **Local AI Stack**: Ollama + Qdrant + Gradio
- **Healthcare Domain**: Specialized medical AI assistant
- **Cost-Effective**: Local models for rapid prototyping

### 🤖 **Healthcare Agentic RAG System**
**Location**: `agentic_rag/`  
- **Enterprise AI Stack**: Azure AI Foundry + Azure AI Agent Service
- **Multi-Agent Architecture**: Research → Analysis → Synthesis workflow
- **Production Ready**: Azure AI Search, Code Interpreter, enterprise security

## 🔄 **System Comparison**

```
MVP RAG (Local)                    Agentic RAG (Azure)
┌─────────────────────────┐        ┌─────────────────────────┐
│     Single Agent        │        │   Multi-Agent System    │
│                         │        │                         │
│  User Query            │        │  User Query            │
│       ↓                │        │       ↓                │
│  Document Search       │        │  Research Agent        │
│       ↓                │        │  (Azure AI Search)     │
│  Response Generation   │        │       ↓                │
│       ↓                │        │  Analysis Agent        │
│  Final Answer          │        │  (Code Interpreter)    │
└─────────────────────────┘        │       ↓                │
                                   │  Synthesis Agent       │
                                   │  (Response Gen)        │
                                   │       ↓                │
                                   │  Coordinated Answer    │
                                   └─────────────────────────┘

Tech Stack:                        Tech Stack:
• Ollama (Local)                   • Azure AI Foundry
• Qdrant (Local)                   • Azure AI Search
• Single Model                     • Multiple Specialized Models
• Basic Monitoring                 • Enterprise Security
• Local Deployment                 • Cloud-Scale Production
```

## 🚀 **Quick Start**

```bash
# Clone repository
git clone <your-repo-url>
cd mvp-to-ai-agent

# MVP RAG (Local)
cd mvp_rag
# See README.md for setup

# Agentic RAG (Azure)
cd agentic_rag
cp config.env.example .env
# Edit .env with Azure credentials
python3 test_complete_workflow.py
python3 app.py
```

## 📁 **Repository Structure**

```
mvp-to-ai-agent/
├── mvp_rag/                    # Local MVP RAG
├── agentic_rag/                # Azure AI Foundry
└── README.MD                   # This overview
```

## 🎯 **What You'll Learn**

- **AI Evolution**: From local MVP to production enterprise systems
- **Multi-Agent Architecture**: Coordinated AI workflows and orchestration
- **Azure AI Services**: Enterprise-grade AI infrastructure
- **Healthcare AI**: Domain expertise with proper safety guidelines

---

**Built with ❤️ for demonstrating AI evolution from MVP to production**
