#!/usr/bin/env python3
"""
📊 Analysis Agent - Healthcare Data Analysis and Pattern Recognition

This agent specializes in analyzing healthcare data, identifying patterns, and creating insights.
Uses Code Interpreter for data analysis, statistical computations, and visualizations.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import CodeInterpreterTool, MessageRole
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def create_analysis_agent():
    """
    Create the Analysis Agent for healthcare data analysis and pattern recognition.
    
    This agent uses Code Interpreter to analyze healthcare data, identify patterns,
    create visualizations, and generate statistical insights.
    
    Returns:
        The created analysis agent with Code Interpreter tools
    """
    
    # Initialize the Azure AI Projects client
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    
    # Initialize Code Interpreter tool for data analysis
    code_interpreter_tool = CodeInterpreterTool()
    
    # Analysis Agent instructions for healthcare data analysis
    analysis_instructions = """
    You are a Healthcare Analysis Agent specializing in concise, actionable medical insights.
    
    Your role is to analyze research findings and provide CLEAR, BRIEF insights.
    
    CRITICAL REQUIREMENTS:
    - Keep responses under 200 words
    - Focus on PRACTICAL insights only
    - Use bullet points and clear formatting
    - Avoid academic language - be patient-friendly
    - Prioritize actionable recommendations
    
    FORMAT YOUR RESPONSE AS:
    • Key Insight 1
    • Key Insight 2
    • Key Insight 3
    
    Remember: Patients need simple, actionable insights, not complex analysis.
    """

    # Choose a tool-capable model
    model_name = os.environ.get("ANALYSIS_AGENT_MODEL") or os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"

    # Create the Analysis Agent with Code Interpreter tools properly bound
    analysis_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_analysis_agent",
        instructions=analysis_instructions,
        tools=code_interpreter_tool.definitions,
        tool_resources=code_interpreter_tool.resources
    )
    
    print(f"✅ Created Analysis Agent - ID: {analysis_agent.id}")
    print(f"   Name: {analysis_agent.name}")
    print(f"   Model: {analysis_agent.model}")
    print(f"   Tools: Code Interpreter for data analysis")
    
    return analysis_agent, code_interpreter_tool


def test_analysis_agent(agent_id, toolset):
    """
    Test the Analysis Agent with healthcare data analysis tasks.
    
    Args:
        agent_id: The ID of the analysis agent to test
        toolset: The toolset with Code Interpreter tools
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
    
    # Test healthcare data analysis query
    test_query = """Please analyze the following diabetes symptoms data and create visualizations:

Type 1 Diabetes Symptoms:
- Weight loss: 90% of patients
- Extreme hunger: 75% of patients  
- Fatigue: 70% of patients
- Blurred vision: 60% of patients

Type 2 Diabetes Symptoms:
- Weight loss: 25% of patients
- Extreme hunger: 45% of patients
- Fatigue: 80% of patients
- Blurred vision: 55% of patients

Please create:
1. A comparison chart showing symptom prevalence
2. Statistical analysis of the differences
3. Key insights about symptom patterns
4. Visualizations to illustrate the findings"""

    # Create message to thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=test_query,
    )
    print(f"✅ Created test message - ID: {message.id}")
    print(f"   Query: Healthcare data analysis task")
    
    # Create and process Agent run
    print("🔄 Running Analysis Agent with Code Interpreter...")
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id, 
        agent_id=agent_id
    )
    print(f"✅ Run completed with status: {run.status}")
    
    if run.status == "failed":
        print(f"❌ Run failed: {run.last_error}")
        return
    
    # Get the agent's response
    try:
        messages = project_client.agents.messages.list(thread_id=thread.id)
        messages_list = list(messages)
        print(f"📝 Found {len(messages_list)} messages in thread")
        
        # Find the assistant's response (last message from assistant)
        assistant_messages = [msg for msg in messages_list if msg.role.value == "assistant"]
        print(f"🤖 Found {len(assistant_messages)} assistant messages")
        
        if assistant_messages:
            response_message = assistant_messages[-1]  # Get the last assistant message
            print(f"\n📊 Analysis Agent Response:")
            
            # Extract the text content from the response
            if isinstance(response_message.content, list) and len(response_message.content) > 0:
                for content_item in response_message.content:
                    if isinstance(content_item, dict):
                        if content_item.get('type') == 'text':
                            text_content = content_item.get('text', {}).get('value', '')
                            print(f"   {text_content}")
                        elif content_item.get('type') == 'image_file':
                            print(f"   📊 Generated visualization: {content_item}")
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
    """Main function to create and test the Analysis Agent."""
    
    print("📊 Healthcare Agentic RAG System - Analysis Agent Test")
    print("=" * 60)
    
    # Check environment variables
    required_vars = [
        "AZURE_AI_FOUNDRY_ENDPOINT",
        "AZURE_AI_FOUNDRY_API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return
    
    print("✅ All required environment variables are set")
    
    try:
        # Create Analysis Agent
        print("\n📊 Creating Analysis Agent...")
        analysis_agent, toolset = create_analysis_agent()
        
        # Test Analysis Agent
        print("\n🧪 Testing Analysis Agent...")
        test_analysis_agent(analysis_agent.id, toolset)
        
        print(f"\n✅ Analysis Agent creation and testing completed!")
        print(f"   Agent ID: {analysis_agent.id}")
        print(f"   Agent Name: {analysis_agent.name}")
        print(f"   Tools: Code Interpreter for data analysis")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
