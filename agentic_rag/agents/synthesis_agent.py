#!/usr/bin/env python3
"""
📝 Enhanced Synthesis Agent with Code Interpreter

This agent specializes in synthesizing research findings and analysis insights into 
comprehensive, patient-friendly healthcare responses with visualizations and data analysis.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ToolSet, MessageRole, CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def create_synthesis_agent():
    """
    Create the Enhanced Synthesis Agent with Code Interpreter for healthcare response generation.
    
    This agent takes research findings and analysis insights to generate comprehensive,
    patient-friendly healthcare responses with visualizations and data analysis.
    
    Returns:
        The created synthesis agent with Code Interpreter tool
    """
    
    # Initialize the Azure AI Projects client
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    
    # Initialize Code Interpreter tool for creating visualizations and data analysis
    code_interpreter_tool = CodeInterpreterTool()
    
    # Create toolset for agent execution
    toolset = ToolSet()
    
    # Enhanced Synthesis Agent instructions with Code Interpreter capabilities
    synthesis_instructions = """
    You are an Enhanced Healthcare Synthesis Agent with Code Interpreter capabilities for creating visualizations.
    
    Your role is to create COMPREHENSIVE, ACCURATE, and PATIENT-FRIENDLY healthcare responses with visual aids.
    
    AVAILABLE TOOLS:
    - Code Interpreter: Create charts, graphs, and visualizations to help patients understand health information
    - Data Analysis: Analyze health data and create meaningful insights
    - Visualization Creation: Generate visual aids like symptom timelines, risk factor charts, treatment comparisons
    
    CRITICAL REQUIREMENTS:
    - Use Code Interpreter to create helpful visualizations when data is provided
    - Keep responses under 500 words but comprehensive
    - Use clear, simple language (avoid medical jargon)
    - Structure information logically with headers
    - Include visual aids when helpful for patient understanding
    - Focus on actionable, evidence-based information
    
    ENHANCED FORMAT:
    
    ## 🏥 Key Information
    [Clear, evidence-based medical facts]
    
    ## ⚠️ Warning Signs
    [Key symptoms to watch for]
    
    ## 💊 Treatment Options
    [Evidence-based treatments and medications]
    
    ## 📊 Understanding Your Condition
    [Visual charts or graphs created with Code Interpreter when helpful]
    
    ## 💡 What You Can Do
    [Actionable steps and lifestyle recommendations]
    
    ## 🚨 When to Seek Help
    [Clear guidance on when to see a doctor]
    
    ## 📚 Additional Resources
    [Helpful resources and next steps]
    
    VISUALIZATION GUIDELINES:
    - Create charts when comparing symptoms, treatments, or risk factors
    - Use simple, clear visualizations that patients can easily understand
    - Include titles, labels, and legends for all charts
    - Focus on the most important information in visualizations
    
    Remember: Use Code Interpreter to create visual aids that help patients better understand their health information.
    """

    # Choose a tool-capable model
    model_name = os.environ.get("SYNTHESIS_AGENT_MODEL") or os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"

    # Create the Synthesis Agent with Code Interpreter
    synthesis_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_synthesis_agent",
        instructions=synthesis_instructions,
        tools=code_interpreter_tool.definitions,
        tool_resources=code_interpreter_tool.resources
    )
    
    print(f"✅ Created Synthesis Agent - ID: {synthesis_agent.id}")
    print(f"   Name: {synthesis_agent.name}")
    print(f"   Model: {synthesis_agent.model}")
    print(f"   Tools: Code Interpreter for visualizations and data analysis")
    
    return synthesis_agent, toolset


def test_synthesis_agent(agent_id, toolset):
    """
    Test the Synthesis Agent with Code Interpreter.
    
    Args:
        agent_id: The ID of the synthesis agent to test
        toolset: The toolset for agent execution
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
    
    # Test healthcare synthesis query with visualization
    test_query = """Please synthesize the following healthcare information into a comprehensive, patient-friendly response using your Code Interpreter tool:

RESEARCH FINDINGS:
- Diabetes affects how the body processes glucose
- Common symptoms include frequent urination, increased thirst, extreme hunger, weight loss, fatigue, blurred vision
- Type 1 diabetes typically has more severe symptoms and rapid onset
- Type 2 diabetes often has milder symptoms and gradual onset

ANALYSIS INSIGHTS:
- Weight loss is present in 90% of Type 1 vs 25% of Type 2 patients
- Extreme hunger affects 75% of Type 1 vs 45% of Type 2 patients
- Fatigue is more common in Type 2 (80%) than Type 1 (70%)
- Blurred vision affects similar proportions (60% vs 55%)

Please:
1. Create a visual chart showing the symptom differences between Type 1 and Type 2 diabetes using your Code Interpreter
2. Provide comprehensive, patient-friendly information about diabetes management
3. Include actionable steps and when to seek medical help
4. Make the information clear and accessible for patients

Use your Code Interpreter to create helpful visualizations that make the information easier to understand."""

    # Create message to thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=test_query,
    )
    print(f"✅ Created test message - ID: {message.id}")
    print(f"   Query: Healthcare synthesis with Code Interpreter")
    
    # Create and process Agent run
    print("🔄 Running Synthesis Agent with Code Interpreter...")
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id, 
        agent_id=agent_id,
        toolset=toolset
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
        assistant_messages = [msg for msg in messages_list if msg.role == "assistant"]
        print(f"🤖 Found {len(assistant_messages)} assistant messages")
        
        if assistant_messages:
            response_message = assistant_messages[-1]  # Get the last assistant message
            print(f"\n📝 Synthesis Agent Response:")
            
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
    """Main function to create and test the Synthesis Agent with Code Interpreter."""
    
    print("📝 Healthcare Agentic RAG System - Synthesis Agent with Code Interpreter")
    print("=" * 80)
    
    # Check required environment variables
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
        # Create Synthesis Agent with Code Interpreter
        print("\n📝 Creating Synthesis Agent with Code Interpreter...")
        synthesis_agent, toolset = create_synthesis_agent()
        
        # Test the Synthesis Agent
        print("\n🧪 Testing Synthesis Agent with Code Interpreter...")
        test_synthesis_agent(synthesis_agent.id, toolset)
        
        print(f"\n✅ Synthesis Agent creation and testing completed!")
        print(f"   Agent ID: {synthesis_agent.id}")
        print(f"   Agent Name: {synthesis_agent.name}")
        print(f"   Tools: Code Interpreter for visualizations and data analysis")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
