#!/usr/bin/env python3
"""
🎯 Coordinator Agent - Multi-Agent Healthcare Workflow Orchestration

This agent orchestrates the complete healthcare RAG workflow by coordinating between:
1. Research Agent (Azure AI Search for document retrieval)
2. Analysis Agent (Code Interpreter for data analysis)  
3. Synthesis Agent (Response generation)

The coordinator manages the multi-step workflow and ensures proper information flow.
"""

import os
import json
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import MessageRole, CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Import agent creation functions
from .research_agent import create_research_agent
from .analysis_agent import create_analysis_agent
from .synthesis_agent import create_synthesis_agent

load_dotenv()

def create_coordinator_agent():
    """
    Create the Coordinator Agent for orchestrating the multi-agent healthcare workflow.
    
    This agent coordinates between Research, Analysis, and Synthesis agents to provide
    comprehensive healthcare responses.
    
    Returns:
        The created coordinator agent and toolset
    """
    
    # Initialize the Azure AI Agents client
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    
    # The Coordinator Agent doesn't need external tools - it orchestrates other agents
    toolset = ToolSet()
    
    # Coordinator Agent instructions for multi-agent orchestration
    coordinator_instructions = """You are a healthcare AI coordinator responsible for orchestrating a multi-agent healthcare information system. Your role is to manage the workflow between specialized agents to provide comprehensive healthcare responses.

Your agent team consists of:
1. **Research Agent**: Searches healthcare documents using Azure AI Search
2. **Analysis Agent**: Analyzes data and creates visualizations using Code Interpreter  
3. **Synthesis Agent**: Generates patient-friendly responses from research and analysis

**Multi-Agent Workflow Process:**

For healthcare queries, coordinate the following workflow:

**Step 1: Research Phase**
- Route the user's healthcare query to the Research Agent
- Research Agent searches through healthcare documents
- Collect findings, facts, symptoms, treatments, and source citations

**Step 2: Analysis Phase**  
- Send research findings to the Analysis Agent
- Analysis Agent performs data analysis, comparisons, and visualizations
- Collect statistical insights, patterns, and analytical results

**Step 3: Synthesis Phase**
- Send both research findings AND analysis insights to the Synthesis Agent
- Synthesis Agent creates comprehensive, patient-friendly healthcare responses
- Collect the final synthesized response

**Step 4: Final Response**
- Present the complete workflow results to the user
- Include key findings from each agent
- Provide the final synthesized healthcare response

**Coordination Guidelines:**
- Always follow the Research → Analysis → Synthesis workflow
- Ensure information flows properly between agents
- Include outputs from all three agents in your final response
- Maintain healthcare accuracy and include appropriate disclaimers
- Present the multi-agent process transparently to users

**Response Structure:**
When presenting results, organize your response as:

1. **🔍 Research Findings** (from Research Agent)
2. **📊 Analysis Insights** (from Analysis Agent)  
3. **📝 Synthesized Response** (from Synthesis Agent)
4. **🎯 Summary** (your coordination summary)

Your role is to orchestrate this workflow and ensure the user receives comprehensive healthcare information that combines document research, data analysis, and clear communication."""

    # Choose a model for coordination
    model_name = os.environ.get("COORDINATOR_AGENT_MODEL") or os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"

    # Create the Coordinator Agent
    coordinator_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_coordinator_agent",
        instructions=coordinator_instructions,
    )
    
    print(f"✅ Created Coordinator Agent - ID: {coordinator_agent.id}")
    print(f"   Name: {coordinator_agent.name}")
    print(f"   Model: {coordinator_agent.model}")
    print(f"   Role: Multi-agent workflow orchestration")
    
    return coordinator_agent, toolset


