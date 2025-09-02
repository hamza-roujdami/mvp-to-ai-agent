"""
Healthcare Orchestrator Agent - Connected Agents Implementation
Main orchestrator that coordinates the workflow between specialized agents
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ConnectedAgentTool, MessageRole
from azure.identity import DefaultAzureCredential

from .research_agent import create_research_agent
from .analysis_agent import create_analysis_agent
from .synthesis_agent import create_synthesis_agent


def create_orchestrator_agent(project_client=None, model_name=None):
    """
    Create the main orchestrator agent that coordinates connected agents.
    
    Args:
        project_client: Optional AIProjectClient instance
        model_name: Optional model name override
        
    Returns:
        dict: Dictionary containing all agents and tools
    """
    if project_client is None:
        project_client = AIProjectClient(
            endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
    
    if model_name is None:
        model_name = os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"
    
    # Create the connected agents first
    research_agent, search_tool = create_research_agent(project_client, model_name)
    analysis_agent, analysis_tool = create_analysis_agent(project_client, model_name)
    synthesis_agent, synthesis_tool = create_synthesis_agent(project_client, model_name)
    
    # Create ConnectedAgentTool definitions
    research_connected_tool = ConnectedAgentTool(
        id=research_agent.id,
        name=research_agent.name,
        description="Searches for relevant medical information and research data using Azure AI Search"
    )
    
    analysis_connected_tool = ConnectedAgentTool(
        id=analysis_agent.id,
        name=analysis_agent.name,
        description="Analyzes healthcare data, creates visualizations, and performs statistical analysis"
    )
    
    synthesis_connected_tool = ConnectedAgentTool(
        id=synthesis_agent.id,
        name=synthesis_agent.name,
        description="Synthesizes research findings and creates comprehensive healthcare reports with visual summaries"
    )
    
    # Create the main orchestrator agent
    orchestrator_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_orchestrator",
        instructions="""You are a healthcare AI orchestrator. Your job is to coordinate a team of specialized healthcare agents to provide comprehensive medical information and analysis.

Available connected agents:
1. healthcare_research_agent: Searches for medical information and research data
2. healthcare_analysis_agent: Analyzes data and creates visualizations
3. healthcare_synthesis_agent: Synthesizes findings and creates reports

Workflow:
1. For any healthcare query, first delegate to the research_agent to gather relevant information
2. Then delegate to the analysis_agent to analyze the data and create visualizations
3. Finally, delegate to the synthesis_agent to create a comprehensive, patient-friendly response

Always coordinate between all three agents to provide the most complete and helpful response.""",
        tools=research_connected_tool.definitions + analysis_connected_tool.definitions + synthesis_connected_tool.definitions,
    )
    
    return {
        "orchestrator": orchestrator_agent,
        "research_agent": research_agent,
        "analysis_agent": analysis_agent,
        "synthesis_agent": synthesis_agent,
        "connected_tools": {
            "research": research_connected_tool,
            "analysis": analysis_connected_tool,
            "synthesis": synthesis_connected_tool
        }
    }


def test_orchestrator_agent():
    """Test the orchestrator agent with a comprehensive healthcare query."""
    try:
        # Create the orchestrator and connected agents
        agents = create_orchestrator_agent()
        orchestrator_agent = agents["orchestrator"]
        
        # Initialize client for testing
        project_client = AIProjectClient(
            endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
        
        # Create a thread and test query
        thread = project_client.agents.threads.create()
        test_query = "What are the latest treatments for diabetes? Please provide research, analysis, and a comprehensive summary."
        
        # Add test message
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=test_query,
        )
        
        # Run the orchestrator agent
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id, 
            agent_id=orchestrator_agent.id
        )
        
        if run.status == "completed":
            # Get the response
            messages = project_client.agents.messages.list(thread_id=thread.id)
            messages_list = list(messages)
            
            # Find the latest assistant message
            assistant_messages = [msg for msg in messages_list if str(msg.role) == "MessageRole.AGENT"]
            
            if assistant_messages:
                response_message = assistant_messages[-1]
                response_content = ""
                
                if hasattr(response_message, 'content') and response_message.content:
                    for content_item in response_message.content:
                        if hasattr(content_item, 'text'):
                            text_content = content_item.text
                            if hasattr(text_content, 'value'):
                                text_value = text_content.value
                                if text_value and text_value.strip() != "ASSISTANT":
                                    response_content += text_value + "\n"
                            else:
                                if text_content and str(text_content).strip() != "ASSISTANT":
                                    response_content += str(text_content) + "\n"
                
                # Clean up
                project_client.agents.threads.delete(thread.id)
                
                return response_content.strip() if response_content.strip() else "No response content received"
            else:
                project_client.agents.threads.delete(thread.id)
                return "No response received from orchestrator agent"
        else:
            project_client.agents.threads.delete(thread.id)
            return f"Orchestrator agent test failed: {run.last_error}"
            
    except Exception as e:
        return f"Error testing orchestrator agent: {str(e)}"


if __name__ == "__main__":
    result = test_orchestrator_agent()
    print("Orchestrator Agent Test Result:")
    print("=" * 50)
    print(result)
