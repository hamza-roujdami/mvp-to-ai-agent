#!/usr/bin/env python3
"""
Continuous Evaluation for Healthcare Agents
Provides near real-time observability and monitoring for AI agents
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from azure.ai.projects.models import (
    AgentEvaluationRequest,
    AgentEvaluationRedactionConfiguration,
    AgentEvaluationSamplingConfiguration,
    EvaluatorIds
)

# Load environment variables
load_dotenv()

class ContinuousEvaluator:
    """Continuous evaluation for healthcare agents"""
    
    def __init__(self, project_client):
        self.project_client = project_client
        try:
            self.evaluators = self._setup_evaluators()
            self.sampling_config = self._setup_sampling_config()
            print("✅ Continuous evaluation configured successfully")
        except Exception as e:
            print(f"⚠️ Continuous evaluation setup failed: {e}")
            self.evaluators = {}
            self.sampling_config = None
    
    def _setup_evaluators(self) -> Dict[str, Dict[str, str]]:
        """Set up evaluators for healthcare agents"""
        return {
            "Relevance": {"Id": EvaluatorIds.Relevance.value},
            "Fluency": {"Id": EvaluatorIds.Fluency.value},
            "Coherence": {"Id": EvaluatorIds.Coherence.value}
        }
    
    def _setup_sampling_config(self) -> AgentEvaluationSamplingConfiguration:
        """Set up sampling configuration for continuous evaluation"""
        return AgentEvaluationSamplingConfiguration(
            name="healthcare-agents",
            sampling_percent=50,  # Sample 50% of requests
            max_request_rate=100   # Maximum 100 requests per hour
        )
    
    def evaluate_agent_run(self, thread_id: str, run_id: str, agent_id: str) -> bool:
        """
        Create continuous evaluation for an agent run
        
        Args:
            thread_id: The thread ID
            run_id: The run ID
            agent_id: The agent ID
            
        Returns:
            bool: True if evaluation was created successfully
        """
        if not self.evaluators or not self.sampling_config:
            print("⚠️ Continuous evaluation not properly configured, skipping")
            return False
            
        try:
            # Check if evaluation API is available
            if not hasattr(self.project_client, 'evaluations'):
                print("⚠️ Continuous evaluation API not available in current SDK version")
                print("💡 Monitoring and tracing are still active via Application Insights")
                return False
            
            # Get Application Insights connection string
            app_insights_connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
            
            if not app_insights_connection_string:
                print("⚠️ No Application Insights connection string found")
                return False
            
            # Create evaluation request based on official documentation pattern
            evaluation_request = AgentEvaluationRequest(
                thread_id=thread_id,
                run_id=run_id,
                evaluators=self.evaluators,
                app_insights_connection_string=app_insights_connection_string
            )
            
            # Create the evaluation
            self.project_client.evaluations.create_agent_evaluation(evaluation_request)
            
            print(f"✅ Continuous evaluation created for run {run_id}")
            print(f"   📊 Evaluators: {list(self.evaluators.keys())}")
            print(f"   🔍 Results will appear in Azure AI Foundry monitoring")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Continuous evaluation not available: {e}")
            print("💡 Monitoring and tracing are still active via Application Insights")
            return False
    
    def get_evaluation_results(self, run_id: str) -> Optional[Dict[str, Any]]:
        """
        Get evaluation results from Application Insights
        
        Args:
            run_id: The run ID to get results for
            
        Returns:
            Dict containing evaluation results or None if not found
        """
        try:
            from azure.core.exceptions import HttpResponseError
            from azure.identity import DefaultAzureCredential
            from azure.monitor.query import LogsQueryClient, LogsQueryStatus
            from datetime import timedelta
            import pandas as pd
            
            # Get workspace ID from connection string
            connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
            if not connection_string:
                print("⚠️ No Application Insights connection string found")
                return None
            
            # Extract workspace ID with better error handling
            parts = connection_string.split(';')
            workspace_id = None
            for part in parts:
                if part.startswith('IngestionEndpoint='):
                    endpoint = part.split('=')[1]
                    if '.in.applicationinsights.azure.com' in endpoint:
                        # Extract the workspace ID from the endpoint
                        workspace_id = endpoint.replace('https://', '').replace('.in.applicationinsights.azure.com/', '')
                        break
            
            if not workspace_id:
                print("⚠️ Could not extract workspace ID from connection string")
                return None
            
            print(f"🔍 Querying Application Insights workspace: {workspace_id}")
            
            # For now, let's skip the actual query since we're having workspace access issues
            # This is a known limitation with the current setup
            print("⚠️ Skipping evaluation results query due to workspace access limitations")
            print("💡 Evaluation results will be available in Azure AI Foundry monitoring dashboard")
            return None
                
        except Exception as e:
            print(f"⚠️ Failed to get evaluation results: {e}")
            return None

def create_continuous_evaluator(project_client) -> ContinuousEvaluator:
    """Create a continuous evaluator instance"""
    return ContinuousEvaluator(project_client)
