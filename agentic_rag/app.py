#!/usr/bin/env python3
"""
🏥 Healthcare Agentic RAG System - Gradio Web Interface

This module creates a beautiful, interactive web interface for demonstrating
the multi-agent healthcare RAG system with Azure AI Foundry. It showcases:

- Multi-agent workflow orchestration
- Real-time healthcare AI assistance
- Agent-by-agent progress tracking
- Professional medical disclaimers
- Beautiful, modern UI design
"""

import gradio as gr
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.coordinator_agent import execute_multi_agent_workflow

# Load environment variables
load_dotenv()

class GradioAgenticRAGInterface:
    """
    Gradio interface for the Healthcare Agentic RAG System.
    
    This class handles:
    - Web UI creation and management
    - Multi-agent workflow integration
    - User interaction processing
    - Response formatting and display
    - Workflow history tracking
    """
    
    def __init__(self):
        """Initialize the Gradio interface."""
        self.logger = None
        self.workflow_history = []  # Instance variable instead of global
        self.setup_logging()
        
    def setup_logging(self):
        """Setup basic logging."""
        try:
            import logging
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger("agentic_rag_ui")
            self.logger.info("✅ Agentic RAG UI initialized successfully")
        except Exception as e:
            print(f"⚠️ Logging setup skipped: {e}")
    
    def validate_environment(self):
        """Validate that all required environment variables are set and test Azure connections."""
        required_vars = [
            "AZURE_AI_FOUNDRY_ENDPOINT",
            "AZURE_AI_FOUNDRY_API_KEY", 
            "AZURE_SEARCH_CONNECTION_ID",
            "AZURE_SEARCH_INDEX_NAME"
        ]
        
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            return False, f"❌ Missing environment variables: {', '.join(missing_vars)}"
        
        # Test Azure AI Foundry connection
        try:
            from azure.ai.projects import AIProjectClient
            from azure.identity import DefaultAzureCredential
            
            endpoint = os.environ["AZURE_AI_FOUNDRY_ENDPOINT"]
            api_key = os.environ["AZURE_AI_FOUNDRY_API_KEY"]
            
            # Test connection by creating a client
            project_client = AIProjectClient(
                endpoint=endpoint,
                credential=api_key
            )
            
            # Try to list projects to test connection
            try:
                projects = list(project_client.projects.list())
                ai_foundry_status = "✅ Connected"
            except Exception as e:
                ai_foundry_status = f"⚠️ Connected but limited access: {str(e)[:100]}"
                
        except Exception as e:
            ai_foundry_status = f"❌ Connection failed: {str(e)[:100]}"
        
        # Test Azure Search connection
        try:
            from azure.search.documents import SearchClient
            from azure.core.credentials import AzureKeyCredential
            
            search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT", "")
            search_key = os.environ.get("AZURE_SEARCH_ADMIN_KEY", "")
            search_index = os.environ["AZURE_SEARCH_INDEX_NAME"]
            
            if search_endpoint and search_key:
                search_client = SearchClient(
                    endpoint=search_endpoint,
                    index_name=search_index,
                    credential=AzureKeyCredential(search_key)
                )
                
                # Try to get document count to test connection
                try:
                    doc_count = search_client.get_document_count()
                    search_status = f"✅ Connected (Index: {search_index}, Docs: {doc_count})"
                except Exception as e:
                    search_status = f"⚠️ Connected but limited access: {str(e)[:100]}"
            else:
                search_status = "⚠️ Using connection ID (direct test not available)"
                
        except Exception as e:
            search_status = f"❌ Connection failed: {str(e)[:100]}"
        
        # Overall status
        if "❌" in ai_foundry_status or "❌" in search_status:
            overall_status = "❌ System Issues Detected"
        elif "⚠️" in ai_foundry_status or "⚠️" in search_status:
            overall_status = "⚠️ System Partially Working"
        else:
            overall_status = "✅ System Ready"
        
        # Test agent creation (optional)
        agent_test_status = "⚠️ Not tested"
        if "✅" in ai_foundry_status:
            try:
                # Quick test of agent creation
                from agents.research_agent import create_research_agent
                test_agent, _ = create_research_agent()
                agent_test_status = "✅ Agents can be created successfully"
            except Exception as e:
                agent_test_status = f"⚠️ Agent creation test failed: {str(e)[:100]}"
        
        status_message = f"""## 🔧 System Status Check

### 📊 Overall Status
{overall_status}

### 🚀 Azure AI Foundry
{ai_foundry_status}

### 🔍 Azure AI Search
{search_status}

### 🤖 Agent System
{agent_test_status}

### 📋 Environment Variables
✅ All required variables are set

### 💡 Next Steps
- If status shows ❌, check your Azure credentials
- If status shows ⚠️, the system may work with limited functionality
- If status shows ✅, you're ready to ask healthcare questions!"""
        
        return True, status_message
    
    def format_workflow_step(self, step_name, content, status="completed"):
        """Format a workflow step for display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if status == "completed":
            status_icon = "✅"
            status_class = "step-completed"
        elif status == "running":
            status_icon = "🔄"
            status_class = "step-running"
        else:
            status_icon = "❌"
            status_class = "step-error"
        
        return f"""