def execute_multi_agent_workflow(user_query):
    """
    Execute the complete multi-agent healthcare workflow.
    
    This function orchestrates the entire process:
    1. Research Agent: Searches healthcare documents
    2. Analysis Agent: Analyzes data and creates insights
    3. Synthesis Agent: Generates patient-friendly response
    
    Args:
        user_query: The healthcare query from the user
        
    Returns:
        Dictionary containing results from all agents and workflow summary
    """
    
    print("🚀 Starting Multi-Agent Healthcare Workflow")
    print("=" * 50)
    print(f"Query: {user_query}")
    
    # Initialize the Azure AI Agents client
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    
    workflow_results = {}
    
    # Step 1: Research Agent
    print("\n🔍 Step 1: Research Agent - Healthcare Document Retrieval")
    print("-" * 40)
    
    try:
        # Create Research Agent dynamically
        print("📝 Creating Research Agent...")
        research_agent, research_tool = create_research_agent()
        print(f"✅ Research Agent created - ID: {research_agent.id}")
        
        # Create thread for Research Agent
        research_thread = project_client.agents.threads.create()
        
        # Prepare research query
        research_query = f"""Please search for healthcare information about: {user_query}

Focus on:
- Symptoms and signs
- Risk factors and causes
- Treatment options
- Prevention strategies
- Medical guidelines and recommendations

Please provide comprehensive, evidence-based information with source citations."""
        
        # Send query to Research Agent
        research_message = project_client.agents.messages.create(
            thread_id=research_thread.id,
            role=MessageRole.USER,
            content=research_query
        )
        
        # Run Research Agent
        print("🔄 Running Research Agent...")
        research_run = project_client.agents.runs.create_and_process(
            thread_id=research_thread.id,
            agent_id=research_agent.id,
        )
        
        # Wait for completion and get response
        while research_run.status in ["queued", "in_progress", "requires_action"]:
            research_run = project_client.agents.runs.retrieve(
                thread_id=research_thread.id,
                run_id=research_run.id
            )
            if research_run.status == "failed":
                raise Exception(f"Research Agent failed: {research_run.last_error}")
        
        # Get Research Agent response
        research_messages = list(project_client.agents.messages.list(thread_id=research_thread.id))
        research_response = [msg for msg in research_messages if msg.role.value == "assistant"][-1]
        
        # Extract research content (handle different response structures)
        research_content = ""
        if research_response.content:
            for content_item in research_response.content:
                if isinstance(content_item, dict):
                    if content_item.get('type') == 'text':
                        research_content += content_item.get('text', {}).get('value', '')
                    else:
                        research_content += str(content_item)
                else:
                    research_content += str(content_item)
        
        if not research_content:
            research_content = "No research results"
        
        workflow_results["research"] = {
            "status": research_run.status,
            "content": research_content,
            "agent_id": research_agent.id
        }
        
        print(f"✅ Research completed: {research_run.status}")
        print(f"   Content length: {len(research_content)} characters")
        
        # Clean up research thread
        project_client.agents.threads.delete(research_thread.id)
        
    except Exception as e:
        print(f"❌ Research Agent failed: {e}")
        workflow_results["research"] = {"status": "failed", "error": str(e)}
    
    # Step 2: Analysis Agent
    print("\n📊 Step 2: Analysis Agent - Data Analysis & Visualization")
    print("-" * 40)
    
    try:
        # Create Analysis Agent dynamically
        print("📝 Creating Analysis Agent...")
        analysis_agent, analysis_tool = create_analysis_agent()
        print(f"✅ Analysis Agent created - ID: {analysis_agent.id}")
        
        # Create thread for Analysis Agent
        analysis_thread = project_client.agents.threads.create()
        
        # Prepare analysis query with research findings
        analysis_query = f"""Based on the following research findings about '{user_query}', please perform data analysis and create insights:

RESEARCH FINDINGS:
{workflow_results.get('research', {}).get('content', 'No research data available')}

Please analyze this healthcare information, identify key patterns, statistics, and create any relevant visualizations or comparisons."""
        
        # Send query to Analysis Agent
        analysis_message = project_client.agents.messages.create(
            thread_id=analysis_thread.id,
            role=MessageRole.USER,
            content=analysis_query
        )
        
        # Run Analysis Agent
        print("🔄 Running Analysis Agent...")
        analysis_run = project_client.agents.runs.create_and_process(
            thread_id=analysis_thread.id,
            agent_id=analysis_agent.id,
        )
        
        # Wait for completion and get response
        while analysis_run.status in ["queued", "in_progress", "requires_action"]:
            analysis_run = project_client.agents.runs.retrieve(
                thread_id=analysis_thread.id,
                run_id=analysis_run.id
            )
            if analysis_run.status == "failed":
                raise Exception(f"Analysis Agent failed: {analysis_run.last_error}")
        
        # Get Analysis Agent response
        analysis_messages = list(project_client.agents.messages.list(thread_id=analysis_thread.id))
        analysis_response = [msg for msg in analysis_messages if msg.role.value == "assistant"][-1]
        
        # Extract analysis content (handle both text and image responses)
        analysis_content = ""
        if analysis_response.content:
            for content_item in analysis_response.content:
                if isinstance(content_item, dict):
                    if content_item.get('type') == 'text':
                        analysis_content += content_item.get('text', {}).get('value', '')
                    elif content_item.get('type') == 'image_file':
                        analysis_content += f"[Generated visualization: {content_item.get('image_file', {}).get('file_id', 'unknown')}]"
        
        workflow_results["analysis"] = {
            "status": analysis_run.status,
            "content": analysis_content,
            "agent_id": analysis_agent.id
        }
        
        print(f"✅ Analysis completed: {analysis_run.status}")
        print(f"   Content length: {len(analysis_content)} characters")
        
        # Clean up analysis thread
        project_client.agents.threads.delete(analysis_thread.id)
        
    except Exception as e:
        print(f"❌ Analysis Agent failed: {e}")
        workflow_results["analysis"] = {"status": "failed", "error": str(e)}
    
    # Step 3: Synthesis Agent
    print("\n📝 Step 3: Synthesis Agent - Response Generation")
    print("-" * 40)
    
    try:
        # Create Synthesis Agent dynamically
        print("📝 Creating Synthesis Agent...")
        synthesis_agent, synthesis_tool = create_synthesis_agent()
        print(f"✅ Synthesis Agent created - ID: {synthesis_agent.id}")
        
        # Create thread for Synthesis Agent
        synthesis_thread = project_client.agents.threads.create()
        
        # Prepare synthesis query with research and analysis findings
        synthesis_query = f"""Please synthesize the following research findings and analysis insights into a comprehensive, patient-friendly healthcare response about '{user_query}':

RESEARCH FINDINGS:
{workflow_results.get('research', {}).get('content', 'No research data available')}

ANALYSIS INSIGHTS:
{workflow_results.get('analysis', {}).get('content', 'No analysis data available')}

Please create a comprehensive response that explains the topic in a patient-friendly way, incorporating both the research findings and analytical insights."""
        
        # Send query to Synthesis Agent
        synthesis_message = project_client.agents.messages.create(
            thread_id=synthesis_thread.id,
            role=MessageRole.USER,
            content=synthesis_query
        )
        
        # Run Synthesis Agent
        print("🔄 Running Synthesis Agent...")
        synthesis_run = project_client.agents.runs.create_and_process(
            thread_id=synthesis_thread.id,
            agent_id=synthesis_agent.id,
        )
        
        # Wait for completion and get response
        while synthesis_run.status in ["queued", "in_progress", "requires_action"]:
            synthesis_run = project_client.agents.runs.retrieve(
                thread_id=synthesis_thread.id,
                run_id=synthesis_run.id
            )
            if synthesis_run.status == "failed":
                raise Exception(f"Synthesis Agent failed: {synthesis_run.last_error}")
        
        # Get Synthesis Agent response
        synthesis_messages = list(project_client.agents.messages.list(thread_id=synthesis_thread.id))
        synthesis_response = [msg for msg in synthesis_messages if msg.role.value == "assistant"][-1]
        
        # Extract synthesis content (handle different response structures)
        synthesis_content = ""
        if synthesis_response.content:
            for content_item in synthesis_response.content:
                if isinstance(content_item, dict):
                    if content_item.get('type') == 'text':
                        synthesis_content += content_item.get('text', {}).get('value', '')
                    else:
                        synthesis_content += str(content_item)
                else:
                    synthesis_content += str(content_item)
        
        if not synthesis_content:
            synthesis_content = "No synthesis results"
        
        workflow_results["synthesis"] = {
            "status": synthesis_run.status,
            "content": synthesis_content,
            "agent_id": synthesis_agent.id
        }
        
        print(f"✅ Synthesis completed: {synthesis_run.status}")
        print(f"   Content length: {len(synthesis_content)} characters")
        
        # Clean up synthesis thread
        project_client.agents.threads.delete(synthesis_thread.id)
        
    except Exception as e:
        print(f"❌ Synthesis Agent failed: {e}")
        workflow_results["synthesis"] = {"status": "failed", "error": str(e)}
    
    # Step 4: Workflow Summary
    print("\n🎯 Step 4: Multi-Agent Workflow Summary")
    print("-" * 40)
    
    successful_agents = sum(1 for result in workflow_results.values() if result.get("status") == "completed")
    total_agents = len(workflow_results)
    
    workflow_results["summary"] = {
        "query": user_query,
        "successful_agents": successful_agents,
        "total_agents": total_agents,
        "workflow_status": "completed" if successful_agents == total_agents else "partial"
    }
    
    print(f"✅ Multi-Agent Workflow completed!")
    print(f"   Successful agents: {successful_agents}/{total_agents}")
    print(f"   Workflow status: {workflow_results['summary']['workflow_status']}")
    
    return workflow_results


