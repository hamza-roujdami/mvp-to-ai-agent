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
        """Validate that all required environment variables are set."""
        required_vars = [
            "AZURE_AI_FOUNDRY_ENDPOINT",
            "AZURE_AI_FOUNDRY_API_KEY", 
            "AZURE_SEARCH_CONNECTION_ID",
            "AZURE_SEARCH_INDEX_NAME"
        ]
        
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            return False, f"❌ Missing environment variables: {', '.join(missing_vars)}"
        
        return True, "✅ All environment variables are set"
    
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
                
                # Get actual content from each agent
                research_content = workflow_results.get('research', {}).get('content', 'No research content available')
                analysis_content = workflow_results.get('analysis', {}).get('content', 'No analysis content available')
                synthesis_content = workflow_results.get('synthesis', {}).get('content', 'No synthesis content available')
                
                workflow_display = f"""
<div style="background: white; padding: 30px; border: 2px solid black; border-radius: 15px; margin: 30px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
    <h1 style="color: black; margin-bottom: 25px; font-size: 32px; font-weight: bold; text-align: center; border-bottom: 3px solid black; padding-bottom: 15px;">🏥 Healthcare Agentic RAG System</h1>
    
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #dee2e6;">
        <h3 style="color: black; margin-bottom: 15px; font-size: 20px; font-weight: bold;">📋 Query Summary</h3>
        <p style="color: black; font-size: 18px; margin: 10px 0;"><strong>Question:</strong> {question}</p>
        <p style="color: black; font-size: 18px; margin: 10px 0;"><strong>Status:</strong> ✅ Completed Successfully!</p>
        <p style="color: black; font-size: 18px; margin: 10px 0;"><strong>Agents:</strong> {summary['successful_agents']}/{summary['total_agents']} successful</p>
    </div>
</div>

<div style="margin: 40px 0;">
    <!-- Research Agent Section -->
    <div style="background: white; padding: 30px; border: 2px solid #007bff; border-radius: 15px; margin: 30px 0; box-shadow: 0 4px 15px rgba(0,123,255,0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 25px;">
            <div style="background: #007bff; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; margin-right: 20px;">🔍</div>
            <h2 style="color: #007bff; margin: 0; font-size: 28px; font-weight: bold;">Research Agent - Healthcare Document Retrieval</h2>
        </div>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #dee2e6;">
            <h4 style="color: black; margin-bottom: 15px; font-size: 18px; font-weight: bold;">📊 Agent Status</h4>
            <p style="color: black; font-size: 16px; margin: 8px 0;"><strong>Status:</strong> {workflow_results.get('research', {}).get('status', 'Unknown')}</p>
            <p style="color: black; font-size: 16px; margin: 8px 0;"><strong>Content Length:</strong> {len(research_content)} characters</p>
        </div>
        
        <div style="margin: 25px 0;">
            <h4 style="color: black; margin-bottom: 20px; font-size: 22px; font-weight: bold;">📚 Research Findings</h4>
            <div style="background: white; padding: 25px; border: 2px solid #007bff; border-radius: 12px; margin: 15px 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 16px; line-height: 1.8; color: black; max-height: 600px; overflow-y: auto; box-shadow: 0 2px 8px rgba(0,123,255,0.1);">
                {research_content}
            </div>
        </div>
    </div>
    
    <!-- Analysis Agent Section -->
    <div style="background: white; padding: 30px; border: 2px solid #28a745; border-radius: 15px; margin: 30px 0; box-shadow: 0 4px 15px rgba(40,167,69,0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 25px;">
            <div style="background: #28a745; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; margin-right: 20px;">📊</div>
            <h2 style="color: #28a745; margin: 0; font-size: 28px; font-weight: bold;">Analysis Agent - Data Analysis & Visualization</h2>
        </div>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #dee2e6;">
            <h4 style="color: black; margin-bottom: 15px; font-size: 18px; font-weight: bold;">📊 Agent Status</h4>
            <p style="color: black; font-size: 16px; margin: 8px 0;"><strong>Status:</strong> {workflow_results.get('analysis', {}).get('status', 'Unknown')}</p>
            <p style="color: black; font-size: 16px; margin: 8px 0;"><strong>Content Length:</strong> {len(analysis_content)} characters</p>
        </div>
        
        <div style="margin: 25px 0;">
            <h4 style="color: black; margin-bottom: 20px; font-size: 22px; font-weight: bold;">📊 Analysis Insights</h4>
            <div style="background: white; padding: 25px; border: 2px solid #28a745; border-radius: 12px; margin: 15px 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 16px; line-height: 1.8; color: black; max-height: 600px; overflow-y: auto; box-shadow: 0 2px 8px rgba(40,167,69,0.1);">
                {analysis_content if analysis_content else 'No analysis content generated for this query.'}
            </div>
        </div>
    </div>
    
    <!-- Synthesis Agent Section -->
    <div style="background: white; padding: 30px; border: 2px solid #dc3545; border-radius: 15px; margin: 30px 0; box-shadow: 0 4px 15px rgba(220,53,69,0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 25px;">
            <div style="background: #dc3545; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; margin-right: 20px;">📝</div>
            <h2 style="color: #dc3545; margin: 0; font-size: 28px; font-weight: bold;">Synthesis Agent - Patient-Friendly Response</h2>
        </div>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #dee2e6;">
            <h4 style="color: black; margin-bottom: 15px; font-size: 18px; font-weight: bold;">📊 Agent Status</h4>
            <p style="color: black; font-size: 16px; margin: 8px 0;"><strong>Status:</strong> {workflow_results.get('synthesis', {}).get('status', 'Unknown')}</p>
            <p style="color: black; font-size: 16px; margin: 8px 0;"><strong>Content Length:</strong> {len(synthesis_content)} characters</p>
        </div>
        
        <div style="margin: 25px 0;">
            <h4 style="color: black; margin-bottom: 20px; font-size: 22px; font-weight: bold;">📝 Final Healthcare Response</h4>
            <div style="background: white; padding: 25px; border: 2px solid #dc3545; border-radius: 12px; margin: 15px 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 16px; line-height: 1.8; color: black; max-height: 600px; overflow-y: auto; box-shadow: 0 2px 8px rgba(220,53,69,0.1);">
                {synthesis_content}
            </div>
        </div>
    </div>
</div>

<!-- Success Message -->
<div style="background: #d4edda; padding: 25px; border-radius: 15px; margin: 30px 0; border: 2px solid #28a745; text-align: center;">
    <h3 style="color: #155724; margin-bottom: 15px; font-size: 24px; font-weight: bold;">🎉 Multi-Agent Workflow Completed Successfully!</h3>
    <p style="color: #155724; font-size: 18px; margin: 0;">All agents have successfully processed your healthcare query!</p>
</div>

<!-- Final Answer Section -->
<div style="background: white; padding: 35px; border: 3px solid #6f42c1; border-radius: 20px; margin: 40px 0; box-shadow: 0 6px 20px rgba(111,66,193,0.15);">
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: #6f42c1; margin: 0; font-size: 32px; font-weight: bold;">🏥 Your Healthcare Answer</h2>
        <p style="color: #6f42c1; font-size: 18px; margin: 10px 0;">Comprehensive response synthesized from research and analysis</p>
    </div>
    
    <div style="background: #f8f9fa; padding: 30px; border: 2px solid #6f42c1; border-radius: 15px; margin: 25px 0; border-left: 8px solid #6f42c1;">
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 18px; line-height: 2.0; color: black;">
            {synthesis_content}
        </div>
    </div>
    
    <div style="background: #e9ecef; padding: 25px; border-radius: 12px; margin: 25px 0; border: 1px solid #6f42c1;">
        <h4 style="color: #6f42c1; font-size: 20px; font-weight: bold; margin-bottom: 20px;">📋 Summary of What We Found</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
            <div style="background: white; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
                <h5 style="color: #007bff; font-size: 18px; font-weight: bold; margin-bottom: 10px;">🔍 Research</h5>
                <p style="color: black; font-size: 16px; margin: 0;">Retrieved {len(research_content)} characters of healthcare information</p>
            </div>
            <div style="background: white; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
                <h5 style="color: #28a745; font-size: 18px; font-weight: bold; margin-bottom: 10px;">📊 Analysis</h5>
                <p style="color: black; font-size: 16px; margin: 0;">Generated {len(analysis_content)} characters of insights and analysis</p>
            </div>
            <div style="background: white; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
                <h5 style="color: #dc3545; font-size: 18px; font-weight: bold; margin-bottom: 10px;">📝 Synthesis</h5>
                <p style="color: black; font-size: 16px; margin: 0;">Created {len(synthesis_content)} characters of patient-friendly response</p>
            </div>
        </div>
    </div>
</div>
"""
            else:
                workflow_display = f"❌ Unexpected workflow result format: {type(workflow_results)}"
            
            # Prepare context and metrics
            context_display = f"""
<div class="context-section">
    <h3>📚 Multi-Agent Context</h3>
    <p><strong>Research Agent ID:</strong> {workflow_results.get('research', {}).get('agent_id', 'N/A')}</p>
    <p><strong>Analysis Agent ID:</strong> {workflow_results.get('analysis', {}).get('agent_id', 'N/A')}</p>
    <p><strong>Synthesis Agent ID:</strong> {workflow_results.get('synthesis', {}).get('agent_id', 'N/A')}</p>
    <p><strong>Total Content Generated:</strong> {len(workflow_results.get('research', {}).get('content', '')) + len(workflow_results.get('analysis', {}).get('content', '')) + len(workflow_results.get('synthesis', {}).get('content', ''))} characters</p>
</div>
"""
            
            metrics_display = f"""
<div class="metrics-section">
    <h3>📊 Workflow Metrics</h3>
    <p><strong>Agents Executed:</strong> {workflow_results.get('summary', {}).get('total_agents', 0)}</p>
    <p><strong>Successful Agents:</strong> {workflow_results.get('summary', {}).get('successful_agents', 0)}</p>
    <p><strong>Workflow Status:</strong> {workflow_results.get('summary', {}).get('workflow_status', 'Unknown')}</p>
    <p><strong>Execution Time:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
</div>
"""
            
            return workflow_display, context_display, metrics_display
            
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
                .gradio-container {max-width: 1200px !important;}
                .main-header {text-align: center; margin-bottom: 20px;}
                .workflow-header {background: #ffffff; padding: 20px; border-radius: 10px; margin: 20px 0; border: 3px solid #000000; box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
                .workflow-steps {margin: 20px 0;}
                .workflow-step {background: #ffffff; padding: 20px; border-radius: 8px; margin: 15px 0; border: 3px solid #000000; box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
                .step-completed {border-color: #000000; background: #ffffff;}
                .step-running {border-color: #ff6b00; background: #fff8f0;}
                .step-error {border-color: #ff0000; background: #fff5f5;}
                .step-content {margin-top: 15px; line-height: 1.8; color: #000000; font-size: 16px;}
                .workflow-summary {background: #ffffff; padding: 20px; border-radius: 10px; margin: 20px 0; border: 3px solid #000000;}
                .workflow-success {background: #ffffff; padding: 20px; border-radius: 10px; margin: 20px 0; border: 3px solid #000000; box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
                .context-section {background: #ffffff; padding: 20px; border-radius: 8px; margin: 15px 0; border: 3px solid #000000; box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
                .metrics-section {background: #ffffff; padding: 20px; border-radius: 8px; margin: 15px 0; border: 3px solid #000000; box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
                .history-item {background: #ffffff; padding: 15px; border-radius: 8px; margin: 10px 0; border: 2px solid #000000;}
                .agent-card {background: linear-gradient(135deg, #000000 0%, #333333 100%); color: white; padding: 20px; border-radius: 12px; margin: 10px 0; border: 2px solid #ffffff;}
                .example-btn {margin: 5px; min-width: 120px;}
                .final-response {background: #ffffff; padding: 20px; border-radius: 10px; margin: 20px 0; border: 3px solid #000000; box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
                .response-content {background: #f0f0f0; padding: 20px; border-radius: 8px; margin: 15px 0; border: 2px solid #000000; color: #000000; line-height: 1.8;}
                .response-summary {background: #e0e0e0; padding: 20px; border-radius: 8px; margin: 15px 0; color: #000000; border: 2px solid #000000;}
                .research-content, .analysis-content, .synthesis-content {background: #f8f8f8; padding: 20px; border-radius: 8px; margin: 15px 0; border: 3px solid #000000; font-family: 'Arial', 'Helvetica', sans-serif; font-size: 16px; line-height: 1.8; color: #000000; max-height: 500px; overflow-y: auto; box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
                .research-content {border-color: #000000;}
                .analysis-content {border-color: #000000;}
                .synthesis-content {border-color: #000000;}
                .step-content h4 {color: #000000; margin-bottom: 15px; font-size: 18px; font-weight: bold;}
                .step-content strong {color: #000000; font-weight: bold; font-size: 16px;}
                .workflow-header h2 {color: #000000; margin-bottom: 20px; font-size: 24px; font-weight: bold;}
                .workflow-header p {color: #000000; font-size: 18px; font-weight: 500;}
                .context-section h3, .metrics-section h3 {color: #000000; margin-bottom: 20px; font-size: 20px; font-weight: bold;}
                .context-section p, .metrics-section p {color: #000000; margin: 12px 0; font-size: 16px; font-weight: 500;}
                .final-response h3 {color: #000000; margin-bottom: 20px; font-size: 22px; font-weight: bold;}
                .response-content {font-size: 18px; line-height: 2.0; color: #000000; font-weight: 500;}
                .response-summary h4 {color: #000000; font-size: 18px; font-weight: bold;}
                .response-summary ul {color: #000000; font-size: 16px;}
                .response-summary li {margin: 8px 0; color: #000000;}
                .research-content div, .analysis-content div, .synthesis-content div {color: #000000; font-weight: 500;}
                .step-content br {margin: 8px 0;}
            """
        ) as app:
            
            # Header section
            gr.Markdown("""
            # 🏥 Healthcare Agentic RAG System
            
            **Demonstrating Multi-Agent AI Evolution: From Single RAG to Orchestrated Intelligence**
            
            Ask any health-related question and see how our **4-agent system** works together:
            - 🔍 **Research Agent**: Azure AI Search for document retrieval
            - 📊 **Analysis Agent**: Code Interpreter for data analysis & visualization
            - 📝 **Synthesis Agent**: Patient-friendly response generation
            - 🎯 **Coordinator Agent**: Multi-agent workflow orchestration
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
                size="lg"
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
            
            # Output sections
            with gr.Row():
                with gr.Column(scale=2):
                    response_output = gr.HTML(
                        label="🤖 Multi-Agent Workflow Results",
                        value="<div class='workflow-header'><h3>Submit a health question to see the multi-agent workflow in action!</h3></div>",
                        elem_classes=["response-box"]
                    )
                
                with gr.Column(scale=1):
                    context_output = gr.HTML(
                        label="📚 Context & Agent Info",
                        value="<div class='context-section'><h3>Context will appear here when you ask a question...</h3></div>",
                        elem_classes=["context-box"]
                    )
            
            # Performance metrics
            metrics_output = gr.HTML(
                label="📊 Workflow Metrics",
                value="<div class='metrics-section'><h3>Metrics will appear here after your first query...</h3></div>",
                elem_classes=["metric-box"]
            )
            
            # Workflow history section
            with gr.Row():
                with gr.Column(scale=1):
                    history_btn = gr.Button("📜 View History", variant="secondary")
                with gr.Column(scale=1):
                    clear_history_btn = gr.Button("🗑️ Clear History", variant="secondary", size="sm")
            
            history_output = gr.HTML(
                label="📋 Workflow History",
                value="<div class='history-section'><h3>No workflows executed yet...</h3></div>"
            )
            
            # Event handlers
            submit_btn.click(
                fn=self.execute_healthcare_workflow,
                inputs=[question_input],
                outputs=[response_output, context_output, metrics_output],
                api_name="execute_workflow",
                queue=True
            )
            
            # Enter key support
            question_input.submit(
                fn=self.execute_healthcare_workflow,
                inputs=[question_input],
                outputs=[response_output, context_output, metrics_output],
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
            ---
            
            ## 🏗️ Built with Azure AI Foundry
            
            This system demonstrates the power of **Azure AI Foundry** for building multi-agent AI systems:
            
            - **Azure AI Search**: Enterprise-grade vector search for healthcare documents
            - **Azure AI Agents**: Multi-agent orchestration and workflow management
            - **Azure AI Models**: GPT-4o and Code Interpreter capabilities
            
            ## 🔒 Privacy & Security
            
            - All processing happens in Azure AI Foundry
            - No data is stored locally
            - Healthcare information is for educational purposes only
            - Always consult healthcare professionals for medical advice
            
            ---
            
            *Healthcare Agentic RAG System - Demonstrating the future of AI-powered healthcare information retrieval and analysis.*
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