<div class="workflow-step {status_class}">
    <h4>{status_icon} {step_name} ({timestamp})</h4>
    <div class="step-content">{content}</div>
</div>
"""
    
    def execute_healthcare_workflow(self, question: str, progress=gr.Progress()):
        """
        Execute the complete multi-agent healthcare workflow.
        
        Args:
            question: User's healthcare question
            progress: Gradio progress tracker
            
        Returns:
            Formatted workflow results
        """
        
        print(f"🔍 UI received query: {question}")
        
        # Validate environment
        env_valid, env_message = self.validate_environment()
        if not env_valid:
            return env_message, "", ""
        
        try:
            # Execute the multi-agent workflow
            print("🚀 Starting workflow execution...")
            workflow_results = execute_multi_agent_workflow(question)
            print(f"✅ Workflow completed: {workflow_results.keys() if isinstance(workflow_results, dict) else 'Not a dict'}")
            
            # Store in history
            self.workflow_history.append({
                "timestamp": datetime.now().isoformat(),
                "query": question,
                "status": "completed",
                "results": workflow_results
            })
            
            # Format the main response
            if isinstance(workflow_results, dict) and 'summary' in workflow_results:
                summary = workflow_results["summary"]
                
                # Get actual content from each agent and clean it up
                research_content = workflow_results.get('research', {}).get('content', 'No research content available')
                analysis_content = workflow_results.get('analysis', {}).get('content', 'No analysis content available')
                synthesis_content = workflow_results.get('synthesis', {}).get('content', 'No synthesis content available')
                
                # Debug: Print the actual content structure
                print(f"🔍 Research content type: {type(research_content)}")
                print(f"🔍 Research content: {research_content}")
                print(f"📊 Analysis content type: {type(analysis_content)}")
                print(f"📊 Analysis content: {analysis_content}")
                print(f"📝 Synthesis content type: {type(synthesis_content)}")
                print(f"📝 Synthesis content: {synthesis_content}")
                
                # Clean up the content by extracting text from complex objects
                def clean_content(content):
                    print(f"🔍 Cleaning content of type: {type(content)}")
                    print(f"🔍 Raw content: {content}")
                    
                    # Handle string representations of lists
                    if isinstance(content, str) and content.startswith("[") and content.endswith("]"):
                        try:
                            import ast
                            content = ast.literal_eval(content)
                            print(f"  🔄 Converted string to list: {type(content)}")
                        except:
                            print(f"  ⚠️ Could not parse string as list, treating as string")
                            return content
                    
                    if isinstance(content, str):
                        return content
                    elif isinstance(content, list):
                        # Handle list of objects with text values
                        cleaned_parts = []
                        for i, item in enumerate(content):
                            print(f"  📝 Processing list item {i}: {type(item)}")
                            if isinstance(item, dict):
                                print(f"    📝 Item keys: {list(item.keys())}")
                                if 'text' in item and isinstance(item['text'], dict) and 'value' in item['text']:
                                    print(f"      ✅ Found nested text.value: {item['text']['value'][:100]}...")
                                    cleaned_parts.append(item['text']['value'])
                                elif 'value' in item:
                                    cleaned_parts.append(item['value'])
                                elif 'content' in item:
                                    cleaned_parts.append(item['content'])
                                elif 'text' in item and isinstance(item['text'], str):
                                    cleaned_parts.append(item['text'])
                            elif isinstance(item, str):
                                cleaned_parts.append(item)
                        
                        result = '\n\n'.join(cleaned_parts) if cleaned_parts else str(content)
                        print(f"  ✅ List cleaning result: {result[:100]}...")
                        return result
                    elif isinstance(content, dict):
                        # Handle dict with text values
                        print(f"  📝 Processing dict: {list(content.keys())}")
                        if 'value' in content:
                            return content['value']
                        elif 'text' in content:
                            text_obj = content['text']
                            if isinstance(text_obj, dict) and 'value' in text_obj:
                                return text_obj['value']
                            elif isinstance(text_obj, str):
                                return text_obj
                        elif 'content' in content:
                            return content['content']
                        elif 'message' in content:
                            return content['message']
                    
                    result = str(content)
                    print(f"  ✅ Final result: {result[:100]}...")
                    return result
                
                # Clean all content
                research_content = clean_content(research_content)
                analysis_content = clean_content(analysis_content)
                synthesis_content = clean_content(synthesis_content)
                
                print(f"✅ Cleaned research content: {research_content[:100]}...")
                print(f"✅ Cleaned analysis content: {analysis_content[:100]}...")
                print(f"✅ Cleaned synthesis content: {synthesis_content[:100]}...")
                
                # Clean, focused formatting with separate rectangular sections
                workflow_display = f"""<div class="section-container">