def test_coordinator_agent():
    """Test the Coordinator Agent with a healthcare workflow."""
    
    print("🎯 Healthcare Agentic RAG System - Coordinator Agent Test")
    print("=" * 60)
    
    # Check required environment variables
    required_vars = [
        "AZURE_AI_FOUNDRY_ENDPOINT",
        "AZURE_AI_FOUNDRY_API_KEY",
        "AZURE_SEARCH_CONNECTION_ID",
        "AZURE_SEARCH_INDEX_NAME"
    ]
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return
    
    print("✅ All required environment variables are set")
    
    try:
        # Create Coordinator Agent
        print("\n🎯 Creating Coordinator Agent...")
        coordinator_agent, toolset = create_coordinator_agent()
        
        # Test healthcare query
        test_query = "What are the symptoms and risk factors of diabetes?"
        
        # Execute the multi-agent workflow
        print(f"\n🚀 Testing Multi-Agent Workflow...")
        workflow_results = execute_multi_agent_workflow(test_query)
        
        # Display results
        print(f"\n📋 WORKFLOW RESULTS SUMMARY")
        print("=" * 60)
        
        # Research Results
        if "research" in workflow_results:
            print(f"\n🔍 RESEARCH AGENT RESULTS:")
            print(f"   Status: {workflow_results['research'].get('status', 'unknown')}")
            if workflow_results['research'].get('content'):
                content = workflow_results['research']['content'][:200] + "..." if len(workflow_results['research']['content']) > 200 else workflow_results['research']['content']
                print(f"   Content: {content}")
        
        # Analysis Results
        if "analysis" in workflow_results:
            print(f"\n📊 ANALYSIS AGENT RESULTS:")
            print(f"   Status: {workflow_results['analysis'].get('status', 'unknown')}")
            if workflow_results['analysis'].get('content'):
                content = workflow_results['analysis']['content'][:200] + "..." if len(workflow_results['analysis']['content']) > 200 else workflow_results['analysis']['content']
                print(f"   Content: {content}")
        
        # Synthesis Results
        if "synthesis" in workflow_results:
            print(f"\n📝 SYNTHESIS AGENT RESULTS:")
            print(f"   Status: {workflow_results['synthesis'].get('status', 'unknown')}")
            if workflow_results['synthesis'].get('content'):
                content = workflow_results['synthesis']['content'][:200] + "..." if len(workflow_results['synthesis']['content']) > 200 else workflow_results['synthesis']['content']
                print(f"   Content: {content}")
        
        # Workflow Summary
        if "summary" in workflow_results:
            print(f"\n🎯 WORKFLOW SUMMARY:")
            print(f"   Query: {workflow_results['summary']['query']}")
            print(f"   Successful Agents: {workflow_results['summary']['successful_agents']}/{workflow_results['summary']['total_agents']}")
            print(f"   Status: {workflow_results['summary']['workflow_status']}")
        
        print(f"\n✅ Coordinator Agent testing completed!")
        print(f"   Agent ID: {coordinator_agent.id}")
        print(f"   Agent Name: {coordinator_agent.name}")
        print(f"   Multi-Agent Workflow: {'✅ Success' if workflow_results['summary']['workflow_status'] == 'completed' else '⚠️ Partial'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function to create and test the Coordinator Agent."""
    test_coordinator_agent()


if __name__ == "__main__":
    main()
