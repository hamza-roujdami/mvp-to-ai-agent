#!/usr/bin/env python3
"""
📝 Research Agent - Healthcare Document Retrieval with Azure AI Search

This agent specializes in searching healthcare documents using Azure AI Search
and providing evidence-based medical information with proper citations.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import (
    AzureAISearchTool, 
    AzureAISearchQueryType,
    AgentsNamedToolChoice,
    MessageRole
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def create_research_agent():
    """
    Create the Research Agent for healthcare document retrieval.
    
    This agent uses Azure AI Search to find relevant healthcare documents
    and provides evidence-based medical information.
    
    Returns:
        The created research agent
    """
    
    # Initialize the Azure AI Projects client
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    
    # Create Azure AI Search tool with proper configuration
    search_tool = AzureAISearchTool(
        index_connection_id=os.environ["AZURE_SEARCH_CONNECTION_ID"],
        index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
        query_type=AzureAISearchQueryType.SIMPLE,  # Use SIMPLE for compatibility
        top_k=10
    )
    
    # Research Agent instructions for healthcare document retrieval
    research_instructions = """You are a healthcare research specialist with access to Azure AI Search tools. Your PRIMARY responsibility is to SEARCH THROUGH HEALTHCARE DOCUMENTS using the provided search tools before answering any questions.

CRITICAL: You MUST use the Azure AI Search tool to find relevant healthcare documents before providing any information. DO NOT rely on general knowledge.

**AVAILABLE TOOLS:**
- Azure AI Search Tool: Use this to search through healthcare documents in the database

**MANDATORY WORKFLOW:**
1. ALWAYS start by using the Azure AI Search tool to search for relevant healthcare documents
2. Search using specific keywords related to the user's query
3. Extract information ONLY from the search results
4. Provide detailed citations from the found documents
5. If no relevant documents are found, say so clearly

**Search Instructions:**
- Use the Azure AI Search tool for EVERY query
- Search with relevant medical terms and keywords
- Extract specific facts, symptoms, treatments from the documents
- Include document sources and citations
- Focus on the most recent and authoritative information found

**Response Requirements:**
- Start with "Based on my search of healthcare documents..."
- Include specific information found in the documents
- Cite the document sources
- If documents don't contain the requested information, state this clearly
- DO NOT provide general medical knowledge without document support

**Example Response Structure:**
"Based on my search of healthcare documents, I found the following information about [topic]:

[Specific information from documents with citations]

Sources: [Document names/sources from search results]

Note: This information is based on the documents available in our healthcare database."

Remember: You MUST use the search tool first. Never provide information without searching the documents. The search tool is your primary source of information."""

    # Choose a tool-capable model
    model_name = os.environ.get("RESEARCH_AGENT_MODEL") or os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"

    # Create the Research Agent with proper tool binding
    research_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_research_agent",
        instructions=research_instructions,
        tools=search_tool.definitions,  # Pass tool definitions
        tool_resources=search_tool.resources,  # Pass tool resources
    )
    
    print(f"✅ Created Research Agent - ID: {research_agent.id}")
    print(f"   Name: {research_agent.name}")
    print(f"   Model: {research_agent.model}")
    print(f"   Tools: Azure AI Search integration")
    
    return research_agent, search_tool


def test_research_agent(agent_id, search_tool):
    """
    Test the Research Agent with a healthcare query.
    
    Args:
        agent_id: The ID of the research agent to test
        search_tool: The Azure AI Search tool
    """
    
    # Initialize the Azure AI Projects client
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    
    # Create a test thread
    thread = project_client.agents.threads.create()
    print(f"✅ Created test thread - ID: {thread.id}")
    
    # Test healthcare query
    test_query = "What are the common symptoms of diabetes?"
    
    # Create message to thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=test_query,
    )
    print(f"✅ Created test message - ID: {message.id}")
    print(f"   Query: {test_query}")
    
    # Create and process Agent run with FORCED tool usage
    print("🔄 Running Research Agent with forced Azure AI Search usage...")
    
    # Force the agent to use Azure AI Search tool
    tool_choice = AgentsNamedToolChoice(type="azure_ai_search")
    
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id, 
        agent_id=agent_id,
        tool_choice=tool_choice,  # Force tool usage
    )
    print(f"✅ Run created - ID: {run.id}")
    print(f"   Initial status: {run.status}")
    
    # Monitor the run
    while run.status in ["queued", "in_progress", "requires_action"]:
        run = project_client.agents.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"   Status: {run.status}")
        
        if run.status == "requires_action":
            print(f"   🔧 Tool action required!")
            if hasattr(run, 'required_action') and run.required_action:
                print(f"   Required action: {run.required_action}")
        
        if run.status == "failed":
            print(f"   ❌ Run failed: {run.last_error}")
            return
    
    print(f"✅ Final run status: {run.status}")
    
    # Get the agent's response
    try:
        messages = list(project_client.agents.messages.list(thread_id=thread.id))
        print(f"📝 Found {len(messages)} messages in thread")
        
        # Find the assistant's response (last message from assistant)
        assistant_messages = [msg for msg in messages if msg.role.value == "assistant"]
        print(f"🤖 Found {len(assistant_messages)} assistant messages")
        
        if assistant_messages:
            response_message = assistant_messages[-1]  # Get the last assistant message
            print(f"\n🔍 Research Agent Response:")
            
            # Extract the text content from the response
            if isinstance(response_message.content, list) and len(response_message.content) > 0:
                for content_item in response_message.content:
                    if isinstance(content_item, dict):
                        if content_item.get('type') == 'text':
                            text_content = content_item.get('text', {}).get('value', '')
                            print(f"   {text_content}")
                        else:
                            print(f"   {content_item}")
                    else:
                        print(f"   {content_item}")
            else:
                print(f"   {response_message.content}")
        else:
            print("❌ No assistant messages found")
            
    except Exception as e:
        print(f"❌ Error retrieving response: {e}")
        import traceback
        traceback.print_exc()
    
    # Clean up - delete the test thread
    project_client.agents.threads.delete(thread.id)
    print(f"✅ Cleaned up test thread")


def main():
    """Main function to create and test the Research Agent."""
    
    print("🔍 Healthcare Agentic RAG System - Research Agent Test")
    print("=" * 60)
    
    # Check required environment variables
    required_vars = [
        "AZURE_AI_FOUNDRY_ENDPOINT",
        "AZURE_AI_FOUNDRY_API_KEY",
        "AZURE_SEARCH_CONNECTION_ID"
    ]
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return
    
    print("✅ All required environment variables are set")
    
    try:
        # Create Research Agent
        print("\n🔍 Creating Research Agent...")
        research_agent, search_tool = create_research_agent()
        
        # Test the Research Agent
        print("\n🧪 Testing Research Agent...")
        test_research_agent(research_agent.id, search_tool)
        
        print(f"\n✅ Research Agent creation and testing completed!")
        print(f"   Agent ID: {research_agent.id}")
        print(f"   Agent Name: {research_agent.name}")
        print(f"   Tools: Azure AI Search integration")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
