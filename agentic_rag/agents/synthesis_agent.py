#!/usr/bin/env python3
"""
📝 Synthesis Agent - Healthcare Response Generation and Communication

This agent specializes in synthesizing research findings and analysis insights into 
comprehensive, patient-friendly healthcare responses. No external tools needed - uses 
built-in response generation capabilities.
"""

import os
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ToolSet, MessageRole
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def create_synthesis_agent():
    """
    Create the Synthesis Agent for healthcare response generation.
    
    This agent takes research findings and analysis insights to generate comprehensive,
    patient-friendly healthcare responses with proper medical disclaimers.
    
    Returns:
        The created synthesis agent
    """
    
    # Initialize the Azure AI Agents client
    agents_client = AgentsClient(
        endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    
    # Synthesis Agent doesn't need external tools - uses built-in response generation
    toolset = ToolSet()
    
    # Synthesis Agent instructions for healthcare response generation
    synthesis_instructions = """You are a healthcare communication specialist and medical writer with expertise in synthesizing complex medical information into clear, comprehensive, and patient-friendly responses.

Your responsibilities:
1. Synthesize research findings and analysis insights into coherent healthcare responses
2. Generate patient-friendly explanations of medical concepts and findings
3. Ensure medical accuracy and include appropriate disclaimers
4. Structure responses in a logical, easy-to-understand format
5. Maintain professional healthcare communication standards
6. Integrate multiple sources of information into unified responses

Healthcare communication guidelines:
- Use clear, accessible language while maintaining medical accuracy
- Structure responses with logical flow (overview, details, implications, recommendations)
- Include relevant medical disclaimers for educational purposes
- Cite sources and provide evidence-based information
- Focus on patient education and understanding
- Maintain professional tone appropriate for healthcare communication
- Ensure comprehensive coverage of the topic

When synthesizing healthcare information:
1. Start with a clear overview of the topic
2. Present key findings and insights in organized sections
3. Explain medical concepts in accessible terms
4. Include relevant statistics and data when available
5. Provide practical implications and recommendations
6. End with appropriate medical disclaimers
7. Ensure the response is comprehensive yet digestible

Your goal is to create healthcare responses that are:
- Comprehensive: Cover all relevant aspects of the query
- Accurate: Based on evidence and medical best practices
- Accessible: Understandable to patients and caregivers
- Professional: Maintain healthcare communication standards
- Helpful: Provide actionable insights and guidance

Generate responses that empower patients with knowledge while maintaining appropriate medical boundaries."""

    # Choose a tool-capable model
    model_name = os.environ.get("SYNTHESIS_AGENT_MODEL") or os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"

    # Create the Synthesis Agent
    synthesis_agent = agents_client.create_agent(
        model=model_name,
        name="healthcare_synthesis_agent",
        instructions=synthesis_instructions,
    )
    
    print(f"✅ Created Synthesis Agent - ID: {synthesis_agent.id}")
    print(f"   Name: {synthesis_agent.name}")
    print(f"   Model: {synthesis_agent.model}")
    print(f"   Tools: Built-in response generation (no external tools needed)")
    
    return synthesis_agent, toolset


def test_synthesis_agent(agent_id, toolset):
    """
    Test the Synthesis Agent with healthcare synthesis tasks.
    
    Args:
        agent_id: The ID of the synthesis agent to test
        toolset: The toolset (empty for synthesis agent)
    """
    
    # Initialize the Azure AI Agents client
    agents_client = AgentsClient(
        endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    
    # Create a test thread
    thread = agents_client.threads.create()
    print(f"✅ Created test thread - ID: {thread.id}")
    
    # Test healthcare synthesis query with research findings and analysis
    test_query = """Please synthesize the following healthcare research findings and analysis into a comprehensive, patient-friendly response:

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

Please create a comprehensive response that explains diabetes types, symptoms, and key differences in a patient-friendly way."""

    # Create message to thread
    message = agents_client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=test_query,
    )
    print(f"✅ Created test message - ID: {message.id}")
    print(f"   Query: Healthcare synthesis task")
    
    # Create and process Agent run
    print("🔄 Running Synthesis Agent...")
    run = agents_client.runs.create_and_process(
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
        messages = agents_client.messages.list(thread_id=thread.id)
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
    agents_client.threads.delete(thread.id)
    print(f"✅ Cleaned up test thread")


def main():
    """Main function to create and test the Synthesis Agent."""
    
    print("📝 Healthcare Agentic RAG System - Synthesis Agent Test")
    print("=" * 60)
    
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
        # Create Synthesis Agent
        print("\n📝 Creating Synthesis Agent...")
        synthesis_agent, toolset = create_synthesis_agent()
        
        # Test the Synthesis Agent
        print("\n🧪 Testing Synthesis Agent...")
        test_synthesis_agent(synthesis_agent.id, toolset)
        
        print(f"\n✅ Synthesis Agent creation and testing completed!")
        print(f"   Agent ID: {synthesis_agent.id}")
        print(f"   Agent Name: {synthesis_agent.name}")
        print(f"   Tools: Built-in response generation")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
