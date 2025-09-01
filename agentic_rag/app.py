#!/usr/bin/env python3
"""
Simplified Healthcare Agentic RAG System for testing.
"""

import gradio as gr
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agents.coordinator_agent import execute_multi_agent_workflow
    from monitoring import setup_monitoring
    print("✅ Successfully imported coordinator and monitoring modules")
    
    # Initialize Azure AI Foundry monitoring
    monitor = setup_monitoring()
    monitor.set_application_context("healthcare-agentic-rag")
    print("✅ Azure AI Foundry monitoring initialized with application context")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class SimpleHealthcareInterface:
    """Simplified Healthcare Agentic RAG Interface."""
    
    def __init__(self):
        """Initialize the interface."""
        print("✅ Simple healthcare interface initialized successfully")
    
    def create_interface(self):
        """Create the simplified Gradio interface."""
        
        with gr.Blocks(
            title="🏥 Healthcare Agentic RAG System",
            theme=gr.themes.Soft(),
            css="""
                .gradio-container {background: #1a202c !important;}
                .gr-interface {background: #1a202c !important;}
                .gr-panel {background: #2d3748 !important; border: 2px solid #4a5568 !important; border-radius: 15px !important;}
                .gr-textbox textarea, .gr-textbox input {color: #e2e8f0 !important; background: #1a202c !important; border: 2px solid #4a5568 !important;}
                .gr-button {background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important; color: white !important; border: none !important;}
                .gr-button:hover {background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important;}
                .gr-markdown {color: #e2e8f0 !important;}
                .gr-markdown h1, .gr-markdown h2, .gr-markdown h3 {color: #48bb78 !important;}
                .gr-html {background: #1a202c !important; border: 2px solid #4a5568 !important; border-radius: 10px !important; padding: 15px !important;}
            """
        ) as app:
            
            gr.Markdown("""
            # 🏥 Healthcare Agentic RAG System
            
            **Multi-Agent AI System for Healthcare Information**
            
            This system uses **4 specialized AI agents** working together to provide comprehensive healthcare responses:
            
            🔍 **Research Agent** - Searches Azure AI Search for relevant medical documents and extracts key information with sources  
            📊 **Analysis Agent** - Uses Code Interpreter to analyze data, create visualizations, and identify patterns  
            📝 **Synthesis Agent** - Generates patient-friendly healthcare responses by combining research and analysis  
            🎯 **Coordinator Agent** - Orchestrates the complete workflow: Research → Analysis → Synthesis → Final Response  
            
            **🔍 All traces are automatically sent to Azure Application Insights**
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    query_input = gr.Textbox(
                        label="Health Question",
                        placeholder="Ask a healthcare question...",
                        lines=3
                    )
                    
                    submit_btn = gr.Button("Submit", variant="primary")
                
                with gr.Column(scale=1):
                    gr.Markdown("### Example Questions:")
                    example_btn_1 = gr.Button("🩺 Diabetes Symptoms", size="sm")
                    example_btn_2 = gr.Button("💊 Blood Pressure", size="sm")
                    example_btn_3 = gr.Button("🫀 Heart Disease", size="sm")
            
            # Progress indicator
            progress_bar = gr.Progress()
            
            # Status display
            status_display = gr.HTML(
                label="Workflow Status",
                value="<div style='color: #e2e8f0; background: #2d3748; padding: 15px; border-radius: 10px; text-align: center;'>Ready to process your healthcare question</div>"
            )
            
            # Main output
            output = gr.HTML(
                label="Multi-Agent Response",
                value="<div style='color: #e2e8f0; background: #2d3748; padding: 20px; border-radius: 10px;'>Submit a health question to see the multi-agent workflow in action!</div>"
            )
            
            # Event handlers
            def process_query(query, progress=gr.Progress()):
                if not query.strip():
                    return (
                        "<div style='color: #e2e8f0; background: #2d3748; padding: 20px; border-radius: 10px;'>Please enter a health question.</div>",
                        "<div style='color: #f56565; background: #2d3748; padding: 15px; border-radius: 10px; text-align: center;'>No query provided</div>"
                    )
                
                try:
                    # Update status
                    status_html = "<div style='color: #4299e1; background: #2d3748; padding: 15px; border-radius: 10px; text-align: center;'>🚀 Starting multi-agent workflow...</div>"
                    
                    # Execute the multi-agent workflow with progress updates
                    progress(0.1, desc="Initializing agents...")
                    
                    def progress_callback(message):
                        progress(0.3, desc=message)
                        return message
                    
                    result = execute_multi_agent_workflow(query, progress_callback)
                    
                    progress(1.0, desc="Workflow completed!")
                    
                    # Format the response with detailed agent information
                    research_content = result.get('research', {}).get('content', 'No research data')
                    analysis_content = result.get('analysis', {}).get('content', 'No analysis data')
                    synthesis_content = result.get('synthesis', {}).get('content', 'No synthesis data')
                    
                    # Clean and format the content for better display
                    def format_content(content, max_length=800):
                        if not content or content == 'No research data' or content == 'No analysis data' or content == 'No synthesis data':
                            return content
                        
                        # Clean up any JSON artifacts or formatting issues
                        content = str(content).strip()
                        
                        # If it's too long, truncate and add ellipsis
                        if len(content) > max_length:
                            content = content[:max_length] + "..."
                        
                        return content
                    
                    research_formatted = format_content(research_content)
                    analysis_formatted = format_content(analysis_content)
                    synthesis_formatted = format_content(synthesis_content, 2000)  # Allow longer synthesis
                    
                    response_html = f"""
                    <div style='padding: 20px; background: #2d3748; border-radius: 10px; color: #e2e8f0;'>
                        <h3 style='color: #48bb78; margin-bottom: 20px;'>🏥 Multi-Agent Healthcare Response</h3>
                        <div style='background: #1a202c; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #48bb78;'>
                            <p style='margin: 0; font-size: 1.1em;'><strong>Query:</strong> {query}</p>
                        </div>
                        
                        <div style='margin: 25px 0;'>
                            <h4 style='color: #4299e1; margin-bottom: 10px; display: flex; align-items: center;'>
                                🔍 Research Agent Results
                                <span style='margin-left: 10px; font-size: 0.8em; color: #718096;'>(Medical Document Search)</span>
                            </h4>
                            <div style='background: #1a202c; padding: 20px; border-radius: 8px; color: #e2e8f0; border: 1px solid #4a5568; max-height: 250px; overflow-y: auto; line-height: 1.6;'>
                                <div style='white-space: pre-wrap; font-family: "Segoe UI", sans-serif;'>{research_formatted}</div>
                            </div>
                        </div>
                        
                        <div style='margin: 25px 0;'>
                            <h4 style='color: #ed8936; margin-bottom: 10px; display: flex; align-items: center;'>
                                📊 Analysis Agent Results
                                <span style='margin-left: 10px; font-size: 0.8em; color: #718096;'>(Data Analysis & Insights)</span>
                            </h4>
                            <div style='background: #1a202c; padding: 20px; border-radius: 8px; color: #e2e8f0; border: 1px solid #4a5568; max-height: 250px; overflow-y: auto; line-height: 1.6;'>
                                <div style='white-space: pre-wrap; font-family: "Segoe UI", sans-serif;'>{analysis_formatted}</div>
                            </div>
                        </div>
                        
                        <div style='margin: 25px 0;'>
                            <h4 style='color: #48bb78; margin-bottom: 10px; display: flex; align-items: center;'>
                                📝 Final Synthesis
                                <span style='margin-left: 10px; font-size: 0.8em; color: #718096;'>(Patient-Friendly Response)</span>
                            </h4>
                            <div style='background: #1a202c; padding: 20px; border-radius: 8px; color: #e2e8f0; border: 1px solid #4a5568; line-height: 1.6;'>
                                <div style='white-space: pre-wrap; font-family: "Segoe UI", sans-serif;'>{synthesis_formatted}</div>
                            </div>
                        </div>
                        
                        <div style='margin-top: 25px; padding: 20px; background: #1a202c; border-radius: 8px; border: 1px solid #4a5568;'>
                            <h4 style='color: #48bb78; margin-bottom: 15px;'>📊 Workflow Summary</h4>
                            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'>
                                <div>
                                    <p style='margin: 5px 0;'><strong>Status:</strong> <span style='color: #48bb78;'>{result.get('summary', {}).get('workflow_status', 'Unknown')}</span></p>
                                    <p style='margin: 5px 0;'><strong>Execution Time:</strong> <span style='color: #4299e1;'>{result.get('summary', {}).get('execution_time', 'N/A')}s</span></p>
                                </div>
                                <div>
                                    <p style='margin: 5px 0;'><strong>Successful Agents:</strong> <span style='color: #48bb78;'>{result.get('summary', {}).get('successful_agents', 'N/A')}/{result.get('summary', {}).get('total_agents', 'N/A')}</span></p>
                                    <p style='margin: 5px 0;'><strong>Trace ID:</strong> <span style='color: #718096; font-family: monospace; font-size: 0.9em;'>{result.get('summary', {}).get('trace_id', 'N/A')}</span></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    """
                    
                    # Update status to completed
                    final_status = f"<div style='color: #48bb78; background: #2d3748; padding: 15px; border-radius: 10px; text-align: center;'>✅ Workflow completed successfully! Execution time: {result.get('summary', {}).get('execution_time', 'N/A')}s</div>"
                    
                    return response_html, final_status
                    
                except Exception as e:
                    error_response = f"<div style='color: #f56565; background: #2d3748; padding: 20px; border-radius: 10px;'>Error: {str(e)}</div>"
                    error_status = f"<div style='color: #f56565; background: #2d3748; padding: 15px; border-radius: 10px; text-align: center;'>❌ Workflow failed: {str(e)}</div>"
                    return error_response, error_status
            
            # Connect the submit button
            submit_btn.click(
                process_query,
                inputs=query_input,
                outputs=[output, status_display]
            )
            
            # Connect example buttons
            example_btn_1.click(lambda: "What are the symptoms of diabetes?", outputs=query_input)
            example_btn_2.click(lambda: "How can I manage high blood pressure?", outputs=query_input)
            example_btn_3.click(lambda: "What are the risk factors for heart disease?", outputs=query_input)
        
        return app
    
    def launch(self):
        """Launch the interface."""
        app = self.create_interface()
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            quiet=False
        )

def main():
    """Main entry point."""
    try:
        interface = SimpleHealthcareInterface()
        interface.launch()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your Azure AI Foundry configuration.")

if __name__ == "__main__":
    main()
