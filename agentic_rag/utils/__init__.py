"""
🔧 Healthcare Agentic RAG System - Utils Module

This module contains utility scripts for Azure setup, configuration, and maintenance.
"""

# Import utility functions for easy access
from .setup_azure_search import create_search_index_and_upload_documents
from .check_azure_search import check_azure_search_index

__all__ = [
    "create_search_index_and_upload_documents",
    "check_azure_search_index", 
]
