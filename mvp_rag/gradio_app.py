#!/usr/bin/env python3
"""
Gradio UI for MVP RAG Healthcare AI Assistant

This creates a beautiful, interactive web interface for
demonstrating the RAG system with Ollama + Qdrant.
"""

import gradio as gr
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from core.rag_engine import RAGEngine
from utils.logger import get_logger

logger = get_logger("gradio_app")

class GradioRAGInterface:
    """Gradio interface for the MVP RAG system."""
    
    def __init__(self):
        """Initialize the Gradio interface."""
        self.rag_engine = None
        self.logger = logger
        self.setup_rag_engine()
    
    def setup_rag_engine(self):
        """Setup the RAG engine."""
        try:
            self.rag_engine = RAGEngine()
            self.logger.info("RAG Engine initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize RAG Engine: {e}")
            self.rag_engine = None
    
    def query_rag(self, question: str, show_context: bool = False) -> tuple:
        """
        Process a query through the RAG system.
        
        Args:
            question: User's health question
            show_context: Whether to show retrieved context
            
        Returns:
            Tuple of (response, context, metrics)
        """
        if not self.rag_engine:
            return (
                "❌ RAG Engine not available. Please check Ollama and Qdrant services.",
                "System Error",
                "Service Unavailable"
            )
        
        try:
            # Process the query
            result = self.rag_engine.query(question)
            
            # Format response
            response = result['response']
            
            # Format context
            if show_context and result['context']['retrieved_documents']:
                context_parts = []
                for i, doc in enumerate(result['context']['retrieved_documents'], 1):
                    score = doc.get('score', 0)
                    source = doc.get('source', 'Unknown')
                    content = doc.get('content', '')[:200] + "..." if len(doc.get('content', '')) > 200 else doc.get('content', '')
                    
                    context_parts.append(f"**Document {i}** (Score: {score:.3f}, Source: {source})\n{content}\n")
                
                context = "\n".join(context_parts)
            else:
                context = result['context']['context_summary']
            
            # Format metrics
            metrics = result['metrics']
            metrics_text = f"""
**Performance Metrics:**
• Total Time: {metrics['total_time_ms']}ms
• Embedding Time: {metrics['embedding_time_ms']}ms  
• Search Time: {metrics['search_time_ms']}ms
• Generation Time: {metrics['generation_time_ms']}ms
• Documents Retrieved: {metrics['documents_retrieved']}
• Average Similarity Score: {metrics['average_similarity_score']}
• LLM Model: {metrics['llm_model']}
• Embedding Model: {metrics['embedding_model']}
            """
            
            return response, context, metrics_text
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return (
                f"❌ Error processing your question: {str(e)}",
                "Error occurred during processing",
                "Processing failed"
            )
    
    def health_check(self) -> str:
        """Check system health."""
        if not self.rag_engine:
            return "❌ RAG Engine not available"
        
        try:
            health = self.rag_engine.health_check()
            system_info = self.rag_engine._get_system_info()
            
            health_text = f"""
**🏥 System Health Check:**
• Ollama: {'✅ Healthy' if health['ollama'] else '❌ Unhealthy'}
• Qdrant: {'✅ Healthy' if health['qdrant'] else '❌ Unhealthy'}
• Overall: {'✅ Healthy' if health['overall'] else '❌ Unhealthy'}

**📊 System Information:**
• RAG Engine: {system_info['rag_engine']}
• LLM Model: {system_info['llm_model']}
• Embedding Model: {system_info['embedding_model']}
• Vector Store: {system_info['vector_store']}

**🗄️ Collection Info:**
• Collection: {system_info['collection_info'].get('name', 'Unknown')}
• Documents: {system_info['collection_info'].get('points_count', 'Unknown')}
• Vector Size: {system_info['collection_info'].get('vector_size', 'Unknown')}
            """
            
            return health_text
            
        except Exception as e:
            return f"❌ Health check failed: {str(e)}"
    
    def create_interface(self) -> gr.Interface:
        """Create the Gradio interface."""
        
        # Custom CSS for better styling
        css = """
        .gradio-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        .health-check-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .metrics-box {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        """
        
        with gr.Blocks(css=css, title="MVP RAG Healthcare AI Assistant") as interface:
            gr.Markdown("""
            # 🏥 MVP RAG Healthcare AI Assistant
            ## 🚀 Real RAG with Local AI Tools: Ollama + Qdrant
            
            This demonstrates a production-ready RAG system using local AI tools before evolving to Azure services.
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Main query interface
                    gr.Markdown("### 💬 Ask a Health Question")
                    question_input = gr.Textbox(
                        label="Your Health Question",
                        placeholder="e.g., What are the symptoms of diabetes?",
                        lines=3
                    )
                    
                    with gr.Row():
                        submit_btn = gr.Button("🔍 Ask Question", variant="primary", size="lg")
                        health_btn = gr.Button("🏥 System Health", variant="secondary")
                    
                    show_context = gr.Checkbox(label="Show Retrieved Context", value=True)
                    
                with gr.Column(scale=1):
                    # System info
                    gr.Markdown("### 📊 System Status")
                    system_status = gr.Markdown("Click 'System Health' to check status")
            
            # Response area
            gr.Markdown("### 📝 AI Response")
            response_output = gr.Textbox(label="Response", lines=8, interactive=False)
            
            # Context area
            gr.Markdown("### 📚 Retrieved Context")
            context_output = gr.Markdown(label="Context")
            
            # Metrics area
            gr.Markdown("### 📈 Performance Metrics")
            metrics_output = gr.Markdown(label="Metrics")
            
            # Demo queries
            gr.Markdown("### 💡 Sample Questions")
            demo_queries = [
                "What are the symptoms of diabetes?",
                "How do I check my blood pressure at home?",
                "What should I do if I have chest pain?",
                "How do I manage stress and anxiety?",
                "What are the benefits of regular exercise?"
            ]
            
            demo_buttons = gr.Row()
            for query in demo_queries:
                demo_buttons.add(gr.Button(query, size="sm"))
            
            # Event handlers
            submit_btn.click(
                fn=self.query_rag,
                inputs=[question_input, show_context],
                outputs=[response_output, context_output, metrics_output]
            )
            
            health_btn.click(
                fn=self.health_check,
                outputs=system_status
            )
            
            # Demo query handlers
            for i, query in enumerate(demo_queries):
                demo_buttons.children[i].click(
                    fn=lambda q=query: (q, "", "", ""),
                    outputs=[question_input, response_output, context_output, metrics_output]
                )
            
            # Footer
            gr.Markdown("""
            ---
            **🎯 What This Demonstrates:**
            - ✅ Real RAG with local AI tools
            - ✅ Semantic search with embeddings  
            - ✅ Dynamic LLM responses
            - ✅ Performance metrics and monitoring
            
            **🚀 Next Steps to Production:**
            - 🔄 Replace Ollama with Azure OpenAI
            - 🔄 Replace Qdrant with Azure AI Search
            - 🔄 Add Content Safety and compliance
            - 🔄 Add agentic workflow and tools
            """)
        
        return interface

def main():
    """Main function to launch the Gradio app."""
    print("🚀 Launching MVP RAG Healthcare AI Assistant with Gradio...")
    
    try:
        interface = GradioRAGInterface()
        app = interface.create_interface()
        
        # Launch the app
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,  # Set to True if you want a public link
            show_error=True
        )
        
    except Exception as e:
        print(f"❌ Failed to launch Gradio app: {e}")
        print("Please ensure all dependencies are installed and services are running.")

if __name__ == "__main__":
    main()
