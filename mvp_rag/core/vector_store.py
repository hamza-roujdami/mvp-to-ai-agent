"""
Qdrant vector store client for the MVP RAG system.

This provides vector database operations for storing and
retrieving healthcare document embeddings.
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

logger = get_logger("vector_store")

class QdrantVectorStore:
    """Vector store using Qdrant for document storage and retrieval."""
    
    def __init__(self, 
                 host: str = "localhost", 
                 port: int = 6333,
                 collection_name: str = "healthcare_docs"):
        """
        Initialize the Qdrant vector store.
        
        Args:
            host: Qdrant host
            port: Qdrant port
            collection_name: Collection name for documents
        """
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.logger = logger
        
        # Initialize collection if it doesn't exist
        self._init_collection()
    
    def _init_collection(self, vector_size: int = 1024):
        """Initialize the collection with proper configuration."""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )
                self.logger.info(f"Created collection: {self.collection_name}")
            else:
                self.logger.info(f"Using existing collection: {self.collection_name}")
                
        except Exception as e:
            self.logger.error(f"Error initializing collection: {e}")
            raise
    
    def add_documents(self, 
                     documents: List[Dict[str, any]], 
                     embeddings: List[List[float]]) -> List[str]:
        """
        Add documents with their embeddings to the vector store.
        
        Args:
            documents: List of document dictionaries
            embeddings: List of embedding vectors
            
        Returns:
            List of document IDs
        """
        if len(documents) != len(embeddings):
            raise ValueError("Documents and embeddings must have the same length")
        
        points = []
        doc_ids = []
        
        for doc, embedding in zip(documents, embeddings):
            doc_id = str(uuid.uuid4())
            doc_ids.append(doc_id)
            
            point = PointStruct(
                id=doc_id,
                vector=embedding,
                payload={
                    "content": doc.get("content", ""),
                    "metadata": doc.get("metadata", {}),
                    "source": doc.get("source", ""),
                    "chunk_id": doc.get("chunk_id", ""),
                    "title": doc.get("title", "")
                }
            )
            points.append(point)
        
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            self.logger.info(f"Added {len(documents)} documents to vector store")
            return doc_ids
            
        except Exception as e:
            self.logger.error(f"Error adding documents: {e}")
            raise
    
    def search(self, 
              query_embedding: List[float], 
              top_k: int = 5,
              score_threshold: float = 0.7) -> List[Dict[str, any]]:
        """
        Search for similar documents using vector similarity.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            score_threshold: Minimum similarity score
            
        Returns:
            List of similar documents with scores
        """
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=score_threshold
            )
            
            results = []
            for hit in search_result:
                results.append({
                    "id": hit.id,
                    "score": hit.score,
                    "content": hit.payload.get("content", ""),
                    "metadata": hit.payload.get("metadata", {}),
                    "source": hit.payload.get("source", ""),
                    "title": hit.payload.get("title", "")
                })
            
            self.logger.info(f"Found {len(results)} similar documents")
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching documents: {e}")
            raise
    
    def get_collection_info(self) -> Dict[str, any]:
        """Get information about the collection."""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vector_size": info.config.params.vectors.size,
                "distance": str(info.config.params.vectors.distance),
                "points_count": info.points_count,
                "segments_count": info.segments_count
            }
        except Exception as e:
            self.logger.error(f"Error getting collection info: {e}")
            return {}
    
    def delete_collection(self):
        """Delete the collection (use with caution)."""
        try:
            self.client.delete_collection(self.collection_name)
            self.logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            self.logger.error(f"Error deleting collection: {e}")
            raise
    
    def health_check(self) -> bool:
        """Check if Qdrant service is healthy."""
        try:
            self.client.get_collections()
            return True
        except:
            return False
