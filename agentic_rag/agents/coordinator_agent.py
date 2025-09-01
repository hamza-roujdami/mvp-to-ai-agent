#!/usr/bin/env python3
"""
🎯 Coordinator Agent - High-Performance Multi-Agent Healthcare Workflow

This coordinator implements:
1. True parallel execution of Research + Analysis agents
2. Response streaming for real-time updates
3. Advanced connection pooling and optimization
4. Intelligent workflow orchestration
"""

import os
import json
import asyncio
import concurrent.futures
import threading
import time
from typing import Dict, Any, Optional, Callable
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import MessageRole
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Import logging configuration
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_config import configure_logging

# Import agent creation functions
from .research_agent import create_research_agent
from .analysis_agent import create_analysis_agent
from .synthesis_agent import create_synthesis_agent

load_dotenv()

class CoordinatorAgent:
    """
    High-performance coordinator with true parallel execution and streaming.
    """
    
    def __init__(self):
        """Initialize the coordinator with persistent Azure client and connection pooling."""
        # Configure logging to reduce verbose Azure output
        configure_logging()
        
        # Create persistent Azure client for connection pooling
        self.project_client = AIProjectClient(
            endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
            credential=DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True
            )
        )
        
        # Cache for agent IDs - created once, reused many times
        self.agent_cache: Dict[str, str] = {}
        self.agents_initialized = False
        
        # Thread pool for parallel execution
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        
        # Performance metrics
        self.performance_metrics = {
            'total_queries': 0,
            'average_response_time': 0,
            'total_time_saved': 0
        }
    
    def initialize_agents(self):
        """Initialize all agents once and cache their IDs."""
        if self.agents_initialized:
            return
            
        print("🚀 Initializing agents (one-time setup)...")
        
        # Create and cache all agents
        research_agent, _ = create_research_agent()
        analysis_agent, _ = create_analysis_agent()
        synthesis_agent, _ = create_synthesis_agent()
        
        # Cache agent IDs for reuse
        self.agent_cache = {
            'research': research_agent.id,
            'analysis': analysis_agent.id,
            'synthesis': synthesis_agent.id
        }
        
        self.agents_initialized = True
        print(f"✅ Agents initialized and cached:")
        print(f"   Research Agent: {self.agent_cache['research']}")
        print(f"   Analysis Agent: {self.agent_cache['analysis']}")
        print(f"   Synthesis Agent: {self.agent_cache['synthesis']}")
    
    def execute_agent_with_streaming(self, agent_id: str, query: str, agent_name: str, 
                                   progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Execute an agent with streaming progress updates."""
        thread = self.project_client.agents.threads.create()
        
        try:
            # Create message
            message = self.project_client.agents.messages.create(
                thread_id=thread.id,
                role=MessageRole.USER,
                content=query,
            )
            
            if progress_callback:
                progress_callback(f"🔄 {agent_name} started...")
            
            # Run agent
            run = self.project_client.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent_id
            )
            
            # Monitor run with progress updates
            while run.status in ["queued", "in_progress"]:
                run = self.project_client.agents.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                
                if progress_callback:
                    progress_callback(f"⏳ {agent_name} processing...")
                
                time.sleep(0.5)  # Small delay to avoid excessive API calls
            
            if run.status == "completed":
                # Get response
                messages = list(self.project_client.agents.messages.list(thread_id=thread.id))
                assistant_messages = [msg for msg in messages if msg.role.value == "assistant"]
                
                if assistant_messages:
                    response = assistant_messages[-1]
                    content = self._extract_content(response.content)
                    
                    if progress_callback:
                        progress_callback(f"✅ {agent_name} completed!")
                    
                    return {
                        'status': 'completed',
                        'content': content,
                        'agent_id': agent_id
                    }
            
            return {'status': 'failed', 'content': '', 'agent_id': agent_id}
            
        finally:
            # Clean up thread
            self.project_client.agents.threads.delete(thread.id)
    
    def execute_parallel_workflow_with_streaming(self, query: str, 
                                               progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Execute the ultra-optimized parallel workflow with real-time streaming."""
        start_time = time.time()
        
        if progress_callback:
            progress_callback("🚀 Starting ultra-optimized parallel workflow...")
        
        # Ensure agents are initialized
        self.initialize_agents()
        
        # Step 1: Research Agent (must run first)
        if progress_callback:
            progress_callback("🔍 Step 1: Research Agent - Healthcare Document Retrieval")
        
        research_result = self.execute_agent_with_streaming(
            self.agent_cache['research'], 
            query, 
            "Research Agent",
            progress_callback
        )
        
        if research_result['status'] != 'completed':
            if progress_callback:
                progress_callback("❌ Research failed - stopping workflow")
            return {
                'research': research_result,
                'analysis': {'status': 'skipped', 'content': '', 'agent_id': ''},
                'synthesis': {'status': 'skipped', 'content': '', 'agent_id': ''},
                'summary': {
                    'query': query,
                    'successful_agents': 0,
                    'total_agents': 3,
                    'workflow_status': 'failed'
                }
            }
        
        if progress_callback:
            progress_callback(f"✅ Research completed: {len(research_result['content'])} characters")
        
        # Step 2: Run Analysis and Synthesis in TRUE parallel
        if progress_callback:
            progress_callback("📊 Step 2: Analysis Agent - Data Analysis & Visualization")
            progress_callback("📝 Step 3: Synthesis Agent - Response Generation")
            progress_callback("🔄 Running Analysis and Synthesis agents in parallel...")
        
        # Execute both agents simultaneously with different queries
        analysis_query = f"Analyze this healthcare research and provide insights:\n\n{research_result['content']}"
        synthesis_query = f"Synthesize this healthcare research into a patient-friendly response:\n\n{research_result['content']}"
        
        # Submit both tasks to thread pool for true parallel execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit both tasks simultaneously
            analysis_future = executor.submit(
                self.execute_agent_with_streaming,
                self.agent_cache['analysis'],
                analysis_query,
                "Analysis Agent",
                progress_callback
            )
            
            synthesis_future = executor.submit(
                self.execute_agent_with_streaming,
                self.agent_cache['synthesis'],
                synthesis_query,
                "Synthesis Agent",
                progress_callback
            )
            
            # Wait for both to complete (they run in parallel)
            analysis_result = analysis_future.result()
            synthesis_result = synthesis_future.result()
            
            if progress_callback:
                progress_callback(f"✅ Analysis completed: {analysis_result['status']}")
                progress_callback(f"✅ Synthesis completed: {synthesis_result['status']}")
                progress_callback(f"   Content length: {len(synthesis_result['content'])} characters")
        
        # Step 4: Workflow Summary
        if progress_callback:
            progress_callback("🎯 Step 4: Multi-Agent Workflow Summary")
        
        successful_agents = sum(1 for result in [research_result, analysis_result, synthesis_result] 
                              if result['status'] == 'completed')
        
        workflow_status = 'completed' if successful_agents == 3 else 'partial'
        
        if progress_callback:
            progress_callback(f"✅ Multi-Agent Workflow {workflow_status}!")
            progress_callback(f"   Successful agents: {successful_agents}/3")
            progress_callback(f"   Workflow status: {workflow_status}")
        
        # Calculate performance metrics
        end_time = time.time()
        duration = end_time - start_time
        
        # Update performance metrics
        self.performance_metrics['total_queries'] += 1
        self.performance_metrics['average_response_time'] = (
            (self.performance_metrics['average_response_time'] * (self.performance_metrics['total_queries'] - 1) + duration) 
            / self.performance_metrics['total_queries']
        )
        
        if progress_callback:
            progress_callback(f"⏱️  Total execution time: {duration:.2f} seconds")
            progress_callback(f"📊 Average response time: {self.performance_metrics['average_response_time']:.2f} seconds")
        
        return {
            'research': research_result,
            'analysis': analysis_result,
            'synthesis': synthesis_result,
            'summary': {
                'query': query,
                'successful_agents': successful_agents,
                'total_agents': 3,
                'workflow_status': workflow_status,
                'execution_time': duration
            }
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        return self.performance_metrics.copy()
    
    def _extract_content(self, content) -> str:
        """Extract text content from agent response."""
        if isinstance(content, list) and len(content) > 0:
            for content_item in content:
                if isinstance(content_item, dict):
                    if content_item.get('type') == 'text':
                        return content_item.get('text', {}).get('value', '')
        return str(content)
    
    def __del__(self):
        """Cleanup when coordinator is destroyed."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=True)

# Global coordinator instance for reuse
_global_coordinator = None

def get_coordinator() -> CoordinatorAgent:
    """Get or create the global coordinator instance."""
    global _global_coordinator
    if _global_coordinator is None:
        _global_coordinator = CoordinatorAgent()
    return _global_coordinator

def execute_multi_agent_workflow(query: str, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
    """Execute the multi-agent workflow."""
    coordinator = get_coordinator()
    return coordinator.execute_parallel_workflow_with_streaming(query, progress_callback)
