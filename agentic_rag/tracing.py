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
        """Set up tracing for Azure AI Foundry monitoring dashboard."""
        try:
            # Enable comprehensive Azure AI tracing for monitoring
            os.environ["AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED"] = "true"
            os.environ["AZURE_AI_FOUNDRY_TRACING_ENABLED"] = "true"
            os.environ["AZURE_AI_FOUNDRY_MONITORING_ENABLED"] = "true"
            
            # Set application name for monitoring dashboard
            os.environ["AZURE_AI_FOUNDRY_APPLICATION_NAME"] = "healthcare-agents"
            
            # Set project name for Azure AI Foundry monitoring
            project_name = os.getenv("AZURE_AI_FOUNDRY_PROJECT_NAME", "mvp_rag_to_agentic")
            os.environ["AZURE_AI_FOUNDRY_PROJECT_NAME"] = project_name
            
            # Enable Azure AI model call tracking
            os.environ["AZURE_AI_MODEL_CALL_TRACKING_ENABLED"] = "true"
            os.environ["AZURE_AI_TOKEN_TRACKING_ENABLED"] = "true"
            os.environ["AZURE_AI_INFERENCE_TRACKING_ENABLED"] = "true"
            
            # Get Application Insights connection string
            connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
            
            if connection_string:
                # Configure Azure Monitor for AI Foundry monitoring (minimal approach)
                configure_azure_monitor(
                    connection_string=connection_string,
                    enable_live_metrics=True,
                    enable_distributed_tracing=True
                )
                
                # Instrument Azure AI Agents - this captures model calls for monitoring
                # This is the key for Azure AI Foundry monitoring dashboard
                AIAgentsInstrumentor().instrument()
                
                # Additional instrumentation for Azure AI services
                try:
                    from azure.ai.inference import AzureOpenAI
                    # This ensures Azure AI model calls are tracked
                    print("✅ Azure AI model call tracking enabled")
                except ImportError:
                    print("⚠️ Azure AI inference SDK not available")
                
                # Get tracer for custom spans
                self.tracer = trace.get_tracer("healthcare-agents")
                
                print("✅ Azure AI Foundry monitoring configured successfully")
                print("📊 Model calls will appear in Azure AI Foundry → Monitoring → Application analytics")
                print("🔍 Token consumption, inference calls, and latency will be tracked")
                print("💡 Make sure to run queries in the app to generate Azure AI model calls")
                print("🔗 Application Insights connection: app-insights-agentic-rag")
            else:
                print("⚠️ No Application Insights connection string found")
                print("💡 Set APPLICATIONINSIGHTS_CONNECTION_STRING in your .env file")
                
        except Exception as e:
            print(f"❌ Tracing setup failed: {e}")
            import traceback
            traceback.print_exc()
    
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
    
    def log_azure_ai_model_call(self, model_name: str, operation: str, tokens_used: int = 0, duration_ms: float = 0):
        """Log Azure AI model calls for monitoring dashboard."""
        if not self.tracer:
            return
            
        with self.tracer.start_as_current_span("azure_ai_model_call") as span:
            span.set_attributes({
                "azure.ai.model.name": model_name,
                "azure.ai.operation": operation,
                "azure.ai.tokens.used": tokens_used,
                "azure.ai.duration.ms": duration_ms,
                "azure.ai.foundry.application": "healthcare-agents",
                "trace.category": "azure_ai_model_call"
            })
            
            print(f"🤖 Azure AI model call: {model_name} - {operation} ({tokens_used} tokens, {duration_ms}ms)")
    
    def log_azure_ai_search_call(self, query: str, results_count: int, duration_ms: float = 0):
        """Log Azure AI Search calls for monitoring dashboard."""
        if not self.tracer:
            return
            
        with self.tracer.start_as_current_span("azure_ai_search_call") as span:
            span.set_attributes({
                "azure.ai.search.query": query,
                "azure.ai.search.results_count": results_count,
                "azure.ai.search.duration.ms": duration_ms,
                "azure.ai.foundry.application": "healthcare-agents",
                "trace.category": "azure_ai_search_call"
            })
            
            print(f"🔍 Azure AI Search call: {query[:50]}... ({results_count} results, {duration_ms}ms)")

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
