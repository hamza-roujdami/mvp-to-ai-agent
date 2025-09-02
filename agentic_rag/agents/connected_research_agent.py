#!/usr/bin/env python3
"""
🔍 Connected Research Agent - Healthcare Document Retrieval with Agent Orchestration

This agent serves as the main entry point and orchestrates the connected agent workflow.
It retrieves healthcare documents and coordinates with Analysis and Synthesis agents.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import (
    AzureAISearchTool, 
    AzureAISearchQueryType,
    MessageRole
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def create_connected_research_agent():
    """
    Create the Connected Research Agent that orchestrates the entire workflow.
    
    This agent:
    1. Searches healthcare documents using Azure AI Search
    2. Calls the Analysis Agent with research results
    3. Calls the Synthesis Agent with research results
    4. Combines all results into a comprehensive response
    
    Returns:
        The created connected research agent with orchestration capabilities
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
        query_type=AzureAISearchQueryType.SIMPLE,
        top_k=10
    )
    
    # Connected Research Agent instructions with orchestration capabilities
    research_instructions = """
    You are a Connected Healthcare Research Agent that orchestrates a multi-agent healthcare workflow.
    
    Your role is to:
    1. Search healthcare documents using Azure AI Search
    2. Coordinate with Analysis and Synthesis agents
    3. Combine all results into a comprehensive healthcare response
    
    WORKFLOW PROCESS:
    1. When you receive a healthcare query, first search for relevant documents
    2. Extract key research findings from the search results
    3. Call the Analysis Agent with the research findings for data analysis
    4. Call the Synthesis Agent with the research findings for patient-friendly synthesis
    5. Combine the analysis and synthesis results into a comprehensive response
    
    AGENT COORDINATION:
    - Analysis Agent ID: healthcare_analysis_agent_connected
    - Synthesis Agent ID: healthcare_synthesis_agent_connected
    
    CALLING OTHER AGENTS:
    To call the Analysis Agent, use this format:
    "Please analyze this healthcare research: [research findings]"
    
    To call the Synthesis Agent, use this format:
    "Please synthesize this healthcare research into a patient-friendly response: [research findings]"
    
    RESPONSE FORMAT:
    Combine all results into a comprehensive 7-section response:
    1. 🏥 Key Information
    2. ⚠️ Warning Signs  
    3. 💊 Treatment Options
    4. 📊 Understanding Your Condition
    5. 💡 What You Can Do
    6. 🚨 When to Seek Help
    7. 📚 Additional Resources
    
    CRITICAL REQUIREMENTS:
    - Keep responses comprehensive but patient-friendly
    - Include visualizations and data analysis from the Analysis Agent
    - Ensure all information is evidence-based from your research
    - Coordinate effectively with other agents
    - Provide actionable healthcare guidance
    """
    
    # Choose a tool-capable model
    model_name = os.environ.get("RESEARCH_AGENT_MODEL") or os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"
    
    # Create the Connected Research Agent with orchestration capabilities
    research_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_research_agent_connected",
        instructions=research_instructions,
        tools=search_tool.definitions,
        tool_resources=search_tool.resources,
    )
    
    print(f"✅ Created Connected Research Agent - ID: {research_agent.id}")
    print(f"   Name: {research_agent.name}")
    print(f"   Model: {research_agent.model}")
    print(f"   Tools: Azure AI Search + Agent Orchestration")
    print(f"   Capabilities: Multi-agent workflow coordination")
    
    return research_agent, search_tool

def test_connected_research_agent():
    """Test the connected research agent with a healthcare query."""
    
    print("🔍 Testing Connected Research Agent with Multi-Agent Workflow")
    print("=" * 70)
    
    # Check required environment variables
    required_vars = [
        "AZURE_AI_FOUNDRY_ENDPOINT",
        "AZURE_SEARCH_CONNECTION_ID", 
        "AZURE_SEARCH_INDEX_NAME"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return None
    
    print("✅ All required environment variables are set")
    
    try:
        # Create the connected research agent
        print("\n🔍 Creating Connected Research Agent...")
        research_agent, search_tool = create_connected_research_agent()
        
        # Test the agent with a healthcare query
        print("\n🧪 Testing Connected Research Agent with Multi-Agent Workflow...")
        
        # Initialize client for testing
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
        
        # Test query
        test_query = "What are the symptoms of diabetes and how is it treated?"
        
        # Create test message
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=test_query,
        )
        print(f"✅ Created test message - ID: {message.id}")
        print(f"   Query: {test_query}")
        
        # Run the connected research agent (this will orchestrate the entire workflow)
        print("\n🔄 Running Connected Research Agent with Multi-Agent Workflow...")
        print("   This will coordinate with Analysis and Synthesis agents...")
        
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=research_agent.id
        )
        
        print(f"✅ Run completed with status: {run.status}")
        
        if run.status == "completed":
            # Retrieve the response
            messages = project_client.agents.messages.list(thread_id=thread.id)
            messages_list = list(messages)
            
            print(f"📝 Found {len(messages_list)} messages in thread")
            
            # Find assistant messages
            assistant_messages = [msg for msg in messages_list if msg.role == MessageRole.ASSISTANT]
            
            if assistant_messages:
                print(f"🤖 Found {len(assistant_messages)} assistant messages")
                
                # Get the latest assistant message
                response_message = assistant_messages[-1]
                
                print(f"\n🔍 Connected Research Agent Response (Multi-Agent Workflow):")
                print("=" * 60)
                
                if hasattr(response_message, 'content') and response_message.content:
                    for content_item in response_message.content:
                        if hasattr(content_item, 'text'):
                            text_content = content_item.text
                            if text_content:
                                print(f"   {text_content}")
                        else:
                            print(f"   {content_item}")
                else:
                    print(f"   {response_message.content}")
            else:
                print("❌ No assistant messages found")
        else:
            print(f"❌ Run failed: {run.last_error}")
        
        # Clean up test thread
        project_client.agents.threads.delete(thread.id)
        print(f"✅ Cleaned up test thread")
        
        return research_agent
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🔍 Healthcare Agentic RAG System - Connected Research Agent Test")
    print("=" * 80)
    
    # Test the connected research agent
    research_agent = test_connected_research_agent()
    
    if research_agent:
        print(f"\n✅ Connected Research Agent creation and testing completed!")
        print(f"   Agent ID: {research_agent.id}")
        print(f"   Agent Name: {research_agent.name}")
        print(f"   Capabilities: Multi-agent workflow orchestration")
        print(f"   Tools: Azure AI Search + Agent Coordination")
    else:
        print(f"❌ Error during testing")