<div class="section healthcare-section">
<h2>💡 Healthcare Information</h2>
<div class="section-content">
{synthesis_content}
</div>
</div>

<div class="section metrics-section">
<h2>📊 Workflow Metrics</h2>
<div class="section-content">
- **Research:** ✅ Completed ({len(research_content)} characters)
- **Analysis:** ✅ Completed ({len(analysis_content) if analysis_content else 0} characters)  
- **Synthesis:** ✅ Completed ({len(synthesis_content)} characters)
</div>
</div>

<div class="section technical-section">
<h2>🔍 Technical Details</h2>
<div class="section-content">
<details>
<summary><strong>📚 Research Details</strong></summary>
{research_content}
</details>

<details>
<summary><strong>📊 Analysis Details</strong></summary>
{analysis_content if analysis_content else 'No analysis content generated for this query.'}
</details>
</details>
</div>
</div>

<div class="section context-section">
<h2>📚 Agent Context</h2>
<div class="section-content">
- **Research Agent ID:** {workflow_results.get('research', {}).get('agent_id', 'N/A')}
- **Analysis Agent ID:** {workflow_results.get('analysis', {}).get('agent_id', 'N/A')}
- **Synthesis Agent ID:** {workflow_results.get('synthesis', {}).get('agent_id', 'N/A')}
- **Total Content:** {len(workflow_results.get('research', {}).get('content', '')) + len(workflow_results.get('analysis', {}).get('content', '')) + len(workflow_results.get('synthesis', {}).get('content', ''))} characters
</div>
</div>
</div>

