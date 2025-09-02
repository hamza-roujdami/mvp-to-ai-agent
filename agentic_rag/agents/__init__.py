"""
Healthcare Connected Agents System

This package contains the implementation of connected agents for healthcare applications
using Azure AI Foundry's Connected Agents feature.

Agents:
- Research Agent: Searches medical information using Azure AI Search
- Analysis Agent: Analyzes data and creates visualizations using Code Interpreter
- Synthesis Agent: Creates comprehensive reports using Code Interpreter
- Orchestrator Agent: Coordinates the workflow between all agents
"""

from .research_agent import create_research_agent, test_research_agent
from .analysis_agent import create_analysis_agent, test_analysis_agent
from .synthesis_agent import create_synthesis_agent, test_synthesis_agent
from .orchestrator_agent import create_orchestrator_agent, test_orchestrator_agent

__all__ = [
    "create_research_agent",
    "test_research_agent",
    "create_analysis_agent", 
    "test_analysis_agent",
    "create_synthesis_agent",
    "test_synthesis_agent",
    "create_orchestrator_agent",
    "test_orchestrator_agent"
]