# 🏥 Healthcare Agentic RAG System

A production-ready multi-agent healthcare AI system built with Azure AI Foundry, featuring comprehensive monitoring and patient-friendly responses.

## 🏗️ Architecture

### **Multi-Agent Workflow:**
```
User Query → Research Agent → Analysis Agent + Synthesis Agent (Parallel) → Comprehensive Response
```

### **Agents:**
- **🔍 Research Agent**: Azure AI Search integration for healthcare document retrieval
- **📊 Analysis Agent**: Code Interpreter for data analysis and insights
- **📝 Synthesis Agent**: Enhanced with Code Interpreter for visualizations and patient-friendly responses

## 🚀 Features

- ✅ **Multi-Agent Architecture**: Coordinated workflow with parallel execution
- ✅ **Azure AI Foundry Integration**: Native Azure AI services
- ✅ **Comprehensive Monitoring**: Azure Monitor Application Insights integration
- ✅ **Enhanced Visualizations**: Code Interpreter for charts and graphs
- ✅ **Patient-Friendly Responses**: Clear, actionable healthcare information
- ✅ **Real-Time Progress**: Streaming updates during workflow execution
- ✅ **Dark Theme UI**: Modern, accessible interface

## 📁 Project Structure

```
agentic_rag/
├── agents/                    # Multi-agent system
│   ├── coordinator_agent.py   # Workflow orchestration
│   ├── research_agent.py      # Document retrieval
│   ├── analysis_agent.py      # Data analysis
│   └── synthesis_agent.py     # Response generation with visualizations
├── monitoring/                # Azure Monitor integration
│   ├── setup_monitoring.py    # Comprehensive monitoring setup
│   └── __init__.py
├── utils/                     # Utilities
│   ├── logging_config.py      # Logging configuration
│   └── __init__.py
├── app.py                     # Main Gradio application
├── config.env.example         # Environment configuration template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Setup

### **1. Environment Configuration**
Copy `config.env.example` to `.env` and configure:

```bash
# Azure AI Foundry Configuration
AZURE_AI_FOUNDRY_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
AZURE_AI_FOUNDRY_API_KEY=your-azure-ai-foundry-api-key-here

# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_API_KEY=your-azure-search-admin-key-here
AZURE_SEARCH_INDEX_NAME=your-search-index-name
AZURE_SEARCH_CONNECTION_ID=/subscriptions/your-subscription-id/resourceGroups/your-resource-group/providers/Microsoft.CognitiveServices/accounts/your-account/projects/your-project/connections/your-connection

# Application Insights Configuration
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=your-key;IngestionEndpoint=https://your-region.in.applicationinsights.azure.com/;LiveEndpoint=https://your-region.livediagnostics.monitor.azure.com/;ApplicationId=your-app-id

# Model Deployments
GPT4O_DEPLOYMENT=gpt-4o
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run the Application**
```bash
python app.py
```

## 📊 Monitoring

The system includes comprehensive monitoring with Azure Monitor Application Insights:

- **Workflow Traces**: Complete multi-agent execution tracking
- **Agent Performance**: Individual agent metrics and timing
- **Custom Events**: Workflow completion and status events
- **Custom Metrics**: Duration, success rates, performance data
- **Error Tracking**: Exception monitoring and debugging

### **Viewing Monitoring Data:**
1. **Azure AI Foundry Portal**: Go to Monitoring → Application analytics
2. **Azure Monitor**: Application Insights dashboard
3. **Real-time Metrics**: Live performance monitoring

## 🎯 Usage

### **Example Healthcare Queries:**
- "What are the symptoms of diabetes and how is it treated?"
- "Explain the difference between Type 1 and Type 2 diabetes"
- "What are the side effects of metformin?"
- "How do I manage high blood pressure?"
- "What are the warning signs of a heart attack?"

### **Response Format:**
- **🏥 Key Information**: Essential medical facts
- **⚠️ Warning Signs**: Symptoms to watch for
- **💊 Treatment Options**: Evidence-based treatments
- **📊 Understanding Your Condition**: Visual charts and graphs
- **💡 What You Can Do**: Actionable steps
- **🚨 When to Seek Help**: Clear guidance
- **📚 Additional Resources**: Helpful links and information

## 🔍 Technical Details

### **Performance:**
- **Typical Execution Time**: 30-40 seconds for comprehensive responses
- **Parallel Execution**: Analysis and Synthesis agents run simultaneously
- **Enhanced Capabilities**: Code Interpreter adds visualization overhead but provides better patient understanding

### **Monitoring Integration:**
- **OpenTelemetry**: Full observability stack
- **Azure AI Agents Instrumentation**: Native Azure AI Foundry tracing
- **Application Insights**: Comprehensive telemetry and analytics
- **Custom Metrics**: Performance and quality tracking

## 🚀 Getting Started

1. **Configure Environment**: Set up your Azure AI Foundry and Application Insights credentials
2. **Install Dependencies**: Run `pip install -r requirements.txt`
3. **Launch Application**: Run `python app.py`
4. **Access Interface**: Open http://localhost:7860 in your browser
5. **Ask Healthcare Questions**: Enter your queries and get comprehensive responses

## 📈 Performance Optimization

The system is optimized for:
- **Parallel Agent Execution**: Analysis and Synthesis run simultaneously
- **Efficient Resource Usage**: Optimized Azure AI service calls
- **Comprehensive Monitoring**: Real-time performance tracking
- **Patient-Friendly Output**: Clear, actionable healthcare information

## 🔒 Security & Compliance

- **Azure AI Foundry**: Enterprise-grade security and compliance
- **Application Insights**: Secure telemetry and monitoring
- **Environment Variables**: Secure credential management
- **Healthcare Focus**: Patient-friendly, evidence-based responses

---

**Built with ❤️ for healthcare professionals and patients**