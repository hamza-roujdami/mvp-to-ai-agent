"""
Ollama LLM client for the MVP RAG system.

This provides a clean interface to Ollama models for
both text generation and embeddings.
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import requests

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import get_logger

logger = get_logger("llm_client")

class OllamaClient:
    """Client for interacting with Ollama models."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: Ollama service URL
        """
        self.base_url = base_url
        self.logger = logger
        
    def generate(self, 
                model: str, 
                prompt: str, 
                system: Optional[str] = None,
                temperature: float = 0.7,
                max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Generate text using Ollama.
        
        Args:
            model: Ollama model name
            prompt: User prompt
            system: System message
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response
        """
        start_time = time.time()
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            generation_time = time.time() - start_time
            
            self.logger.info(f"Generated response in {generation_time:.2f}s using {model}")
            
            return {
                "text": result.get("response", ""),
                "model": model,
                "generation_time": generation_time,
                "total_duration": result.get("total_duration", 0),
                "prompt_eval_count": result.get("prompt_eval_count", 0),
                "eval_count": result.get("eval_count", 0)
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error generating text: {e}")
            raise Exception(f"Failed to generate text: {e}")
    
    def embed(self, model: str, text: str) -> List[float]:
        """
        Generate embeddings using Ollama.
        
        Args:
            model: Ollama model name (should be embedding model)
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        payload = {
            "model": model,
            "prompt": text
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            embedding = result.get("embedding", [])
            
            self.logger.info(f"Generated embedding with {len(embedding)} dimensions using {model}")
            
            return embedding
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error generating embedding: {e}")
            raise Exception(f"Failed to generate embedding: {e}")
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List available Ollama models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            
            models = response.json().get("models", [])
            self.logger.info(f"Found {len(models)} available models")
            
            return models
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error listing models: {e}")
            return []
    
    def health_check(self) -> bool:
        """Check if Ollama service is healthy."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False
