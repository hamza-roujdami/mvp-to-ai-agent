"""
🧪 Healthcare Agentic RAG System - Tests Module

This module contains all tests for the healthcare agentic RAG system.

Individual Agent Tests:
- test_research_agent.py: Research Agent with Azure AI Search
- test_analysis_agent.py: Analysis Agent with Code Interpreter  
- test_synthesis_agent.py: Synthesis Agent with response generation
- test_coordinator_agent.py: Coordinator Agent with multi-agent orchestration

System Tests:
- test_azure_connection.py: Azure AI Foundry connection test
"""

# Agent test modules
from . import test_research_agent
from . import test_analysis_agent
from . import test_synthesis_agent
from . import test_coordinator_agent

__all__ = [
    # Individual agent test modules
    "test_research_agent",
    "test_analysis_agent", 
    "test_synthesis_agent",
    "test_coordinator_agent",
]
