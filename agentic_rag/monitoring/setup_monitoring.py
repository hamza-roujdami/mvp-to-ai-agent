#!/usr/bin/env python3
"""
🔍 Azure AI Foundry Monitoring Setup

This module sets up comprehensive monitoring for Azure AI Foundry applications
following the official Microsoft documentation for Application Insights integration.

Reference: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/monitor-applications
"""

import os
import logging
from typing import Dict, Any, Optional
from contextlib import contextmanager

from azure.monitor.opentelemetry import configure_azure_monitor
from azure.ai.agents.telemetry import AIAgentsInstrumentor
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
# Note: Azure Core and Azure AI instrumentations may not be available in all versions
# from opentelemetry.instrumentation.azure_core import AzureCoreInstrumentor
# from opentelemetry.instrumentation.azure_ai import AzureAIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureAIFoundryMonitor:
    """
    Azure AI Foundry monitoring setup following official Microsoft documentation.
    
    This class sets up comprehensive monitoring that will appear in:
    1. Azure AI Foundry portal - Monitoring tab
    2. Azure Monitor Application Insights
    3. Application analytics dashboard
    """
    
    def __init__(self):
        """Initialize Azure AI Foundry monitoring."""
        self.tracer = None
        self._setup_monitoring()
    
    def _setup_monitoring(self):
        """Set up Azure AI Foundry monitoring with Application Insights."""
        try:
            # Get Application Insights connection string
            connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
            
            if not connection_string:
                logger.warning("APPLICATIONINSIGHTS_CONNECTION_STRING not found. Using default configuration.")
                # Try to get from Azure AI Foundry project
                connection_string = self._get_connection_string_from_project()
            
            if connection_string:
                # Create resource with proper service identification for Azure AI Foundry
                resource = Resource.create({
                    ResourceAttributes.SERVICE_NAME: "healthcare-agentic-rag",
                    ResourceAttributes.SERVICE_VERSION: "1.0.0",
                    ResourceAttributes.SERVICE_NAMESPACE: "azure-ai-foundry",
                    ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "production"
                })
                
                # Configure Azure Monitor with Application Insights
                configure_azure_monitor(
                    connection_string=connection_string,
                    resource=resource,
                    enable_live_metrics=True,
                    enable_distributed_tracing=True,
                    enable_performance_counters=True,
                    enable_dependency_tracking=True,
                    enable_request_tracking=True,
                    enable_exception_tracking=True,
                    enable_logging=True
                )
                logger.info("✅ Azure Monitor configured with Application Insights and proper resource identification")
            else:
                logger.warning("⚠️ No Application Insights connection string found. Monitoring may not work properly.")
            
            # Instrument Azure AI Agents (this is crucial for Azure AI Foundry)
            AIAgentsInstrumentor().instrument()
            logger.info("✅ Azure AI Agents instrumented for tracing")
            
            # Note: Azure Core and Azure AI instrumentations are not available in current version
            # The Azure AI Agents instrumentation should be sufficient for Azure AI Foundry
            logger.info("✅ Using Azure AI Agents instrumentation for Azure AI Foundry")
            
            # Instrument HTTP requests
            RequestsInstrumentor().instrument()
            URLLib3Instrumentor().instrument()
            logger.info("✅ HTTP requests instrumented for tracing")
            
            # Get the tracer
            self.tracer = trace.get_tracer(__name__)
            logger.info("✅ Azure AI Foundry monitoring setup completed")
            
        except Exception as e:
            logger.error(f"❌ Error setting up monitoring: {e}")
            raise
    
    def _get_connection_string_from_project(self) -> Optional[str]:
        """Get Application Insights connection string from Azure AI Foundry project."""
        try:
            from azure.ai.projects import AIProjectClient
            from azure.identity import DefaultAzureCredential
            
            project_client = AIProjectClient(
                credential=DefaultAzureCredential(),
                endpoint=os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
            )
            
            # This would need to be implemented based on the actual API
            # For now, return None to use environment variable
            return None
            
        except Exception as e:
            logger.warning(f"Could not get connection string from project: {e}")
            return None
    
    @contextmanager
    def trace_workflow(self, workflow_name: str, **attributes):
        """Trace a comprehensive workflow execution including all agents and Azure AI Search."""
        if not self.tracer:
            yield
            return
            
        with self.tracer.start_as_current_span(
            f"workflow.{workflow_name}",
            attributes={
                "workflow.name": workflow_name,
                "service.name": "healthcare-agentic-rag",
                "service.version": "1.0.0",
                "workflow.type": "multi-agent",
                "workflow.includes_azure_search": attributes.get("includes_azure_search", False),
                "workflow.total_agents": attributes.get("total_agents", 3),
                "workflow.query": attributes.get("query", ""),
                "workflow.workflow_type": attributes.get("workflow_type", "parallel"),
                "application.name": attributes.get("application_name", "healthcare-agentic-rag"),
                **attributes
            }
        ) as span:
            try:
                # Log workflow start
                span.add_event("workflow_started", {
                    "workflow_name": workflow_name,
                    "query": attributes.get("query", ""),
                    "total_agents": attributes.get("total_agents", 3)
                })
                
                yield span
                
                # Log workflow completion
                span.add_event("workflow_completed", {
                    "workflow_name": workflow_name,
                    "status": "success"
                })
                
                span.set_status(Status(StatusCode.OK))
            except Exception as e:
                # Log workflow error
                span.add_event("workflow_failed", {
                    "workflow_name": workflow_name,
                    "error": str(e)
                })
                
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise
    
    @contextmanager
    def trace_agent(self, agent_name: str, agent_type: str, **attributes):
        """Trace an agent execution with detailed Azure AI Search and tool usage."""
        if not self.tracer:
            yield
            return
            
        with self.tracer.start_as_current_span(
            f"agent.{agent_name}",
            attributes={
                "agent.name": agent_name,
                "agent.type": agent_type,
                "service.name": "healthcare-agentic-rag",
                "service.version": "1.0.0",
                "agent.agent_id": attributes.get("agent_id", ""),
                "agent.query": attributes.get("query", ""),
                "agent.includes_tools": attributes.get("includes_tools", False),
                "agent.agent_type": attributes.get("agent_type", agent_type),
                **attributes
            }
        ) as span:
            try:
                # Log agent start
                span.add_event("agent_started", {
                    "agent_name": agent_name,
                    "agent_type": agent_type,
                    "query": attributes.get("query", "")
                })
                
                yield span
                
                # Log agent completion
                span.add_event("agent_completed", {
                    "agent_name": agent_name,
                    "agent_type": agent_type,
                    "status": "success"
                })
                
                span.set_status(Status(StatusCode.OK))
            except Exception as e:
                # Log agent error
                span.add_event("agent_failed", {
                    "agent_name": agent_name,
                    "agent_type": agent_type,
                    "error": str(e)
                })
                
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise
    
    def log_custom_event(self, event_name: str, **properties):
        """Log a custom event to Application Insights."""
        if not self.tracer:
            return
            
        with self.tracer.start_as_current_span(f"event.{event_name}") as span:
            span.set_attributes({
                "event.name": event_name,
                "service.name": "healthcare-agentic-rag",
                "service.version": "1.0.0",
                **properties
            })
    
    def log_metric(self, metric_name: str, value: float, **attributes):
        """Log a custom metric to Application Insights."""
        if not self.tracer:
            return
            
        with self.tracer.start_as_current_span(f"metric.{metric_name}") as span:
            span.set_attributes({
                "metric.name": metric_name,
                "metric.value": value,
                "service.name": "healthcare-agentic-rag",
                "service.version": "1.0.0",
                **attributes
            })
    
    @contextmanager
    def trace_azure_search(self, search_query: str, index_name: str, **attributes):
        """Trace Azure AI Search operations."""
        if not self.tracer:
            yield
            return
            
        with self.tracer.start_as_current_span(
            "azure_search.query",
            attributes={
                "search.query": search_query,
                "search.index_name": index_name,
                "service.name": "healthcare-agentic-rag",
                "service.version": "1.0.0",
                "search.service": "azure_ai_search",
                **attributes
            }
        ) as span:
            try:
                # Log search start
                span.add_event("search_started", {
                    "query": search_query,
                    "index_name": index_name
                })
                
                yield span
                
                # Log search completion
                span.add_event("search_completed", {
                    "query": search_query,
                    "index_name": index_name,
                    "status": "success"
                })
                
                span.set_status(Status(StatusCode.OK))
            except Exception as e:
                # Log search error
                span.add_event("search_failed", {
                    "query": search_query,
                    "index_name": index_name,
                    "error": str(e)
                })
                
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    def set_application_context(self, application_name: str = "healthcare-agentic-rag"):
        """Set the application context for Azure AI Foundry monitoring."""
        if not self.tracer:
            return
            
        # Set application context in the current span
        current_span = trace.get_current_span()
        if current_span:
            current_span.set_attributes({
                "application.name": application_name,
                "application.type": "multi-agent-rag",
                "application.framework": "azure-ai-foundry"
            })

    def log_exception(self, exception: Exception, **context):
        """Log an exception to Application Insights."""
        if not self.tracer:
            return
            
        with self.tracer.start_as_current_span("exception") as span:
            span.set_status(Status(StatusCode.ERROR, str(exception)))
            span.record_exception(exception)
            span.set_attributes({
                "exception.type": type(exception).__name__,
                "exception.message": str(exception),
                "service.name": "healthcare-agentic-rag",
                "service.version": "1.0.0",
                **context
            })

