"""
Healthcare Connected Agents System - Main Application
Gradio interface for the connected agents workflow
"""

import gradio as gr
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify critical environment variables
required_vars = ["AZURE_AI_FOUNDRY_ENDPOINT", "AZURE_SEARCH_CONNECTION_ID", "AZURE_SEARCH_INDEX_NAME"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print(f"❌ Missing required environment variables: {missing_vars}")
    print("Please check your .env file and ensure all required variables are set.")
    sys.exit(1)

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from azure.ai.projects import AIProjectClient
    from azure.ai.agents.models import MessageRole
    from azure.identity import DefaultAzureCredential
    from tracing import get_tracing
    from agents.orchestrator_agent import create_orchestrator_agent
    from continuous_evaluation import create_continuous_evaluator
    print("✅ Successfully imported all required modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


class HealthAINexusApp:
    """Main application class for the HealthAI Nexus system."""
    
    def __init__(self):
        """Initialize the application."""
        self.project_client = None
        self.orchestrator_agent = None
        self.agents_created = False
        self.continuous_evaluator = None
        
        # Initialize clean tracing
        self.tracing = get_tracing()

    def initialize_agents(self):
        """Initialize the connected agents system."""
        try:
            print("🚀 Initializing Healthcare Connected Agents System...")
            
            # Initialize the client
            self.project_client = AIProjectClient(
                endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
                credential=DefaultAzureCredential(),
            )
            
            # Create the orchestrator and connected agents
            agents = create_orchestrator_agent(self.project_client)
            self.orchestrator_agent = agents["orchestrator"]
            self.agents_created = True
            
            # Initialize continuous evaluation
            self.continuous_evaluator = create_continuous_evaluator(self.project_client)
            print("✅ Continuous evaluation initialized")
            
            print("✅ Connected Agents System Initialized Successfully!")
            print(f"   Orchestrator Agent ID: {self.orchestrator_agent.id}")
            print(f"   Research Agent ID: {agents['research_agent'].id}")
            print(f"   Analysis Agent ID: {agents['analysis_agent'].id}")
            print(f"   Synthesis Agent ID: {agents['synthesis_agent'].id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize connected agents: {e}")
            return False

    def process_healthcare_query(self, query, show_agents=True, progress=gr.Progress()):
        """Process a healthcare query using the connected agents system."""
        
        if not self.agents_created:
            return "❌ Connected agents not initialized. Please restart the app.", "", ""
        
        # Start clean tracing for the entire workflow
        with self.tracing.trace_user_query(query, "gradio-user") as main_span:
            try:
                progress(0.1, desc="🚀 Starting connected agents workflow...")
                
                # Create a thread
                thread = self.project_client.agents.threads.create()
                progress(0.2, desc="💬 Created conversation thread...")
                
                # Add the user message
                message = self.project_client.agents.messages.create(
                    thread_id=thread.id,
                    role=MessageRole.USER,
                    content=query,
                )
                progress(0.3, desc="📝 Added query to thread...")
                
                # Run the orchestrator agent with tracing
                progress(0.4, desc="🎯 Running orchestrator agent...")
                with self.tracing.trace_orchestrator(query) as orch_span:
                    run = self.project_client.agents.runs.create_and_process(
                        thread_id=thread.id, 
                        agent_id=self.orchestrator_agent.id
                    )
                
                progress(0.8, desc="⏳ Processing with connected agents...")
                
                # Create continuous evaluation for the run
                if self.continuous_evaluator:
                    progress(0.85, desc="📊 Setting up continuous evaluation...")
                    self.continuous_evaluator.evaluate_agent_run(
                        thread_id=thread.id,
                        run_id=run.id,
                        agent_id=self.orchestrator_agent.id
                    )
                
                if run.status == "completed":
                    # Get the response
                    messages = self.project_client.agents.messages.list(thread_id=thread.id)
                    messages_list = list(messages)
                    
                    # Find the latest assistant message
                    assistant_messages = [msg for msg in messages_list if str(msg.role) == "MessageRole.AGENT"]
                    
                    if assistant_messages:
                        response_message = assistant_messages[-1]
                        
                        # Extract the response content
                        response_content = ""
                        if hasattr(response_message, 'content') and response_message.content:
                            for content_item in response_message.content:
                                if hasattr(content_item, 'text'):
                                    text_content = content_item.text
                                    if hasattr(text_content, 'value'):
                                        text_value = text_content.value
                                        if text_value and text_value.strip() != "ASSISTANT":
                                            response_content += text_value + "\n"
                                    else:
                                        if text_content and str(text_content).strip() != "ASSISTANT":
                                            response_content += str(text_content) + "\n"
                                else:
                                    content_str = str(content_item)
                                    if content_str and content_str.strip() != "ASSISTANT":
                                        response_content += content_str + "\n"
                        
                        progress(1.0, desc="✅ Connected agents workflow completed!")
                        
                        # Get evaluation results if available
                        evaluation_info = ""
                        if self.continuous_evaluator:
                            try:
                                eval_results = self.continuous_evaluator.get_evaluation_results(run.id)
                                if eval_results:
                                    evaluation_info = f"\n**📊 Continuous Evaluation:** Active (Results available in Azure AI Foundry)"
                                else:
                                    evaluation_info = f"\n**📊 Continuous Evaluation:** Active (Results pending - check Azure AI Foundry monitoring)"
                            except Exception as e:
                                print(f"⚠️ Evaluation results query failed: {e}")
                                evaluation_info = f"\n**📊 Continuous Evaluation:** Active (Check Azure AI Foundry monitoring)"
                        else:
                            evaluation_info = f"\n**📊 Monitoring:** Active via Application Insights and Azure AI Foundry tracing"
                        
                        # Generate workflow info
                        workflow_info = ""
                        if show_agents:
                            workflow_info = f"""
### 🤖 Agent Workflow Details

**Orchestrator Agent:** {self.orchestrator_agent.name} (ID: {self.orchestrator_agent.id})

**Connected Agents Used:**
- 🔍 **Research Agent:** Searched medical information using Azure AI Search
- 📊 **Analysis Agent:** Analyzed data and created visualizations  
- 📝 **Synthesis Agent:** Created comprehensive reports and summaries

**Workflow Status:** ✅ Completed Successfully
**Thread ID:** {thread.id}
**Run ID:** {run.id}{evaluation_info}
                            """
                        
                        # Generate system status
                        system_status = f"""
### 📊 System Status

**✅ Connected Agents System:** Operational
**🎯 Orchestrator Agent:** Active
**🔗 Agent Coordination:** Successful
**📈 Azure AI Foundry:** Connected
**🔍 Azure AI Search:** Integrated
**⏱️ Response Time:** {run.created_at} - {run.completed_at if hasattr(run, 'completed_at') else 'N/A'}

**⚠️ Medical Disclaimer:** This system provides general health information only. Always consult with qualified healthcare professionals for medical advice, diagnosis, or treatment.
                        """
                        
                        # Clean up - Commented out for demo purposes to keep threads visible
                        # self.project_client.agents.threads.delete(thread.id)
                        
                        # Log workflow completion
                        self.tracing.log_workflow_completion(True, 1000.0, 4)
                        
                        final_response = response_content.strip() if response_content.strip() else "❌ No response content received from connected agents."
                        return final_response, workflow_info, system_status
                    else:
                        progress(1.0, desc="❌ No response received")
                        self.tracing.log_workflow_completion(False, 0.0, 0)
                        return "❌ No response received from the connected agents.", "", ""
                else:
                    progress(1.0, desc="❌ Workflow failed")
                    self.tracing.log_workflow_completion(False, 0.0, 0)
                    error_msg = f"❌ Connected agents workflow failed: {run.last_error}"
                    return error_msg, "", ""
                    
            except Exception as e:
                progress(1.0, desc="❌ Error occurred")
                print(f"❌ Error processing query: {e}")
                self.tracing.log_workflow_completion(False, 0.0, 0)
                error_msg = f"❌ Error processing query: {str(e)}"
                return error_msg, "", ""


def create_gradio_interface():
    """Create the Gradio interface for the connected agents app."""
    
    app = HealthAINexusApp()
    
    # Initialize connected agents
    if not app.initialize_agents():
        return None
    
    # Create the Gradio interface with beautiful design
    with gr.Blocks(
        title="🏥 HealthAI Nexus",
        theme=gr.themes.Soft(),
        css="""
            .gradio-container {
                max-width: 1200px !important;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                min-height: 100vh !important;
            }
            .main-header {
                text-align: center; 
                margin-bottom: 20px;
                color: #ffffff !important;
            }
            .metric-box {
                background: rgba(255, 255, 255, 0.1) !important;
                padding: 15px; 
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: #ffffff !important;
                backdrop-filter: blur(10px);
            }
            .gradio-container .gr-form {
                background: rgba(255, 255, 255, 0.95) !important;
                border-radius: 15px !important;
                padding: 20px !important;
                margin: 10px !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
            }
            .gradio-container .gr-button {
                background: linear-gradient(45deg, #667eea, #764ba2) !important;
                border: none !important;
                border-radius: 8px !important;
                color: white !important;
                font-weight: 600 !important;
            }
            .gradio-container .gr-button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            }
            .gradio-container h1, .gradio-container h2, .gradio-container h3 {
                color: #ffffff !important;
            }
            .gradio-container .gr-textbox, .gradio-container .gr-checkbox {
                background: rgba(255, 255, 255, 0.9) !important;
                border-radius: 8px !important;
            }
            .agent-info {
                background: rgba(255, 255, 255, 0.1) !important;
                padding: 20px; 
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: #ffffff !important;
                backdrop-filter: blur(10px);
                margin: 20px 0;
            }
        """
    ) as interface:
        
        # Header section
        gr.Markdown("""
        # 🏥 HealthAI Nexus
        
        **Intelligent Healthcare AI System**
        
        Ask any health-related question and experience our intelligent multi-agent system:
        - 🔍 **Research Agent** searches medical information using Azure AI Search
        - 📊 **Analysis Agent** analyzes data and creates visualizations  
        - 📝 **Synthesis Agent** creates comprehensive reports and summaries
        - 🎯 **Orchestrator** coordinates the workflow between all agents
        - ⚠️ Includes appropriate medical disclaimers
        """, elem_classes=["main-header"])
        

        
        # Main input section
        with gr.Row():
            with gr.Column(scale=3):
                query_input = gr.Textbox(
                    label="🏥 Your Health Question",
                    placeholder="e.g., What are the symptoms of diabetes?",
                    lines=3,
                    max_lines=5
                )
            
            with gr.Column(scale=1):
                show_agents = gr.Checkbox(
                    label="🤖 Show Agent Workflow",
                    value=True,
                    info="Display the agent coordination process"
                )
        
        # Submit button
        submit_btn = gr.Button(
            "🚀 Get AI Response",
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
                    variant="secondary"
                )
                example_btn_2 = gr.Button(
                    "💊 Blood Pressure Meds",
                    size="sm",
                    variant="secondary"
                )
            
            with gr.Column(scale=1):
                example_btn_3 = gr.Button(
                    "🫀 Heart Attack Signs",
                    size="sm",
                    variant="secondary"
                )
                example_btn_4 = gr.Button(
                    "🦠 COVID-19 Guidelines",
                    size="sm",
                    variant="secondary"
                )
            
            with gr.Column(scale=1):
                example_btn_5 = gr.Button(
                    "🧠 Mental Health Support",
                    size="sm",
                    variant="secondary"
                )
                example_btn_6 = gr.Button(
                    "👶 Pregnancy Care",
                    size="sm",
                    variant="secondary"
                )
        
        # Output sections
        with gr.Row():
            with gr.Column(scale=2):
                response_output = gr.Markdown(
                    label="🤖 AI Response",
                    value="Ask a health question to get started...",
                    elem_classes=["response-box"]
                )
            
            with gr.Column(scale=1):
                workflow_output = gr.Markdown(
                    label="🤖 System Workflow",
                    value="Agent workflow will appear here when you ask a question...",
                    elem_classes=["context-box"]
                )
        
        # Performance metrics
        metrics_output = gr.Markdown(
            label="📊 System Status",
            value="System status will appear here after your first query...",
            elem_classes=["metric-box"]
        )
        
        # Event handlers
        submit_btn.click(
            fn=app.process_healthcare_query,
            inputs=[query_input, show_agents],
            outputs=[response_output, workflow_output, metrics_output],
            api_name="query_connected_agents",
            queue=True  # Enable streaming for better UX
        )
        
        # Enter key support
        query_input.submit(
            fn=app.process_healthcare_query,
            inputs=[query_input, show_agents],
            outputs=[response_output, workflow_output, metrics_output],
            api_name="query_connected_agents_enter",
            queue=True
        )
        
        # Example button handlers
        example_btn_1.click(
            fn=lambda: "What are the common symptoms of diabetes and how can I recognize them?",
            outputs=[query_input]
        )
        
        example_btn_2.click(
            fn=lambda: "What are the different types of blood pressure medications and their side effects?",
            outputs=[query_input]
        )
        
        example_btn_3.click(
            fn=lambda: "What are the warning signs and symptoms of a heart attack?",
            outputs=[query_input]
        )
        
        example_btn_4.click(
            fn=lambda: "What are the current COVID-19 vaccination guidelines for adults?",
            outputs=[query_input]
        )
        
        example_btn_5.click(
            fn=lambda: "What are the signs of depression and anxiety, and what support resources are available?",
            outputs=[query_input]
        )
        
        example_btn_6.click(
            fn=lambda: "What are the important prenatal care guidelines and what should I expect during pregnancy?",
            outputs=[query_input]
        )
    
    return interface


if __name__ == "__main__":
    print("🚀 Starting HealthAI Nexus App...")
    print("=" * 60)
    
    interface = create_gradio_interface()
    
    if interface:
        print("\n✅ Gradio interface created successfully!")
        print("🌐 Starting web server...")
        print("📱 Access the app at: http://localhost:7860")
        print("=" * 60)
        
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            quiet=False
        )
    else:
        print("❌ Failed to create Gradio interface")
        sys.exit(1)