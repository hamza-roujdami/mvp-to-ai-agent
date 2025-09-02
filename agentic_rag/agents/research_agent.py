"""
Healthcare Research Agent - Connected Agents Implementation
Searches for medical information using Azure AI Search
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import AzureAISearchTool, MessageRole
from azure.identity import DefaultAzureCredential


def create_research_agent(project_client=None, model_name=None):
    """
    Create a healthcare research agent with Azure AI Search capabilities.
    
    Args:
        project_client: Optional AIProjectClient instance
        model_name: Optional model name override
        
    Returns:
        tuple: (research_agent, search_tool)
    """
    if project_client is None:
        project_client = AIProjectClient(
            endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
    
    if model_name is None:
        model_name = os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"
    
    # Create Azure AI Search tool
    search_tool = AzureAISearchTool(
        index_connection_id=os.environ["AZURE_SEARCH_CONNECTION_ID"],
        index_name=os.environ["AZURE_SEARCH_INDEX_NAME"]
    )
    
    # Create the research agent
    research_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_research_agent",
        instructions="""You are a healthcare research specialist. Your responsibilities include:

- Search for relevant medical information using Azure AI Search
- Find evidence-based healthcare content and research papers
- Provide accurate, up-to-date medical information
- Focus on finding reliable sources and citations
- Always search thoroughly and provide comprehensive research results

When searching, use specific medical terms and be thorough in your research approach.""",
        tools=search_tool.definitions,
        tool_resources=search_tool.resources,
    )
    
    return research_agent, search_tool


def test_research_agent():
    """Test the research agent with a healthcare query."""
    try:
        # Create the research agent
        research_agent, search_tool = create_research_agent()
        
        # Initialize client for testing
        project_client = AIProjectClient(
            endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
        
        # Create a thread and test query
        thread = project_client.agents.threads.create()
        test_query = "What are the latest treatments for diabetes?"
        
        # Add test message
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=test_query,
        )
        
        # Run the agent
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id, 
            agent_id=research_agent.id
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
                return "No response received from research agent"
        else:
            project_client.agents.threads.delete(thread.id)
            return f"Research agent test failed: {run.last_error}"
            
    except Exception as e:
        return f"Error testing research agent: {str(e)}"


if __name__ == "__main__":
    result = test_research_agent()
    print("Research Agent Test Result:")
    print("=" * 50)
    print(result)