# Global monitor instance
azure_monitor = AzureAIFoundryMonitor()

def get_monitor() -> AzureAIFoundryMonitor:
    """Get the global Azure AI Foundry monitor instance."""
    return azure_monitor

def setup_monitoring():
    """Set up Azure AI Foundry monitoring."""
    return azure_monitor

if __name__ == "__main__":
    """Test the monitoring setup."""
    print("🔍 Testing Azure AI Foundry Monitoring Setup")
    print("=" * 50)
    
    try:
        monitor = setup_monitoring()
        print("✅ Monitoring setup completed successfully")
        
        # Test tracing
        with monitor.trace_workflow("test_workflow", test_param="test_value") as span:
            print("✅ Workflow tracing test passed")
            
        with monitor.trace_agent("test_agent", "test_type", test_param="test_value") as span:
            print("✅ Agent tracing test passed")
            
        monitor.log_custom_event("test_event", test_property="test_value")
        print("✅ Custom event logging test passed")
        
        monitor.log_metric("test_metric", 42.0, test_attr="test_value")
        print("✅ Custom metric logging test passed")
        
        print("\n🎉 All monitoring tests passed!")
        print("📊 Check Azure Monitor Application Insights for data")
        
    except Exception as e:
        print(f"❌ Monitoring setup failed: {e}")
        import traceback
        traceback.print_exc()
