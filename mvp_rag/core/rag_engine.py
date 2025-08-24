"""
Main RAG engine for the MVP Healthcare AI Assistant.

This orchestrates the entire RAG workflow:
1. Query embedding
2. Vector search
3. Context retrieval
4. LLM generation
5. Response formatting
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

logger = get_logger("rag_engine")

class RAGEngine:
    """Main RAG orchestration engine."""
    
    def __init__(self,
                 llm_model: str = "phi4-mini",
                 embedding_model: str = "bge-m3",
                 top_k: int = 5,
                 score_threshold: float = 0.3):
        """
        Initialize the RAG engine.
        
        Args:
            llm_model: Ollama model for text generation
            embedding_model: Ollama model for embeddings
            top_k: Number of documents to retrieve
            score_threshold: Minimum similarity score
        """
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.top_k = top_k
        self.score_threshold = score_threshold
        
        # Initialize clients
        self.llm_client = OllamaClient()
        self.vector_store = QdrantVectorStore()
        
        self.logger = logger
        
        # Healthcare-specific system prompt
        self.system_prompt = """You are a helpful healthcare AI assistant. You provide accurate, 
        educational health information based on the context provided. Always include appropriate 
        medical disclaimers and encourage users to consult healthcare professionals for medical advice.
        
        Guidelines:
        - Be informative but not diagnostic
        - Include relevant medical disclaimers
        - Encourage professional consultation when appropriate
        - Be clear about limitations of AI health advice"""
    
    def query(self, user_question: str) -> Dict[str, Any]:
        """
        Process a user query through the RAG pipeline.
        
        Args:
            user_question: The user's health-related question
            
        Returns:
            Complete response with context and metadata
        """
        start_time = time.time()
        
        self.logger.info(f"Processing query: {user_question}")
        
        try:
            # Step 1: Generate query embedding
            embedding_start = time.time()
            query_embedding = self.llm_client.embed(self.embedding_model, user_question)
            embedding_time = time.time() - embedding_start
            
            # Step 2: Vector search
            search_start = time.time()
            search_results = self.vector_store.search(
                query_embedding, 
                top_k=self.top_k,
                score_threshold=self.score_threshold
            )
            search_time = time.time() - search_start
            
            # Step 3: Prepare context for LLM
            context = self._prepare_context(search_results)
            
            # Step 4: Generate LLM response
            generation_start = time.time()
            llm_response = self._generate_response(user_question, context)
            generation_time = time.time() - generation_start
            
            # Step 5: Calculate metrics
            total_time = time.time() - start_time
            
            metrics = {
                "total_time_ms": round(total_time * 1000, 2),
                "embedding_time_ms": round(embedding_time * 1000, 2),
                "search_time_ms": round(search_time * 1000, 2),
                "generation_time_ms": round(generation_time * 1000, 2),
                "documents_retrieved": len(search_results),
                "average_similarity_score": self._calculate_avg_score(search_results),
                "llm_model": self.llm_model,
                "embedding_model": self.embedding_model
            }
            
            # Step 6: Prepare final response
            result = {
                "response": llm_response["text"],
                "context": {
                    "retrieved_documents": search_results,
                    "context_summary": self._summarize_context(search_results)
                },
                "metrics": metrics,
                "query": user_question,
                "system_info": self._get_system_info()
            }
            
            self.logger.info(f"Query processed in {total_time:.2f}s, retrieved {len(search_results)} documents")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return self._create_error_response(user_question, str(e))
    
    def _prepare_context(self, search_results: List[Dict[str, Any]]) -> str:
        """Prepare context from search results for LLM prompt."""
        if not search_results:
            return "No relevant documents found in the knowledge base."
        
        context_parts = []
        for i, result in enumerate(search_results, 1):
            content = result.get("content", "")
            score = result.get("score", 0)
            source = result.get("source", "Unknown")
            
            context_parts.append(f"Document {i} (Relevance: {score:.3f}, Source: {source}):\n{content}\n")
        
        return "\n".join(context_parts)
    
    def _generate_response(self, question: str, context: str) -> Dict[str, Any]:
        """Generate LLM response using retrieved context."""
        prompt = f"""Based on the following healthcare information, please answer the user's question.

Context:
{context}

User Question: {question}

Please provide a helpful, accurate response based on the context above. Include appropriate medical disclaimers."""

        return self.llm_client.generate(
            model=self.llm_model,
            prompt=prompt,
            system=self.system_prompt,
            temperature=0.7,
            max_tokens=1000
        )
    
    def _calculate_avg_score(self, search_results: List[Dict[str, Any]]) -> float:
        """Calculate average similarity score of retrieved documents."""
        if not search_results:
            return 0.0
        
        scores = [result.get("score", 0) for result in search_results]
        return round(sum(scores) / len(scores), 3)
    
    def _summarize_context(self, search_results: List[Dict[str, Any]]) -> str:
        """Create a summary of the retrieved context."""
        if not search_results:
            return "No relevant documents found."
        
        sources = set(result.get("source", "Unknown") for result in search_results)
        avg_score = self._calculate_avg_score(search_results)
        
        return f"Retrieved {len(search_results)} documents from {len(sources)} sources with average relevance score {avg_score}"
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information and status."""
        return {
            "rag_engine": "MVP Local RAG",
            "llm_model": self.llm_model,
            "embedding_model": self.embedding_model,
            "vector_store": "Qdrant (Local)",
            "ollama_status": self.llm_client.health_check(),
            "qdrant_status": self.vector_store.health_check(),
            "collection_info": self.vector_store.get_collection_info()
        }
    
    def _create_error_response(self, question: str, error: str) -> Dict[str, Any]:
        """Create an error response when processing fails."""
        return {
            "response": f"I apologize, but I encountered an error while processing your question: '{error}'. This demonstrates a limitation of the current MVP system. In production, we'd have better error handling and fallback mechanisms.",
            "context": {"retrieved_documents": [], "context_summary": "Error occurred during processing"},
            "metrics": {"total_time_ms": 0, "error": error},
            "query": question,
            "system_info": self._get_system_info()
        }
    
    def health_check(self) -> Dict[str, bool]:
        """Check health of all components."""
        return {
            "ollama": self.llm_client.health_check(),
            "qdrant": self.vector_store.health_check(),
            "overall": self.llm_client.health_check() and self.vector_store.health_check()
        }
