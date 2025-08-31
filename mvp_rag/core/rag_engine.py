"""
🏥 MVP RAG Healthcare AI Assistant - Core RAG Engine

This module orchestrates the entire RAG (Retrieval-Augmented Generation) workflow:
1. Query embedding using Ollama's nomic-embed-text model
2. Vector search in Qdrant database
3. Context retrieval and preparation
4. LLM generation using Ollama's qwen3:4b-instruct model
5. Response formatting with medical disclaimers
6. Performance metrics collection

The engine is optimized for:
- Fast response times (pre-warming, optimized retrieval)
- Healthcare domain expertise (medical disclaimers, professional guidance)
- Production-ready patterns (error handling, logging, monitoring)
"""

import time
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.llm_client import OllamaClient
from core.vector_store import QdrantVectorStore
from utils.logger import get_logger

# Initialize logging for the RAG engine
logger = get_logger("rag_engine")


class RAGEngine:
    """
    Main RAG orchestration engine for healthcare AI assistance.
    
    This class coordinates all components of the RAG pipeline:
    - LLM client for text generation and embeddings
    - Vector store for document retrieval
    - Context preparation and optimization
    - Response generation with healthcare focus
    - Performance monitoring and metrics
    """
    
    def __init__(self,
                 llm_model: str = "qwen3:4b-instruct",
                 embedding_model: str = "nomic-embed-text",
                 top_k: int = 3,
                 score_threshold: float = 0.38):
        """
        Initialize the RAG engine with optimized parameters.
        
        Args:
            llm_model: Ollama model for text generation (default: qwen3:4b-instruct)
            embedding_model: Ollama model for embeddings (default: nomic-embed-text)
            top_k: Number of documents to retrieve (default: 3 for focused context)
            score_threshold: Minimum similarity score for retrieval (default: 0.38)
        """
        # Model configuration
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        
        # Retrieval optimization parameters
        self.top_k = top_k
        self.score_threshold = score_threshold
        
        # Initialize core clients
        self.llm_client = OllamaClient()
        self.vector_store = QdrantVectorStore()
        
        # Setup logging
        self.logger = logger
        
        # Healthcare-specific system prompt with safety guidelines
        self.system_prompt = """You are a helpful healthcare AI assistant. You provide accurate, 
        educational health information based on the context provided. Always include appropriate 
        medical disclaimers and encourage users to consult healthcare professionals for medical advice.
        
        Guidelines:
        - Be informative but not diagnostic
        - Include relevant medical disclaimers
        - Encourage professional consultation when appropriate
        - Be clear about limitations of AI health advice
        - Keep answers concise (about 3–5 sentences) focused on the question
        - When helpful, include one practical, low-risk actionable step users can take now"""
        
        # Pre-warm the LLM to reduce first-response latency
        self._pre_warm_llm()
    
    def _pre_warm_llm(self):
        """
        Pre-warm the LLM to reduce first-response latency.
        
        This is crucial for demo presentations and production use.
        Sends a trivial query to initialize the model in memory.
        """
        self.logger.info("🔥 Pre-warming LLM for optimal performance...")
        try:
            # Send a minimal query to warm up the model
            _ = self.llm_client.generate(
                model=self.llm_model,
                prompt="hello",
                system="You are a helpful assistant.",
                temperature=0.1,
                max_tokens=10
            )
            self.logger.info("✅ LLM pre-warmed successfully")
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to pre-warm LLM: {e}")
            # Non-critical - continue without pre-warming
    
    def query(self, user_question: str) -> Dict[str, Any]:
        """
        Process a user query through the complete RAG pipeline.
        
        This is the main method that orchestrates the entire workflow:
        1. Query embedding generation
        2. Vector similarity search
        3. Context retrieval and preparation
        4. LLM response generation
        5. Performance metrics collection
        
        Args:
            user_question: The user's health-related question
            
        Returns:
            Complete response dictionary containing:
            - response: Generated AI response
            - context: Retrieved documents and context summary
            - metrics: Performance timing and search analytics
        """
        start_time = time.time()
        
        self.logger.info(f"🔍 Processing query: {user_question}")
        
        try:
            # Step 1: Generate query embedding for semantic search
            embedding_start = time.time()
            query_embedding = self.llm_client.embed(self.embedding_model, user_question)
            embedding_time = time.time() - embedding_start
            
            # Step 2: Perform vector similarity search in Qdrant
            search_start = time.time()
            search_results = self.vector_store.search(
                query_embedding, 
                top_k=self.top_k,
                score_threshold=self.score_threshold
            )
            search_time = time.time() - search_start
            
            # Step 3: Prepare context for LLM generation
            context = self._prepare_context(search_results)
            
            # Step 4: Generate LLM response with healthcare focus
            generation_start = time.time()
            response = self._generate_response(user_question, context)
            generation_time = time.time() - generation_start
            
            # Calculate total processing time
            total_time = time.time() - start_time
            
            # Collect comprehensive performance metrics
            metrics = self._collect_metrics(
                total_time, embedding_time, search_time, generation_time,
                search_results, user_question
            )
            
            # Log successful query completion
            self.logger.info(f"✅ Query processed successfully in {total_time:.2f}s")
            
            return {
                "response": response,
                "context": context,
                "metrics": metrics
            }
            
        except Exception as e:
            # Log error and return error response
            self.logger.error(f"❌ Error processing query: {e}")
            total_time = time.time() - start_time
            
            return {
                "response": f"❌ I apologize, but I encountered an error processing your question: {str(e)}",
                "context": {"context_summary": "Error occurred during processing", "retrieved_documents": []},
                "metrics": self._collect_error_metrics(total_time, str(e))
            }
    
    def _prepare_context(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prepare context from search results for LLM generation.
        
        This method:
        - Formats retrieved documents for LLM consumption
        - Creates a context summary for the user
        - Ensures proper medical information handling
        
        Args:
            search_results: List of retrieved documents with scores
            
        Returns:
            Context dictionary with summary and document details
        """
        if not search_results:
            return {
                "context_summary": "No relevant documents found for this query.",
                "retrieved_documents": []
            }
        
        # Create context summary for LLM
        context_parts = []
        for doc in search_results:
            # Include document content and metadata
            context_parts.append(f"Document: {doc.get('content', '')}")
        
        # Join all context parts for LLM consumption
        full_context = "\n\n".join(context_parts)
        
        # Create user-friendly context summary
        context_summary = f"Found {len(search_results)} relevant document(s) for your question."
        
        return {
            "context_summary": context_summary,
            "retrieved_documents": search_results,
            "full_context": full_context
        }
    
    def _generate_response(self, question: str, context: Dict[str, Any]) -> str:
        """
        Generate AI response using the LLM with healthcare context.
        
        This method:
        - Constructs an optimized prompt for the LLM
        - Includes retrieved context for accurate responses
        - Applies healthcare-specific system prompt
        - Ensures medical disclaimers and safety guidelines
        
        Args:
            question: User's original question
            context: Retrieved context and documents
            
        Returns:
            Generated AI response with healthcare focus
        """
        # Construct the prompt for the LLM
        if context.get('full_context'):
            prompt = f"""Based on the following healthcare information, please answer this question: {question}

Context:
{context['full_context']}

Please provide a helpful, accurate response that includes appropriate medical disclaimers."""
        else:
            prompt = f"""Please answer this healthcare question: {question}

Note: I don't have specific context for this question, so I'll provide general information with appropriate medical disclaimers."""
        
        # Generate response with healthcare-optimized parameters
        try:
            result = self.llm_client.generate(
                model=self.llm_model,
                prompt=prompt,
                system=self.system_prompt,
                temperature=0.4,      # Balanced creativity and accuracy
                max_tokens=400        # Concise, focused responses
            )
            
            return result.get('text', 'No response generated')
            
        except Exception as e:
            self.logger.error(f"❌ Error generating LLM response: {e}")
            return f"❌ I apologize, but I encountered an error generating a response: {str(e)}"
    
    def _collect_metrics(self, total_time: float, embedding_time: float, 
                        search_time: float, generation_time: float,
                        search_results: List[Dict[str, Any]], 
                        user_question: str) -> Dict[str, Any]:
        """
        Collect comprehensive performance metrics for monitoring.
        
        This method tracks:
        - Timing for each pipeline stage
        - Search performance metrics
        - Model usage information
        - Query characteristics
        
        Args:
            total_time: Total processing time
            embedding_time: Time spent on query embedding
            search_time: Time spent on vector search
            generation_time: Time spent on LLM generation
            search_results: Retrieved search results
            user_question: Original user question
            
        Returns:
            Dictionary containing all performance metrics
        """
        # Calculate similarity scores for analysis
        similarity_scores = [doc.get('score', 0) for doc in search_results]
        avg_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0
        
        return {
            # Timing metrics (in milliseconds)
            "total_time_ms": round(total_time * 1000, 2),
            "embedding_time_ms": round(embedding_time * 1000, 2),
            "search_time_ms": round(search_time * 1000, 2),
            "generation_time_ms": round(generation_time * 1000, 2),
            
            # Search performance metrics
            "documents_retrieved": len(search_results),
            "avg_similarity_score": round(avg_similarity, 3),
            "min_similarity_score": min(similarity_scores) if similarity_scores else 0,
            "max_similarity_score": max(similarity_scores) if similarity_scores else 0,
            
            # Model information
            "llm_model": self.llm_model,
            "embedding_model": self.embedding_model,
            
            # Query characteristics
            "query_length": len(user_question),
            "query_words": len(user_question.split())
        }
    
    def _collect_error_metrics(self, total_time: float, error_message: str) -> Dict[str, Any]:
        """
        Collect metrics for failed queries.
        
        Args:
            total_time: Time spent before error occurred
            error_message: Description of the error
            
        Returns:
            Error metrics dictionary
        """
        return {
            "total_time_ms": round(total_time * 1000, 2),
            "embedding_time_ms": 0,
            "search_time_ms": 0,
            "generation_time_ms": 0,
            "documents_retrieved": 0,
            "avg_similarity_score": 0,
            "error": error_message,
            "status": "failed"
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check of all RAG components.
        
        This method checks:
        - Ollama service availability
        - Qdrant vector store health
        - Model accessibility
        - Collection status
        
        Returns:
            Health status dictionary
        """
        health_status = {
            "ollama": False,
            "qdrant": False,
            "overall": False,
            "details": {}
        }
        
        try:
            # Check Ollama health
            try:
                # Test LLM generation
                test_response = self.llm_client.generate(
                    model=self.llm_model,
                    prompt="health check",
                    max_tokens=5
                )
                health_status["ollama"] = True
                health_status["details"]["ollama"] = "✅ Healthy - LLM generation working"
            except Exception as e:
                health_status["details"]["ollama"] = f"❌ Unhealthy - {str(e)}"
            
            # Check Qdrant health
            try:
                collection_info = self.vector_store.get_collection_info()
                if collection_info:
                    health_status["qdrant"] = True
                    health_status["details"]["qdrant"] = f"✅ Healthy - Collection: {collection_info.get('name', 'Unknown')}, Documents: {collection_info.get('points_count', 'Unknown')}"
                else:
                    health_status["details"]["qdrant"] = "❌ Unhealthy - No collection info"
            except Exception as e:
                health_status["details"]["qdrant"] = f"❌ Unhealthy - {str(e)}"
            
            # Overall health assessment
            health_status["overall"] = health_status["ollama"] and health_status["qdrant"]
            
        except Exception as e:
            health_status["details"]["overall"] = f"❌ Health check failed: {str(e)}"
        
        return health_status
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get comprehensive system information for monitoring.
        
        Returns:
            System configuration and status information
        """
        try:
            collection_info = self.vector_store.get_collection_info()
            
            return {
                "rag_engine": "MVP RAG Healthcare AI Assistant",
                "llm_model": self.llm_model,
                "embedding_model": self.embedding_model,
                "vector_store": "Qdrant (Local Docker)",
                "collection_info": collection_info,
                "retrieval_config": {
                    "top_k": self.top_k,
                    "score_threshold": self.score_threshold
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return {"error": str(e)}
