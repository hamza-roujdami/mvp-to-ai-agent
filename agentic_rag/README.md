# 🏥 Healthcare Agentic RAG System

A production-ready multi-agent RAG system built with Azure AI Foundry, featuring intelligent healthcare document retrieval, analysis, and patient-friendly response generation.

## 🎯 **System Overview**

This Healthcare Agentic RAG System uses a sophisticated multi-agent architecture to provide comprehensive, evidence-based healthcare information:

- **🔍 Research Agent**: Uses Azure AI Search to retrieve relevant healthcare documents
- **📊 Analysis Agent**: Employs Code Interpreter for data analysis and visualization
- **📝 Synthesis Agent**: Generates patient-friendly, comprehensive healthcare responses
- **🎯 Coordinator Agent**: Orchestrates the complete multi-agent workflow

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.9+
- Azure AI Foundry account with deployed models
- Azure AI Search service with healthcare documents
- Virtual environment (recommended)

### **1. Environment Setup**
```bash
# Clone and navigate to project
cd agentic_rag

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Configuration**
```bash
# Copy and configure environment variables
cp config.env.example .env

# Edit .env with your Azure credentials:
# - AZURE_AI_FOUNDRY_ENDPOINT
# - AZURE_AI_FOUNDRY_API_KEY  
# - AZURE_SEARCH_CONNECTION_ID
# - AZURE_SEARCH_INDEX_NAME
```

## 🧪 **Testing the System**

### **Option 1: CLI Testing (Recommended for First Run)**

#### **Test Individual Agents**
```bash
# Test Research Agent (Azure AI Search)
python3 agents/research_agent.py

# Test Analysis Agent (Code Interpreter)
python3 agents/analysis_agent.py

# Test Synthesis Agent (Response Generation)
python3 agents/synthesis_agent.py
```

#### **Test Complete Workflow**
```bash
# Test the entire multi-agent pipeline
python3 test_complete_workflow.py
```

### **Option 2: Gradio Web UI**

#### **Start the Web Interface**
```bash
# Start Gradio UI (runs on http://localhost:7860)
python3 app.py
```

#### **Using the Web Interface**
1. **Open your browser** to `http://localhost:7860`
2. **Enter a healthcare query** (e.g., "What are diabetes symptoms?")
3. **Watch the multi-agent workflow** execute in real-time:
   - 🔍 Research Agent searches documents
   - 📊 Analysis Agent processes data
   - 📝 Synthesis Agent generates response
4. **View the final comprehensive answer** with all insights combined

## 🏗️ **System Architecture**

```
User Query → Coordinator Agent → Research Agent → Analysis Agent → Synthesis Agent → Final Response
                ↓                    ↓              ↓              ↓
            Orchestrates        Azure AI      Code Interpreter  Patient-Friendly
            Workflow           Search Tool    Data Analysis     Response
```

## 🧪 **Testing Scenarios**

### **Healthcare Query Examples**
```bash
# Diabetes and general health
"What are the symptoms and risk factors of diabetes?"
"How does diabetes affect the cardiovascular system?"
"What are the latest treatment options for Type 2 diabetes?"

# Heart health
"What are the warning signs of a heart attack?"
"How does high blood pressure affect the body?"
"What lifestyle changes can improve heart health?"

# Mental health
"What are the symptoms of depression and anxiety?"
"How does stress affect physical health?"
"What are effective stress management techniques?"
```

