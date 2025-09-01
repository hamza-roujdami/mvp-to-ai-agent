#!/usr/bin/env python3
"""
🔇 Logging Configuration - Reduce Verbose Azure Output

This module configures logging to minimize verbose Azure debug output
and improve performance and readability.
"""

import logging
import os

def configure_logging():
    """Configure logging to reduce verbose Azure output."""
    
    # Set Azure logging to WARNING level (reduces verbose output)
    logging.getLogger('azure').setLevel(logging.WARNING)
    logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.ERROR)
    logging.getLogger('azure.identity').setLevel(logging.WARNING)
    logging.getLogger('azure.ai.agents').setLevel(logging.WARNING)
    logging.getLogger('azure.ai.projects').setLevel(logging.WARNING)
    
    # Set our application logging to INFO level
    logging.getLogger('agentic_rag').setLevel(logging.INFO)
    
    # Configure basic logging format
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    print("🔇 Logging configured: Azure verbose output reduced")

def enable_debug_logging():
    """Enable debug logging for troubleshooting."""
    logging.getLogger('azure').setLevel(logging.DEBUG)
    logging.getLogger('agentic_rag').setLevel(logging.DEBUG)
    print("🔍 Debug logging enabled for troubleshooting")

def disable_all_logging():
    """Disable all logging for maximum performance."""
    logging.getLogger().setLevel(logging.ERROR)
    print("🚫 All logging disabled for maximum performance")