<div class="footer-section">
<p><strong>💊 Important:</strong> This information is for educational purposes only. Always consult healthcare professionals for medical advice.</p>
<p><strong>🎯 Next Steps:</strong> Consider discussing these findings with your healthcare provider for personalized medical guidance.</p>
</div>"""
            else:
                workflow_display = f"❌ Unexpected workflow result format: {type(workflow_results)}"
            
            # Prepare context and metrics
            # context_display = f"""
            # <div class="context-section">
            #     <h3>📚 Multi-Agent Context</h3>
            #     <p><strong>Research Agent ID:</strong> {workflow_results.get('research', {}).get('agent_id', 'N/A')}</p>
            #     <p><strong>Analysis Agent ID:</strong> {workflow_results.get('analysis', {}).get('agent_id', 'N/A')}</p>
            #     <p><strong>Synthesis Agent ID:</strong> {workflow_results.get('synthesis', {}).get('agent_id', 'N/A')}</p>
            #     <p><strong>Total Content Generated:</strong> {len(workflow_results.get('research', {}).get('content', '')) + len(workflow_results.get('analysis', {}).get('content', '')) + len(workflow_results.get('synthesis', {}).get('content', ''))} characters</p>
            # </div>
            # """
            
            # metrics_display = f"""
            # <div class="metrics-section">
            #     <h3>📊 Workflow Metrics</h3>
            #     <p><strong>Agents Executed:</strong> {workflow_results.get('summary', {}).get('total_agents', 0)}</p>
            #     <p><strong>Successful Agents:</strong> {workflow_results.get('summary', {}).get('successful_agents', 0)}</p>
            #     <p><strong>Workflow Status:</strong> {workflow_results.get('summary', {}).get('workflow_status', 'Unknown')}</p>
            #     <p><strong>Execution Time:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            # </div>
            # """
            
            return workflow_display, "", ""
            
        except Exception as e:
            error_message = f"❌ <strong>Workflow Error:</strong> {str(e)}<br><br>Please check your configuration and try again."
            print(f"❌ Error in workflow: {e}")
            import traceback
            traceback.print_exc()
            
            # Store error in history
            self.workflow_history.append({
                "timestamp": datetime.now().isoformat(),
                "query": question,
                "status": "error",
                "error": str(e)
            })
            
            return error_message, "❌ Error occurred during workflow execution", "❌ No metrics available"
    
    def get_workflow_history(self):
        """Get the workflow execution history."""
        if not self.workflow_history:
            return "No workflows executed yet."
        
        history_display = "<h3>📋 Workflow Execution History</h3>"
        
        for i, workflow in enumerate(reversed(self.workflow_history), 1):
            timestamp = datetime.fromisoformat(workflow["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            status_icon = "✅" if workflow["status"] == "completed" else "❌"
            
            history_display += f"""
<div class="history-item">
    <h4>{i}. {status_icon} {timestamp}</h4>
    <p><strong>Query:</strong> {workflow['query']}</p>
    <p><strong>Status:</strong> {workflow['status']}</p>
"""
            
            if workflow["status"] == "completed" and "results" in workflow:
                results = workflow["results"]
                if "summary" in results:
                    summary = results["summary"]
                    history_display += f"<p><strong>Agents:</strong> {summary['successful_agents']}/{summary['total_agents']} successful</p>"
            
            history_display += "</div><hr>"
        
        return history_display
    
    def clear_history(self):
        """Clear the workflow history."""
        self.workflow_history.clear()
        return "✅ Workflow history cleared!"
    
    def create_interface(self) -> gr.Blocks:
        """
        Create and configure the Gradio web interface.
        
        Returns:
            Configured Gradio interface ready for launch
        """
        
        # Create the main interface components
        with gr.Blocks(
            title="🏥 Healthcare Agentic RAG System",
            theme=gr.themes.Soft(),
            css="""
                /* Main container */
                .gradio-container {max-width: 1400px !important; margin: 0 auto !important;}
                
                /* Header styling */
                .main-header {text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%); border-radius: 15px; border: 2px solid #4a5568;}
                .main-header h1 {color: #f7fafc !important; font-size: 2.5em !important; margin-bottom: 15px !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);}
                .main-header p {color: #e2e8f0 !important; font-size: 1.2em !important; line-height: 1.6 !important;}
                
                /* Agent cards */
                .agent-card {background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%); padding: 25px; border-radius: 15px; margin: 15px 0; border: 2px solid #718096; text-align: center; color: #e2e8f0; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.3);}
                .agent-card:hover {transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.4); border-color: #48bb78;}
                .agent-card h3 {color: #48bb78 !important; margin-bottom: 15px !important; font-size: 1.4em !important; font-weight: bold !important;}
                .agent-card p {color: #e2e8f0 !important; line-height: 1.6 !important; font-size: 1.1em !important;}
                
                /* Input section */
                .input-section {background: #2d3748; padding: 25px; border-radius: 15px; margin: 25px 0; border: 2px solid #4a5568; box-shadow: 0 4px 15px rgba(0,0,0,0.3);}
                
                /* Buttons */
                .submit-btn {background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important; border: none !important; color: white !important; font-weight: bold !important; padding: 15px 30px !important; border-radius: 10px !important; font-size: 1.1em !important; transition: all 0.3s ease !important;}
                .submit-btn:hover {transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4) !important;}
                
                .example-btn {background: linear-gradient(135deg, #4a5568 0%, #718096 100%) !important; border: 2px solid #718096 !important; color: #e2e8f0 !important; margin: 8px !important; min-width: 140px !important; padding: 12px 20px !important; border-radius: 8px !important; transition: all 0.3s ease !important;}
                .example-btn:hover {background: linear-gradient(135deg, #718096 0%, #4a5568 100%) !important; border-color: #48bb78 !important; transform: translateY(-2px) !important;}
                
                /* Status section */
                .status-section {background: #2d3748; padding: 20px; border-radius: 12px; border: 2px solid #4a5568; margin: 20px 0;}
                
                /* Output sections */
                .output-section {background: #1a202c; padding: 25px; border-radius: 15px; margin: 25px 0; border: 2px solid #4a5568; box-shadow: 0 4px 15px rgba(0,0,0,0.4);}
                .output-section h3 {color: #48bb78 !important; margin-bottom: 20px !important; font-size: 1.5em !important; border-bottom: 2px solid #48bb78 !important; padding-bottom: 10px !important;}
                
                /* Healthcare answer highlight */
                .healthcare-answer {background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%); padding: 35px; border: 3px solid #48bb78; border-radius: 20px; margin: 30px 0; box-shadow: 0 8px 30px rgba(72, 187, 120, 0.3); color: #f7fafc; position: relative;}
                .healthcare-answer::before {content: '🏥'; position: absolute; top: -20px; left: 50%; transform: translateX(-50%); background: #48bb78; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; border: 3px solid #1a202c;}
                .healthcare-answer h2 {color: #48bb78 !important; text-align: center !important; margin-bottom: 30px !important; font-size: 2em !important; border-bottom: 2px solid #48bb78 !important; padding-bottom: 20px !important;}
                
                /* Collapsible sections */
                details {background: #2d3748; padding: 20px; border-radius: 12px; margin: 15px 0; border: 2px solid #4a5568; color: #e2e8f0;}
                details summary {color: #48bb78 !important; font-weight: bold !important; font-size: 1.2em !important; cursor: pointer !important; padding: 10px 0 !important; border-bottom: 1px solid #4a5568 !important;}
                details summary:hover {color: #38a169 !important;}
                
                /* Footer */
                .footer {background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%); padding: 30px; border-radius: 15px; margin: 30px 0; border: 2px solid #4a5568; text-align: center; color: #e2e8f0;}
                .footer h2 {color: #48bb78 !important; margin-bottom: 20px !important;}
                .footer p {color: #e2e8f0 !important; line-height: 1.6 !important;}
                
                /* New styles for section-container and sections */
                .section-container {
                    display: flex;
                    flex-direction: column;
                    gap: 20px; /* Space between sections */
                }
                .section {
                    background: #2d3748;
                    padding: 25px;
                    border-radius: 15px;
                    border: 2px solid #4a5568;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    color: #e2e8f0;
                }
                .section-content {
                    color: #e2e8f0;
                    line-height: 1.8;
                    font-size: 1.1em;
                }
                .section-content p {
                    margin-bottom: 10px;
                }
                .section-content strong {
                    color: #48bb78;
                }
                .section-content details {
                    background: #2d3748;
                    padding: 15px;
                    border-radius: 10px;
                    border: 1px solid #4a5568;
                    margin-top: 10px;
                }
                .section-content details summary {
                    color: #48bb78 !important;
                    font-weight: bold !important;
                    font-size: 1.1em !important;
                    cursor: pointer !important;
                    padding: 8px 0 !important;
                    border-bottom: 1px solid #4a5568 !important;
                }
                .section-content details summary:hover {
                    color: #38a169 !important;
                }
                .section-content details p {
                    color: #e2e8f0;
                    margin-top: 10px;
                }
                
                                 /* Footer section styling */
                 .footer-section {
                     background: #1a202c;
                     padding: 20px;
                     border-radius: 10px;
                     border: 1px solid #4a5568;
                     margin-top: 20px;
                     text-align: center;
                 }
                 .footer-section p {
                     color: #e2e8f0;
                     margin: 8px 0;
                     font-size: 1em;
                 }
                 .footer-section strong {
                     color: #48bb78;
                 }
                 
                 /* Context section styling */
                 .context-section {
                     background: #2d3748;
                     padding: 25px;
                     border-radius: 15px;
                     border: 2px solid #4a5568;
                     box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                     color: #e2e8f0;
                 }
                 
                /* Responsive design */
                @media (max-width: 768px) {
                    .gradio-container {max-width: 95% !important;}
                    .agent-card {margin: 10px 0 !important; padding: 20px !important;}
                    .healthcare-answer {padding: 25px !important;}
                    .section-container {
                        padding: 0 10px;
                    }
                    .section {
                        padding: 15px;
                    }
                }
            """
        ) as app:
            
            # Header section
            gr.Markdown("""
            # 🏥 Healthcare Agentic RAG System
            
            **Multi-Agent AI System for Healthcare Information**
            """, elem_classes=["main-header"])
            
            # Agent showcase section
            gr.Markdown("## 🤖 Our AI Agent Team")
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("""
                    <div class="agent-card">
                        <h3>🔍 Research Agent</h3>
                        <p>Uses Azure AI Search to find relevant healthcare documents and extract medical information with sources.</p>
                    </div>
                    """)
                
                with gr.Column(scale=1):
                    gr.Markdown("""
                    <div class="agent-card">
                        <h3>📊 Analysis Agent</h3>
                        <p>Uses Code Interpreter to analyze medical data, create visualizations, and identify patterns.</p>
                    </div>
                    """)
                
                with gr.Column(scale=1):
                    gr.Markdown("""
                    <div class="agent-card">
                        <h3>📝 Synthesis Agent</h3>
                        <p>Generates comprehensive, patient-friendly healthcare responses from research and analysis.</p>
                    </div>
                    """)
                
                with gr.Column(scale=1):
                    gr.Markdown("""
                    <div class="agent-card">
                        <h3>🎯 Coordinator Agent</h3>
                        <p>Orchestrates the complete workflow: Research → Analysis → Synthesis → Final Response.</p>
                    </div>
                    """)
            
            # Main input section
            with gr.Row():
                with gr.Column(scale=3):
                    question_input = gr.Textbox(
                        label="🏥 Your Health Question",
                        placeholder="e.g., What are the symptoms and risk factors of diabetes?",
                        lines=3,
                        max_lines=5
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### 🔧 System Status")
                    status_btn = gr.Button("📊 Check Status", variant="secondary", size="sm")
                    status_output = gr.Markdown("Click to check system status...")
            
            # Submit button
            submit_btn = gr.Button(
                "🚀 Execute Multi-Agent Workflow",
                variant="primary",
                size="lg",
                elem_classes=["submit-btn"]
            )
            
            # Example prompts section
            gr.Markdown("### 💡 **Try These Example Queries:**")
            
            with gr.Row():
                with gr.Column(scale=1):
                    example_btn_1 = gr.Button(
                        "🩺 Diabetes Symptoms",
                        size="sm",
                        variant="secondary",
                        elem_classes=["example-btn"]
                    )
                    example_btn_2 = gr.Button(
                        "💊 Blood Pressure",
                        size="sm",
                        variant="secondary",
                        elem_classes=["example-btn"]
                    )
                
                with gr.Column(scale=1):
                    example_btn_3 = gr.Button(
                        "🫀 Heart Disease",
                        size="sm",
                        variant="secondary",
                        elem_classes=["example-btn"]
                    )
                    example_btn_4 = gr.Button(
                        "🦠 COVID-19",
                        size="sm",
                        variant="secondary",
                        elem_classes=["example-btn"]
                    )
                
                with gr.Column(scale=1):
                    example_btn_5 = gr.Button(
                        "🧠 Mental Health",
                        size="sm",
                        variant="secondary",
                        elem_classes=["example-btn"]
                    )
                    example_btn_6 = gr.Button(
                        "👶 Pregnancy",
                        size="sm",
                        variant="secondary",
                        elem_classes=["example-btn"]
                    )
            
            # Output section - consolidated into one clean display
            response_output = gr.HTML(
                label="🤖 Multi-Agent Workflow Results",
                value="<div class='output-section'><h3>Submit a health question to see the multi-agent workflow in action!</h3></div>",
                elem_classes=["output-section"]
            )
            
            # Workflow history section
            with gr.Row():
                with gr.Column(scale=1):
                    history_btn = gr.Button("📜 View History", variant="secondary")
                with gr.Column(scale=1):
                    clear_history_btn = gr.Button("🗑️ Clear History", variant="secondary", size="sm")
            
            history_output = gr.HTML(
                label="📋 Workflow History",
                value="<div class='output-section'><h3>No workflows executed yet...</h3></div>",
                elem_classes=["output-section"]
            )
            
            # Event handlers
            submit_btn.click(
                fn=self.execute_healthcare_workflow,
                inputs=[question_input],
                outputs=[response_output],
                api_name="execute_workflow",
                queue=True
            )
            
            # Enter key support
            question_input.submit(
                fn=self.execute_healthcare_workflow,
                inputs=[question_input],
                outputs=[response_output],
                api_name="execute_workflow_enter",
                queue=True
            )
            
            # Status check
            status_btn.click(
                fn=self.validate_environment,
                inputs=[],
                outputs=[status_output]
            )
            
            # History management
            history_btn.click(
                fn=self.get_workflow_history,
                inputs=[],
                outputs=[history_output]
            )
            
            clear_history_btn.click(
                fn=self.clear_history,
                inputs=[],
                outputs=[history_output]
            )
            
            # Example button handlers
            example_btn_1.click(
                fn=lambda: "What are the symptoms and risk factors of diabetes?",
                outputs=[question_input]
            )
            
            example_btn_2.click(
                fn=lambda: "How does high blood pressure affect the heart and what are the treatment options?",
                outputs=[question_input]
            )
            
            example_btn_3.click(
                fn=lambda: "What are the warning signs of heart disease and how can I prevent it?",
                outputs=[question_input]
            )
            
            example_btn_4.click(
                fn=lambda: "What are the current COVID-19 symptoms and prevention guidelines?",
                outputs=[question_input]
            )
            
            example_btn_5.click(
                fn=lambda: "What are the signs of depression and anxiety, and when should I seek professional help?",
                outputs=[question_input]
            )
            
            example_btn_6.click(
                fn=lambda: "What are the important prenatal care guidelines for pregnant women?",
                outputs=[question_input]
            )
            
            # Footer
            gr.Markdown("""
            <div class="footer">
            <h2>🏗️ Built with Azure AI Foundry</h2>
            
            <p>This system demonstrates the power of <strong>Azure AI Foundry</strong> for building multi-agent AI systems:</p>
            
            <p>• <strong>Azure AI Search</strong>: Enterprise-grade vector search for healthcare documents<br>
            • <strong>Azure AI Agents</strong>: Multi-agent orchestration and workflow management<br>
            • <strong>Azure AI Models</strong>: GPT-4o and Code Interpreter capabilities</p>
            
            <h3>🔒 Privacy & Security</h3>
            
            <p>• All processing happens in Azure AI Foundry<br>
            • No data is stored locally<br>
            • Healthcare information is for educational purposes only<br>
            • Always consult healthcare professionals for medical advice</p>
            
            <p><em>Healthcare Agentic RAG System - Demonstrating the future of AI-powered healthcare information retrieval and analysis.</em></p>
            </div>
            """)
        
        return app
    
    def launch(self):
        """Launch the Gradio web interface."""
        app = self.create_interface()
        
        # Launch with optimized settings for demo
        app.launch(
            server_name="0.0.0.0",      # Allow external connections
            server_port=7860,            # Standard Gradio port
            share=False,                 # Local only for demo
            show_error=True,             # Show errors for debugging
            quiet=False                  # Show startup info
        )


def main():
    """Main entry point for the Healthcare Agentic RAG System."""
    try:
        # Create and launch the interface
        interface = GradioAgenticRAGInterface()
        interface.launch()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your Azure AI Foundry configuration.")


if __name__ == "__main__":
    main()
