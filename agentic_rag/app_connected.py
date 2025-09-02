#!/usr/bin/env python3
"""
🏥 Healthcare Agentic RAG System - Connected Agents Version

This version uses Azure AI Foundry Connected Agents instead of Python coordination.
The Research Agent orchestrates the entire workflow by calling Analysis and Synthesis agents directly.
"""

import gradio as gr
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agents.connected_research_agent import create_connected_research_agent
    from monitoring import setup_monitoring
    print("✅ Successfully imported connected agents and monitoring modules")
    
    # Initialize Azure AI Foundry monitoring
    monitor = setup_monitoring()
    monitor.set_application_context("healthcare-agentic-rag-connected")
    print("✅ Azure AI Foundry monitoring initialized for connected agents")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class ConnectedHealthcareInterface:
    """Connected Healthcare Agentic RAG Interface using Azure AI Foundry Connected Agents."""
    
    def __init__(self):
        """Initialize the connected healthcare interface."""
        self.research_agent = None
        self.initialize_connected_agents()
        print("✅ Connected healthcare interface initialized successfully")
    
    def initialize_connected_agents(self):
        """Initialize the connected research agent (which orchestrates the workflow)."""
        try:
            print("🚀 Initializing connected agents...")
            self.research_agent, _ = create_connected_research_agent()
            print("✅ Connected agents initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing connected agents: {e}")
            raise
    
    def process_healthcare_query(self, query: str, progress=gr.Progress()):
        """
        Process a healthcare query using connected agents.
        
        The Research Agent orchestrates the entire workflow by:
        1. Searching healthcare documents
        2. Calling Analysis Agent for data analysis
        3. Calling Synthesis Agent for patient-friendly response
        4. Combining all results
        """
        if not query.strip():
            return "Please enter a healthcare question."
        
        try:
            progress(0.1, desc="🚀 Starting connected agent workflow...")
            
            # Import here to avoid circular imports
            from azure.ai.projects import AIProjectClient
            from azure.ai.agents.models import MessageRole
            from azure.identity import DefaultAzureCredential
            
            # Initialize client
            project_client = AIProjectClient(
                endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
                credential=DefaultAzureCredential(
                    exclude_environment_credential=True,
                    exclude_managed_identity_credential=True
                )
            )
            
            progress(0.2, desc="🔍 Creating conversation thread...")
            
            # Create a new thread for this conversation
            thread = project_client.agents.threads.create()
            
            progress(0.3, desc="📝 Sending query to Research Agent...")
            
            # Send the query to the Research Agent (which will orchestrate the workflow)
            message = project_client.agents.messages.create(
                thread_id=thread.id,
                role=MessageRole.USER,
                content=query,
            )
            
            progress(0.4, desc="🔄 Research Agent coordinating with Analysis and Synthesis agents...")
            
            # Run the Research Agent (this will coordinate with Analysis and Synthesis agents)
            run = project_client.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=self.research_agent.id
            )
            
            progress(0.8, desc="⏳ Processing multi-agent workflow...")
            
            # Monitor the run
            while run.status in ["queued", "in_progress"]:
                run = project_client.agents.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                progress(0.8, desc=f"⏳ Multi-agent workflow status: {run.status}")
            
            progress(0.9, desc="📋 Retrieving comprehensive response...")
            
            if run.status == "completed":
                # Get the final response
                messages = project_client.agents.messages.list(thread_id=thread.id)
                messages_list = list(messages)
                
                # Find the latest assistant message
                assistant_messages = [msg for msg in messages_list if msg.role == MessageRole.ASSISTANT]
                
                if assistant_messages:
                    response_message = assistant_messages[-1]
                    
                    # Extract the response content
                    response_content = ""
                    if hasattr(response_message, 'content') and response_message.content:
                        for content_item in response_message.content:
                            if hasattr(content_item, 'text'):
                                response_content += content_item.text + "\n"
                            else:
                                response_content += str(content_item) + "\n"
                    else:
                        response_content = str(response_message.content)
                    
                    progress(1.0, desc="✅ Connected agent workflow completed!")
                    
                    # Clean up the thread
                    project_client.agents.threads.delete(thread.id)
                    
                    return response_content.strip()
                else:
                    return "❌ No response received from the connected agents."
            else:
                return f"❌ Connected agent workflow failed: {run.last_error}"
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return f"❌ Error processing query: {str(e)}"

def create_connected_interface():
    """Create the connected healthcare interface."""
    
    # Create the interface
    interface = ConnectedHealthcareInterface()
    
    # Create the Gradio interface
    with gr.Blocks(
        title="🏥 Healthcare Agentic RAG - Connected Agents",
        theme=gr.themes.Soft(primary_hue="blue"),
        css="""
        .gradio-container {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        }
        .main-header {
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        }
        .description {
            color: #e0e0e0;
            text-align: center;
            margin-bottom: 2rem;
        }
        """
    ) as demo:
        
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>🏥 Healthcare Agentic RAG System</h1>
            <h2>Connected Agents Version</h2>
        </div>
        <div class="description">
            <p>Ask healthcare questions and get comprehensive responses from our connected AI agents.</p>
            <p><strong>Architecture:</strong> Research Agent → Analysis Agent + Synthesis Agent (Connected Workflow)</p>
            <p><strong>Features:</strong> Azure AI Search + Code Interpreter + Agent Communication</p>
        </div>
        """)
        
        # Main interface
        with gr.Row():
            with gr.Column(scale=3):
                query_input = gr.Textbox(
                    label="🏥 Healthcare Question",
                    placeholder="Ask about symptoms, treatments, medications, or health conditions...",
                    lines=3,
                    max_lines=5
                )
                
                submit_btn = gr.Button(
                    "🔍 Get Healthcare Response",
                    variant="primary",
                    size="lg"
                )
                
                # Example queries
                gr.Examples(
                    examples=[
                        "What are the symptoms of diabetes and how is it treated?",
                        "Explain the difference between Type 1 and Type 2 diabetes",
                        "What are the side effects of metformin?",
                        "How do I manage high blood pressure?",
                        "What are the warning signs of a heart attack?",
                        "How is hypertension diagnosed and treated?"
                    ],
                    inputs=query_input,
                    label="💡 Example Questions"
                )
            
            with gr.Column(scale=7):
                response_output = gr.Markdown(
                    label="📋 Healthcare Response",
                    value="Ask a healthcare question to get a comprehensive response from our connected AI agents.",
                    show_copy_button=True
                )
        
        # Event handlers
        submit_btn.click(
            fn=interface.process_healthcare_query,
            inputs=[query_input],
            outputs=[response_output],
            show_progress=True
        )
        
        query_input.submit(
            fn=interface.process_healthcare_query,
            inputs=[query_input],
            outputs=[response_output],
            show_progress=True
        )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; color: #e0e0e0; margin-top: 2rem;">
            <p><strong>Connected Agents Architecture:</strong></p>
            <p>🔍 Research Agent (Orchestrator) → 📊 Analysis Agent + 📝 Synthesis Agent</p>
            <p>Powered by Azure AI Foundry Connected Agents</p>
        </div>
        """)
    
    return demo

if __name__ == "__main__":
    print("🏥 Starting Healthcare Agentic RAG System - Connected Agents Version")
    print("=" * 70)
    
    try:
        # Create and launch the interface
        demo = create_connected_interface()
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your Azure AI Foundry configuration.")
