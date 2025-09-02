#!/usr/bin/env python3
"""
🎯 Clean Azure AI Foundry Tracing

Simple, focused tracing for agents and end-to-end user query flow.
"""

import os
import time
from contextlib import contextmanager
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

from azure.monitor.opentelemetry import configure_azure_monitor
from azure.ai.agents.telemetry import AIAgentsInstrumentor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CleanTracing:
    """Clean, simple tracing for Azure AI Foundry agents."""
    
    def __init__(self):
        self.tracer = None
        self._setup_tracing()
    
    def _setup_tracing(self):
        """Set up clean tracing for Azure AI Foundry."""
        try:
            # Enable detailed content recording for traces
            os.environ["AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED"] = "true"
            
            # Get Application Insights connection string
            connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
            
            if connection_string:
                # Create resource with clean identification
                resource = Resource.create({
                    ResourceAttributes.SERVICE_NAME: "healthcare-agents",
                    ResourceAttributes.SERVICE_VERSION: "1.0.0",
                    ResourceAttributes.SERVICE_NAMESPACE: "azure-ai-foundry",
                    ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "production"
                })
                
                # Configure Azure Monitor
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
                
                # Instrument Azure AI Agents
                AIAgentsInstrumentor().instrument()
                
                # Get tracer
                self.tracer = trace.get_tracer("healthcare-agents")
                
                print("✅ Clean tracing configured successfully")
            else:
                print("⚠️ No Application Insights connection string found")
                
        except Exception as e:
            print(f"❌ Tracing setup failed: {e}")
    
    @contextmanager
    def trace_user_query(self, query: str, user_id: str = "user"):
        """Trace the complete user query workflow."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("user_query_workflow") as span:
            span.set_attributes({
                "user.query": query,
                "user.id": user_id,
                "workflow.type": "healthcare_multi_agent",
                "trace.category": "end_to_end"
            })
            
            print(f"🎯 Tracing user query: '{query[:50]}...'")
            yield span
    
    @contextmanager
    def trace_orchestrator(self, query: str):
        """Trace orchestrator agent execution with connected agents."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("orchestrator_agent") as span:
            span.set_attributes({
                "agent.type": "orchestrator",
                "agent.role": "workflow_coordination",
                "input.query": query,
                "trace.category": "agent_execution"
            })
            
            print("🎭 Tracing orchestrator agent")
            
            # Trace connected agents execution
            with self.trace_connected_agents_workflow(query) as connected_span:
                yield span
    
    @contextmanager
    def trace_connected_agents_workflow(self, query: str):
        """Trace the complete connected agents workflow."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("connected_agents_workflow") as span:
            span.set_attributes({
                "workflow.type": "connected_agents",
                "input.query": query,
                "trace.category": "multi_agent_workflow"
            })
            
            print("🔗 Tracing connected agents workflow")
            
            # Phase 1: Research Agent with Azure AI Search
            with self.trace_research_agent_with_search(query) as research_span:
                pass
            
            # Phase 2: Analysis Agent with Code Interpreter
            with self.trace_analysis_agent_with_tools(query) as analysis_span:
                pass
            
            # Phase 3: Synthesis Agent with Code Interpreter
            with self.trace_synthesis_agent_with_tools(query) as synthesis_span:
                pass
            
            yield span
    
    @contextmanager
    def trace_research_agent_with_search(self, query: str):
        """Trace research agent with Azure AI Search tool usage."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("research_agent_with_search") as span:
            span.set_attributes({
                "agent.type": "research",
                "agent.role": "document_retrieval",
                "input.query": query,
                "trace.category": "agent_with_tools"
            })
            
            print("🔍 Tracing research agent with Azure AI Search")
            
            # Trace Azure AI Search tool usage
            with self.trace_azure_ai_search_tool(query) as search_span:
                yield span
    
    @contextmanager
    def trace_analysis_agent_with_tools(self, query: str):
        """Trace analysis agent with Code Interpreter tool usage."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("analysis_agent_with_tools") as span:
            span.set_attributes({
                "agent.type": "analysis",
                "agent.role": "data_analysis",
                "input.query": query,
                "trace.category": "agent_with_tools"
            })
            
            print("📊 Tracing analysis agent with Code Interpreter")
            
            # Trace Code Interpreter tool usage
            with self.trace_code_interpreter_tool("data_analysis", query) as code_span:
                yield span
    
    @contextmanager
    def trace_synthesis_agent_with_tools(self, query: str):
        """Trace synthesis agent with Code Interpreter tool usage."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("synthesis_agent_with_tools") as span:
            span.set_attributes({
                "agent.type": "synthesis",
                "agent.role": "report_generation",
                "input.query": query,
                "trace.category": "agent_with_tools"
            })
            
            print("📝 Tracing synthesis agent with Code Interpreter")
            
            # Trace Code Interpreter tool usage
            with self.trace_code_interpreter_tool("report_generation", query) as code_span:
                yield span
    
    @contextmanager
    def trace_azure_ai_search_tool(self, query: str):
        """Trace Azure AI Search tool execution."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("azure_ai_search_tool") as span:
            span.set_attributes({
                "tool.type": "azure_ai_search",
                "tool.operation": "search_documents",
                "search.query": query,
                "search.index": "healthcare-index",
                "trace.category": "tool_execution"
            })
            
            print("🔍 Tracing Azure AI Search tool execution")
            yield span
    
    @contextmanager
    def trace_code_interpreter_tool(self, operation: str, context: str):
        """Trace Code Interpreter tool execution."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("code_interpreter_tool") as span:
            span.set_attributes({
                "tool.type": "code_interpreter",
                "tool.operation": operation,
                "code.context": context,
                "code.language": "python",
                "trace.category": "tool_execution"
            })
            
            print(f"💻 Tracing Code Interpreter tool: {operation}")
            yield span
    
    @contextmanager
    def trace_research_agent(self, query: str):
        """Trace research agent execution."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("research_agent") as span:
            span.set_attributes({
                "agent.type": "research",
                "agent.role": "document_retrieval",
                "input.query": query,
                "tool.used": "azure_ai_search",
                "trace.category": "agent_execution"
            })
            
            print("🔍 Tracing research agent")
            yield span
    
    @contextmanager
    def trace_analysis_agent(self, data_type: str = "healthcare_data"):
        """Trace analysis agent execution."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("analysis_agent") as span:
            span.set_attributes({
                "agent.type": "analysis",
                "agent.role": "data_analysis",
                "input.data_type": data_type,
                "tool.used": "code_interpreter",
                "trace.category": "agent_execution"
            })
            
            print("📊 Tracing analysis agent")
            yield span
    
    @contextmanager
    def trace_synthesis_agent(self, components: int = 3):
        """Trace synthesis agent execution."""
        if not self.tracer:
            yield None
            return
            
        with self.tracer.start_as_current_span("synthesis_agent") as span:
            span.set_attributes({
                "agent.type": "synthesis",
                "agent.role": "report_generation",
                "input.components": components,
                "tool.used": "code_interpreter",
                "trace.category": "agent_execution"
            })
            
            print("📝 Tracing synthesis agent")
            yield span
    
    def log_workflow_completion(self, success: bool, duration_ms: float, agents_used: int):
        """Log workflow completion metrics."""
        if not self.tracer:
            return
            
        with self.tracer.start_as_current_span("workflow_completion") as span:
            span.set_attributes({
                "workflow.success": success,
                "workflow.duration_ms": duration_ms,
                "workflow.agents_used": agents_used,
                "trace.category": "workflow_metrics"
            })
            
            print(f"📊 Workflow completed: success={success}, duration={duration_ms}ms, agents={agents_used}")

