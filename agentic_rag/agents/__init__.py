"""
🤖 Healthcare Agentic RAG System - Agents Module

This module contains all the specialized agents for the healthcare agentic RAG system.
"""

from .research_agent import create_research_agent, test_research_agent
from .analysis_agent import create_analysis_agent, test_analysis_agent
from .synthesis_agent import create_synthesis_agent, test_synthesis_agent
from .coordinator_agent import execute_multi_agent_workflow

# Connected Agents (Azure AI Foundry Connected Agents)
from .connected_research_agent import create_connected_research_agent, test_connected_research_agent
from .connected_analysis_agent import create_connected_analysis_agent, test_connected_analysis_agent
from .connected_synthesis_agent import create_connected_synthesis_agent, test_connected_synthesis_agent

__all__ = [
    # Original Agents - Python Coordinator Architecture
    "create_research_agent",
    "test_research_agent",
    "create_analysis_agent", 
    "test_analysis_agent",
    "create_synthesis_agent",
    "test_synthesis_agent",
    "execute_multi_agent_workflow",
    
    # Connected Agents - Azure AI Foundry Connected Agents Architecture
    "create_connected_research_agent",
    "test_connected_research_agent",
    "create_connected_analysis_agent",
    "test_connected_analysis_agent", 
    "create_connected_synthesis_agent",
    "test_connected_synthesis_agent",
]
