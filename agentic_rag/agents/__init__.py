"""
🤖 Healthcare Agentic RAG System - Agents Module

This module contains all the specialized agents for the healthcare agentic RAG system.
"""

from .research_agent import create_research_agent, test_research_agent
from .analysis_agent import create_analysis_agent, test_analysis_agent
from .synthesis_agent import create_synthesis_agent, test_synthesis_agent
from .coordinator_agent import create_coordinator_agent, test_coordinator_agent, execute_multi_agent_workflow

__all__ = [
    # Research Agent - Healthcare document retrieval
    "create_research_agent",
    "test_research_agent",
    
    # Analysis Agent - Data analysis and visualization
    "create_analysis_agent", 
    "test_analysis_agent",
    
    # Synthesis Agent - Response generation and communication
    "create_synthesis_agent",
    "test_synthesis_agent",
    
    # Coordinator Agent - Multi-agent workflow orchestration
    "create_coordinator_agent",
    "test_coordinator_agent", 
    "execute_multi_agent_workflow",
]