# Global tracing instance
clean_tracing = CleanTracing()

def get_tracing():
    """Get the global tracing instance."""
    return clean_tracing

if __name__ == "__main__":
    """Test the clean tracing setup."""
    print("🎯 Testing Clean Tracing Setup")
    print("=" * 50)
    
    try:
        tracing = get_tracing()
        
        # Test end-to-end workflow trace
        with tracing.trace_user_query("What are the symptoms of diabetes?", "test-user") as main_span:
            # Test orchestrator trace
            with tracing.trace_orchestrator("What are the symptoms of diabetes?") as orch_span:
                time.sleep(0.1)  # Simulate processing
            
            # Test research agent trace
            with tracing.trace_research_agent("diabetes symptoms") as research_span:
                time.sleep(0.2)  # Simulate search
            
            # Test analysis agent trace
            with tracing.trace_analysis_agent("diabetes_data") as analysis_span:
                time.sleep(0.3)  # Simulate analysis
            
            # Test synthesis agent trace
            with tracing.trace_synthesis_agent(4) as synthesis_span:
                time.sleep(0.2)  # Simulate synthesis
            
            # Log completion
            tracing.log_workflow_completion(True, 800.0, 4)
        
        print("\n🎉 Clean tracing test completed successfully!")
        print("📊 Check Azure AI Foundry portal for clean traces")
        
    except Exception as e:
        print(f"❌ Clean tracing test failed: {e}")
        import traceback
        traceback.print_exc()
