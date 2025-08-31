#!/usr/bin/env python3
"""
🏥 MVP RAG Healthcare AI Assistant - Gradio Web Interface

This module creates a beautiful, interactive web interface for demonstrating
the RAG system with Ollama + Qdrant. It showcases:

- Real-time healthcare AI assistance
- Streaming responses for better UX
- Performance metrics and monitoring
- Context retrieval with citations
- Professional medical disclaimers
"""

import gradio as gr
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from core.rag_engine import RAGEngine
from utils.logger import get_logger

# Initialize logging for the Gradio interface
logger = get_logger("gradio_app")


class GradioRAGInterface:
    """
    Gradio interface for the MVP RAG Healthcare AI Assistant.
    
    This class handles:
    - Web UI creation and management
    - RAG engine integration
    - User interaction processing
    - Response formatting and display
    - Performance monitoring
    """
    
    def __init__(self):
        """Initialize the Gradio interface with RAG engine setup."""
        self.rag_engine = None
        self.logger = logger
        
        # Setup the RAG engine with healthcare-optimized models
        self.setup_rag_engine()
    
    def setup_rag_engine(self):
        """
        Initialize and configure the RAG engine.
        
        Sets up:
        - LLM client (qwen3:4b-instruct for generation)
        - Embedding client (nomic-embed-text for search)
        - Vector store (Qdrant for document retrieval)
        - Pre-warming for reduced latency
        """
        try:
            # Initialize RAG engine with optimized parameters
            self.rag_engine = RAGEngine(
                llm_model="qwen3:4b-instruct",      # Fast, accurate text generation
                embedding_model="nomic-embed-text"   # Efficient semantic embeddings
            )
            self.logger.info("✅ RAG Engine initialized successfully")
            
            # Pre-warm LLM to reduce first-response latency
            # This is crucial for demo presentations
            try:
                _ = self.rag_engine.llm_client.generate(
                    model=self.rag_engine.llm_model,
                    prompt="OK",
                    system="You are a helpful assistant.",
                    temperature=0.1,
                    max_tokens=5
                )
                self.logger.info("🔥 LLM pre-warmed successfully")
            except Exception as warm_err:
                self.logger.info(f"⚠️ Warm-up skipped: {warm_err}")
                
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize RAG Engine: {e}")
            self.rag_engine = None
    
    def query_rag(self, question: str, show_context: bool = False) -> tuple:
        """
        Process a user query through the RAG system.
        
        This is the main method that orchestrates:
        1. Query validation
        2. RAG processing
        3. Response formatting
        4. Context preparation
        5. Metrics collection
        
        Args:
            question: User's health-related question
            show_context: Whether to display retrieved documents
            
        Returns:
            Tuple of (formatted_response, context_display, metrics_summary)
        """
        # Validate RAG engine availability
        if not self.rag_engine:
            return (
                "❌ RAG Engine not available. Please check Ollama and Qdrant services.",
                "System Error",
                "Service Unavailable"
            )
        
        try:
            # Process the query through the RAG pipeline
            result = self.rag_engine.query(question)
            
            # Extract the main response
            response = result['response']
            
            # Debug logging to see what's happening
            self.logger.info(f"🔍 RAG Result: {result}")
            self.logger.info(f"🔍 Response: {response}")
            self.logger.info(f"🔍 Response type: {type(response)}")
            self.logger.info(f"🔍 Response length: {len(str(response)) if response else 0}")
            
            # Ensure response is not empty or None
            if not response or response.strip() == "":
                response = "❌ No response was generated. Please try again."
            
            # Format context display based on user preference
            if show_context and result['context']['retrieved_documents']:
                context = self._format_detailed_context(result['context']['retrieved_documents'])
            else:
                context = result['context']['context_summary']
            
            # Format performance metrics for display
            metrics_text = self._format_metrics(result['metrics'])
            
            return response, context, metrics_text
            
        except Exception as e:
            error_msg = f"❌ Error processing query: {str(e)}"
            self.logger.error(f"Query processing failed: {e}")
            return error_msg, "Error occurred", "Processing failed"
    
    def _format_detailed_context(self, documents: list) -> str:
        """
        Format retrieved documents for detailed context display.
        
        Args:
            documents: List of retrieved document dictionaries
            
        Returns:
            Formatted markdown string with document details and citations
        """
        context_parts = []
        
        # Format each retrieved document
        for i, doc in enumerate(documents, 1):
            score = doc.get('score', 0)
            source = doc.get('source', 'Unknown')
            
            # Truncate content for display (keep first 200 chars)
            content = doc.get('content', '')
            if len(content) > 200:
                content = content[:200] + "..."
            
            # Create formatted document entry
            doc_entry = f"**Document {i}** (Score: {score:.3f}, Source: {source})\n{content}\n"
            context_parts.append(doc_entry)
        
        # Add citations section
        citations = self._format_citations(documents[:3])  # Top 3 sources
        context_parts.append(citations)
        
        return "\n".join(context_parts)
    
    def _format_citations(self, documents: list) -> str:
        """
        Create a citations section for the response.
        
        Args:
            documents: List of documents to cite
            
        Returns:
            Formatted citations string
        """
        if not documents:
            return "\n**Citations:**\n- (none)"
        
        cites = []
        for doc in documents:
            title = doc.get('title') or (doc.get('source') or 'Source')
            source = doc.get('source', '')
            
            if source:
                cites.append(f"- {title} ({source})")
            else:
                cites.append(f"- {title}")
        
        return "\n**Citations:**\n" + "\n".join(cites)
    
    def _format_metrics(self, metrics: dict) -> str:
        """
        Format performance metrics for display.
        
        Args:
            metrics: Dictionary containing timing and performance data
            
        Returns:
            Formatted metrics string
        """
        return f"""
**Performance Metrics:**
• Total Time: {metrics['total_time_ms']}ms
• Embedding Time: {metrics['embedding_time_ms']}ms
• Search Time: {metrics['search_time_ms']}ms
• Generation Time: {metrics['generation_time_ms']}ms
• Documents Retrieved: {metrics['documents_retrieved']}
• Average Similarity Score: {metrics['avg_similarity_score']:.3f}
        """.strip()
    
    def create_interface(self) -> gr.Interface:
        """
        Create and configure the Gradio web interface.
        
        Returns:
            Configured Gradio interface ready for launch
        """
        # Create the main interface components
        with gr.Blocks(
            title="🏥 MVP RAG Healthcare AI Assistant",
            theme=gr.themes.Soft(),
            css="""
                .gradio-container {max-width: 1200px !important;}
                .main-header {text-align: center; margin-bottom: 20px;}
                .metric-box {background: #f0f8ff; padding: 10px; border-radius: 5px;}
            """
        ) as app:
            
            # Header section
            gr.Markdown("""
            # 🏥 MVP RAG Healthcare AI Assistant
            
            **Demonstrating AI Evolution: From Local MVP to Production-Ready Solutions**
            
            Ask any health-related question and see how our RAG system:
            - 🔍 Finds relevant medical information
            - 🤖 Generates accurate, helpful responses
            - 📊 Provides performance metrics
            - ⚠️ Includes appropriate medical disclaimers
            """, elem_classes=["main-header"])
            
            # Main input section
            with gr.Row():
                with gr.Column(scale=3):
                    question_input = gr.Textbox(
                        label="🏥 Your Health Question",
                        placeholder="e.g., What are the symptoms of diabetes?",
                        lines=3,
                        max_lines=5
                    )
                
                with gr.Column(scale=1):
                    show_context = gr.Checkbox(
                        label="📚 Show Retrieved Documents",
                        value=False,
                        info="Display the source documents used for the response"
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
                    context_output = gr.Markdown(
                        label="📚 Context & Sources",
                        value="Context will appear here when you ask a question...",
                        elem_classes=["context-box"]
                    )
            
            # Performance metrics
            metrics_output = gr.Markdown(
                label="📊 Performance Metrics",
                value="Metrics will appear here after your first query...",
                elem_classes=["metric-box"]
            )
            
            # Event handlers
            submit_btn.click(
                fn=self.query_rag,
                inputs=[question_input, show_context],
                outputs=[response_output, context_output, metrics_output],
                api_name="query_rag",
                queue=True  # Enable streaming for better UX
            )
            
            # Enter key support
            question_input.submit(
                fn=self.query_rag,
                inputs=[question_input, show_context],
                outputs=[response_output, context_output, metrics_output],
                api_name="query_rag_enter",
                queue=True
            )
            
            # Example button handlers
            example_btn_1.click(
                fn=lambda: "What are the common symptoms of diabetes and how can I recognize them?",
                outputs=[question_input]
            )
            
            example_btn_2.click(
                fn=lambda: "What are the different types of blood pressure medications and their side effects?",
                outputs=[question_input]
            )
            
            example_btn_3.click(
                fn=lambda: "What are the warning signs and symptoms of a heart attack?",
                outputs=[question_input]
            )
            
            example_btn_4.click(
                fn=lambda: "What are the current COVID-19 vaccination guidelines for adults?",
                outputs=[question_input]
            )
            
            example_btn_5.click(
                fn=lambda: "What are some signs of depression and anxiety, and when should I seek help?",
                outputs=[question_input]
            )
            
            example_btn_6.click(
                fn=lambda: "What are the important prenatal care guidelines for pregnant women?",
                outputs=[question_input]
            )
        
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
    """Main entry point for the MVP RAG Healthcare AI Assistant."""
    try:
        # Create and launch the interface
        interface = GradioRAGInterface()
        interface.launch()
        
    except Exception as e:
        logger.error(f"Failed to launch Gradio interface: {e}")
        print(f"❌ Error: {e}")
        print("Please check that Ollama and Qdrant are running.")


if __name__ == "__main__":
    main()
