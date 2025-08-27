"""
📝 Logging Utility for MVP RAG Healthcare AI Assistant

This module provides a centralized logging system for the MVP RAG system.
It ensures consistent logging across all components with:

- Structured log formatting
- Configurable log levels
- Component-specific loggers
- Console output for development
- Production-ready logging patterns

The logging system helps with:
- Debugging and troubleshooting
- Performance monitoring
- Error tracking and analysis
- Demo presentation flow
- Production deployment monitoring

Author: AI Evolution Demo Team
Purpose: Centralized logging for MVP demonstration
"""

import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO") -> None:
    """
    Setup basic logging configuration for the MVP RAG system.
    
    This function configures:
    - Log level (default: INFO for production-like behavior)
    - Log format with timestamp, component name, and level
    - Console output handler for development and demo
    - Consistent formatting across all components
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
              Defaults to INFO for optimal demo performance
    """
    # Configure logging with production-ready format
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)  # Console output for demo visibility
        ]
    )
    
    # Log the logging setup for transparency
    logging.getLogger("mvp_rag.setup").info(f"Logging configured at level: {level}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified component name.
    
    This function creates component-specific loggers that:
    - Include the "mvp_rag" prefix for easy identification
    - Allow component-specific log filtering
    - Maintain consistent formatting across all loggers
    - Support hierarchical logging structure
    
    Args:
        name: Component name (e.g., "rag_engine", "llm_client", "vector_store")
        
    Returns:
        Configured logger instance for the specified component
        
    Example:
        >>> logger = get_logger("rag_engine")
        >>> logger.info("RAG engine initialized successfully")
        # Output: 2024-01-15 10:30:00 - mvp_rag.rag_engine - INFO - RAG engine initialized successfully
    """
    # Create component-specific logger with consistent naming
    logger_name = f"mvp_rag.{name}"
    return logging.getLogger(logger_name)


# Initialize default logging configuration
# This ensures logging is ready when the module is imported
setup_logging()
