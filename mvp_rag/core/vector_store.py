"""
🗄️ Qdrant Vector Store Client for MVP RAG Healthcare AI Assistant

This module provides a production-ready interface to Qdrant vector database for:
- Storing healthcare document embeddings
- Performing semantic similarity search
- Managing document collections
- Auto-scaling vector dimensions
- Health monitoring and status checks

The client is designed for:
- Seamless integration with the RAG pipeline
- Automatic collection management
- Vector size mismatch detection and resolution
- Comprehensive error handling and logging
- Performance optimization for healthcare queries
"""

import uuid
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, 
    VectorParams, 
    PointStruct,
    Filter,
    SearchRequest
)

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import get_logger

# Initialize logging for the vector store
logger = get_logger("vector_store")


class QdrantVectorStore:
    """
    Production-ready vector store using Qdrant for healthcare document management.
    
    This class handles:
    - Document storage with embeddings
    - Semantic similarity search
    - Collection management and auto-scaling
    - Health monitoring and diagnostics
    - Performance optimization
    
    Designed for seamless integration with the RAG pipeline.
    """
    
    def __init__(self, 
                 host: str = "localhost", 
                 port: int = 6333,
                 collection_name: str = "healthcare_docs"):
        """
        Initialize the Qdrant vector store with connection settings.
        
        Args:
            host: Qdrant host address (default: localhost)
            port: Qdrant port number (default: 6333)
            collection_name: Name of the document collection (default: healthcare_docs)
        """
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.logger = logger
        
        # Test connection on initialization
        self._test_connection()
        
        # Collection will be created automatically on first document addition
        # with the correct vector size based on the embedding model
    
    def _test_connection(self):
        """
        Test the connection to Qdrant service.
        
        This method verifies that Qdrant is running and accessible
        before allowing any operations. Critical for demo reliability.
        """
        try:
            # Simple health check using collections endpoint
            collections = self.client.get_collections()
            self.logger.info(f"✅ Qdrant connection established at {self.client._client.url}")
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to Qdrant: {e}")
            # Don't raise here - allow graceful degradation
    
    def _ensure_collection(self, vector_size: int) -> None:
        """
        Ensure collection exists with the correct vector size.
        
        This method:
        - Creates the collection if it doesn't exist
        - Detects vector size mismatches (e.g., when switching embedding models)
        - Automatically recreates the collection with correct dimensions
        - Ensures data integrity across embedding model changes
        
        Args:
            vector_size: Required vector dimensions for the embedding model
            
        Raises:
            Exception: If collection creation or management fails
        """
        try:
            # Get list of existing collections
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if self.collection_name not in collection_names:
                # Create new collection with specified vector size
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=vector_size, 
                        distance=Distance.COSINE  # Cosine similarity for semantic search
                    )
                )
                self.logger.info(f"✅ Created collection: {self.collection_name} (vector_size={vector_size})")
                return
            
            # Collection exists - check for vector size mismatch
            current_info = self.client.get_collection(self.collection_name)
            current_size = current_info.config.params.vectors.size
            
            if current_size != vector_size:
                # Vector size mismatch detected - recreate collection
                self.logger.info(
                    f"🔄 Recreating collection {self.collection_name} due to vector size mismatch "
                    f"(current={current_size}, required={vector_size})"
                )
                
                # Delete and recreate with correct dimensions
                self.client.delete_collection(self.collection_name)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=vector_size, 
                        distance=Distance.COSINE
                    )
                )
                self.logger.info(f"✅ Collection recreated with correct vector size: {vector_size}")
            else:
                self.logger.info(f"✅ Using existing collection: {self.collection_name} (vector_size={current_size})")
                
        except Exception as e:
            self.logger.error(f"❌ Error ensuring collection: {e}")
            raise Exception(f"Collection management failed: {e}")
    
    def add_documents(self, 
                     documents: List[Dict[str, any]], 
                     embeddings: List[List[float]]) -> List[str]:
        """
        Add documents with their embeddings to the vector store.
        
        This method:
        - Validates input data consistency
        - Ensures collection exists with correct vector size
        - Converts documents to Qdrant point format
        - Performs batch insertion for efficiency
        - Generates unique document IDs
        
        Args:
            documents: List of document dictionaries (must contain 'content', 'title', 'source')
            embeddings: List of embedding vectors (must match document count)
            
        Returns:
            List of generated document IDs for reference
            
        Raises:
            ValueError: If documents and embeddings don't match
            Exception: If document insertion fails
        """
        # Validate input consistency
        if len(documents) != len(embeddings):
            raise ValueError("Documents and embeddings must have the same length")
        
        if not documents or not embeddings:
            raise ValueError("Documents and embeddings cannot be empty")
        
        # Ensure collection exists with correct vector size
        if not embeddings[0]:
            raise ValueError("Embeddings are empty; cannot determine vector size")
        
        vector_size = len(embeddings[0])
        self._ensure_collection(vector_size)
        
        # Convert documents to Qdrant point format
        points = []
        doc_ids = []
        
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            # Generate unique document ID
            doc_id = str(uuid.uuid4())
            doc_ids.append(doc_id)
            
            # Create Qdrant point with document data and embedding
            point = PointStruct(
                id=doc_id,
                vector=embedding,
                payload={
                    "content": doc.get("content", ""),
                    "title": doc.get("title", ""),
                    "source": doc.get("source", ""),
                    "metadata": doc.get("metadata", {})
                }
            )
            points.append(point)
        
        try:
            # Perform batch insertion for efficiency
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            self.logger.info(f"✅ Added {len(documents)} documents to collection {self.collection_name}")
            return doc_ids
            
        except Exception as e:
            self.logger.error(f"❌ Error adding documents: {e}")
            raise Exception(f"Document insertion failed: {e}")
    
    def search(self, 
               query_embedding: List[float], 
               top_k: int = 3, 
               score_threshold: float = 0.38) -> List[Dict[str, any]]:
        """
        Perform semantic similarity search using query embedding.
        
        This method:
        - Searches for documents similar to the query
        - Applies similarity score threshold for quality control
        - Returns top-k most relevant documents
        - Includes similarity scores and document metadata
        
        Args:
            query_embedding: Query vector for similarity search
            top_k: Maximum number of documents to return (default: 3)
            score_threshold: Minimum similarity score (default: 0.38)
            
        Returns:
            List of document dictionaries with similarity scores
            
        Raises:
            Exception: If search operation fails
        """
        try:
            # Perform vector similarity search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=score_threshold
            )
            
            # Format results for RAG pipeline consumption
            documents = []
            for result in search_results:
                doc = {
                    "id": result.id,
                    "score": result.score,
                    "content": result.payload.get("content", ""),
                    "title": result.payload.get("title", ""),
                    "source": result.payload.get("source", ""),
                    "metadata": result.payload.get("metadata", {})
                }
                documents.append(doc)
            
            self.logger.info(f"🔍 Search completed: {len(documents)} documents found (threshold={score_threshold})")
            return documents
            
        except Exception as e:
            self.logger.error(f"❌ Error during search: {e}")
            raise Exception(f"Search operation failed: {e}")
    
    def get_collection_info(self) -> Dict[str, any]:
        """
        Get comprehensive information about the current collection.
        
        This method provides:
        - Collection metadata and configuration
        - Document count and storage statistics
        - Vector dimensions and distance metric
        - Performance and health indicators
        
        Returns:
            Dictionary containing collection information
            
        Raises:
            Exception: If collection info retrieval fails
        """
        try:
            # Get detailed collection information
            info = self.client.get_collection(self.collection_name)
            
            collection_info = {
                "name": self.collection_name,
                "vector_size": info.config.params.vectors.size,
                "distance": str(info.config.params.vectors.distance),
                "points_count": info.points_count,
                "segments_count": info.segments_count,
                "status": str(info.status)
            }
            
            self.logger.info(f"📊 Collection info retrieved: {collection_info['points_count']} documents, {collection_info['vector_size']} dimensions")
            return collection_info
            
        except Exception as e:
            self.logger.error(f"❌ Error getting collection info: {e}")
            return {}
    
    def health_check(self) -> bool:
        """
        Check if Qdrant service is healthy and accessible.
        
        This method:
        - Tests basic connectivity to Qdrant
        - Verifies collection accessibility
        - Provides quick health status for monitoring
        
        Returns:
            True if Qdrant is healthy, False otherwise
        """
        try:
            # Test connection and collection access
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if self.collection_name in collection_names:
                # Test collection info retrieval
                info = self.client.get_collection(self.collection_name)
                return info is not None
            else:
                # Collection doesn't exist yet - that's okay for new deployments
                return True
                
        except Exception as e:
            self.logger.warning(f"⚠️ Health check failed: {e}")
            return False
    
    def clear_collection(self) -> None:
        """
        Clear all documents from the collection.
        
        This method:
        - Removes all stored documents and embeddings
        - Keeps the collection structure intact
        - Useful for testing and data refresh
        
        Raises:
            Exception: If collection clearing fails
        """
        try:
            # Delete all points in the collection
            self.client.delete(
                collection_name=self.collection_name,
                points_selector={"all": True}
            )
            
            self.logger.info(f"🗑️ Cleared all documents from collection {self.collection_name}")
            
        except Exception as e:
            self.logger.error(f"❌ Error clearing collection: {e}")
            raise Exception(f"Collection clearing failed: {e}")
    
    def delete_collection(self) -> None:
        """
        Delete the entire collection.
        
        This method:
        - Removes the collection and all its data
        - Useful for complete reset or cleanup
        - Collection will be recreated on next document addition
        
        Raises:
            Exception: If collection deletion fails
        """
        try:
            # Delete the entire collection
            self.client.delete_collection(self.collection_name)
            
            self.logger.info(f"🗑️ Deleted collection {self.collection_name}")
            
        except Exception as e:
            self.logger.error(f"❌ Error deleting collection: {e}")
            raise Exception(f"Collection deletion failed: {e}")
