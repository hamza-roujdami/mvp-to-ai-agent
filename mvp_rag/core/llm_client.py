"""
🤖 Ollama LLM Client for MVP RAG Healthcare AI Assistant

This module provides a clean, production-ready interface to Ollama models for:
- Text generation (using qwen3:4b-instruct)
- Text embeddings (using nomic-embed-text)
- Health monitoring and status checks
- Error handling and logging

The client is designed for:
- Fast, reliable communication with Ollama
- Comprehensive error handling
- Performance monitoring and metrics
- Easy integration with the RAG pipeline
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

# Initialize logging for the LLM client
logger = get_logger("llm_client")


class OllamaClient:
    """
    Production-ready client for interacting with Ollama models.
    
    This class handles:
    - Text generation with configurable parameters
    - Text embedding for semantic search
    - Health monitoring and service status
    - Error handling and retry logic
    - Performance metrics collection
    
    Designed for seamless integration with the RAG pipeline.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        Initialize the Ollama client with connection settings.
        
        Args:
            base_url: Ollama service URL (default: localhost:11434)
        """
        self.base_url = base_url
        self.logger = logger
        
        # Test connection on initialization
        self._test_connection()
    
    def _test_connection(self):
        """
        Test the connection to Ollama service.
        
        This method verifies that Ollama is running and accessible
        before allowing any operations. Critical for demo reliability.
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                self.logger.info(f"✅ Ollama connection established at {self.base_url}")
            else:
                self.logger.warning(f"⚠️ Ollama responded with status {response.status_code}")
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to Ollama at {self.base_url}: {e}")
            # Don't raise here - allow graceful degradation
    
    def generate(self, 
                model: str, 
                prompt: str, 
                system: Optional[str] = None,
                temperature: float = 0.7,
                max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Generate text using the specified Ollama model.
        
        This method:
        - Sends generation requests to Ollama
        - Handles system prompts and user prompts
        - Configures generation parameters (temperature, max_tokens)
        - Collects performance metrics
        - Provides comprehensive error handling
        
        Args:
            model: Ollama model name (e.g., "qwen3:4b-instruct")
            prompt: User prompt for text generation
            system: Optional system message for model behavior
            temperature: Creativity level (0.0 = focused, 1.0 = creative)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dictionary containing:
            - text: Generated response text
            - model: Model used for generation
            - generation_time: Time taken for generation
            - total_duration: Ollama's reported generation time
            - prompt_eval_count: Tokens in prompt
            - eval_count: Tokens generated
            
        Raises:
            Exception: If generation fails or Ollama is unavailable
        """
        start_time = time.time()
        
        # Prepare the request payload
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,  # Disable streaming for consistent response handling
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        # Add system message if provided
        if system:
            payload["system"] = system
        
        try:
            # Send generation request to Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60  # 60 second timeout for generation
            )
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Parse the response
            result = response.json()
            generation_time = time.time() - start_time
            
            # Log successful generation with performance metrics
            self.logger.info(f"✅ Generated response in {generation_time:.2f}s using {model}")
            
            # Return comprehensive response data
            return {
                "text": result.get("response", ""),
                "model": model,
                "generation_time": generation_time,
                "total_duration": result.get("total_duration", 0),
                "prompt_eval_count": result.get("prompt_eval_count", 0),
                "eval_count": result.get("eval_count", 0)
            }
            
        except requests.exceptions.RequestException as e:
            # Handle network and HTTP errors
            self.logger.error(f"❌ Error generating text: {e}")
            raise Exception(f"Failed to generate text: {e}")
        except json.JSONDecodeError as e:
            # Handle malformed JSON responses
            self.logger.error(f"❌ Invalid JSON response from Ollama: {e}")
            raise Exception(f"Invalid response format from Ollama: {e}")
        except Exception as e:
            # Handle any other unexpected errors
            self.logger.error(f"❌ Unexpected error during text generation: {e}")
            raise Exception(f"Text generation failed: {e}")
    
    def embed(self, model: str, text: str) -> List[float]:
        """
        Generate text embeddings using the specified Ollama model.
        
        This method:
        - Converts text to numerical vectors for semantic search
        - Optimized for fast embedding generation
        - Handles various text lengths and formats
        - Provides error handling for embedding failures
        
        Args:
            model: Ollama embedding model name (e.g., "nomic-embed-text")
            text: Text to convert to embeddings
            
        Returns:
            List of float values representing the text embedding
            
        Raises:
            Exception: If embedding generation fails
        """
        start_time = time.time()
        
        # Prepare embedding request
        payload = {
            "model": model,
            "prompt": text
        }
        
        try:
            # Send embedding request to Ollama
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json=payload,
                timeout=30  # 30 second timeout for embeddings
            )
            response.raise_for_status()
            
            # Parse embedding response
            result = response.json()
            embedding_time = time.time() - start_time
            
            # Extract embedding vector
            embedding = result.get("embedding", [])
            
            if not embedding:
                raise Exception("No embedding generated")
            
            # Log successful embedding with performance metrics
            self.logger.info(f"✅ Generated embedding in {embedding_time:.2f}s using {model} (vector size: {len(embedding)})")
            
            return embedding
            
        except requests.exceptions.RequestException as e:
            # Handle network and HTTP errors
            self.logger.error(f"❌ Error generating embedding: {e}")
            raise Exception(f"Failed to generate embedding: {e}")
        except json.JSONDecodeError as e:
            # Handle malformed JSON responses
            self.logger.error(f"❌ Invalid JSON response from Ollama: {e}")
            raise Exception(f"Invalid response format from Ollama: {e}")
        except Exception as e:
            # Handle any other unexpected errors
            self.logger.error(f"❌ Unexpected error during embedding: {e}")
            raise Exception(f"Embedding generation failed: {e}")
    
    def health_check(self) -> bool:
        """
        Check if Ollama service is healthy and accessible.
        
        This method:
        - Tests basic connectivity to Ollama
        - Verifies API endpoint availability
        - Provides quick health status for monitoring
        
        Returns:
            True if Ollama is healthy, False otherwise
        """
        try:
            # Simple health check using the tags endpoint
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            self.logger.warning(f"⚠️ Health check failed: {e}")
            return False
    
    def get_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available Ollama models.
        
        This method:
        - Retrieves all installed models
        - Provides model information and metadata
        - Useful for debugging and model selection
        
        Returns:
            List of model information dictionaries
            
        Raises:
            Exception: If model list retrieval fails
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            
            result = response.json()
            models = result.get("models", [])
            
            self.logger.info(f"✅ Retrieved {len(models)} available models")
            return models
            
        except Exception as e:
            self.logger.error(f"❌ Error retrieving models: {e}")
            raise Exception(f"Failed to retrieve models: {e}")
    
    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific model.
        
        Args:
            model: Name of the model to inspect
            
        Returns:
            Dictionary containing model details
            
        Raises:
            Exception: If model info retrieval fails
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": model},
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            self.logger.info(f"✅ Retrieved info for model: {model}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Error retrieving model info for {model}: {e}")
            raise Exception(f"Failed to retrieve model info: {e}")
