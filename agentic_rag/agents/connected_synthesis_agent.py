#!/usr/bin/env python3
"""
📝 Connected Synthesis Agent - Healthcare Response Generation with Agent Communication

This agent specializes in synthesizing healthcare information into patient-friendly responses
and can communicate with other agents in the connected agent workflow.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import CodeInterpreterTool, MessageRole
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def create_connected_synthesis_agent():
    """
    Create the Connected Synthesis Agent for healthcare response generation.
    
    This agent:
    1. Synthesizes healthcare research and analysis into patient-friendly responses
    2. Creates comprehensive 7-section healthcare summaries
    3. Generates visualizations using Code Interpreter
    4. Can communicate with other connected agents
    
    Returns:
        The created connected synthesis agent with Code Interpreter tools
    """
    
    # Initialize the Azure AI Projects client
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    
    # Create Code Interpreter tool for visualizations
    code_interpreter_tool = CodeInterpreterTool()
    
    # Connected Synthesis Agent instructions with agent communication capabilities
    synthesis_instructions = """
    You are a Connected Healthcare Synthesis Agent specializing in creating comprehensive, 
    patient-friendly healthcare responses with visualizations.
    
    Your role is to:
    1. Synthesize healthcare research and analysis into patient-friendly responses
    2. Create comprehensive 7-section healthcare summaries
    3. Generate visualizations and charts using Code Interpreter
    4. Provide clear, actionable healthcare guidance
    5. Communicate effectively with other connected agents
    
    SYNTHESIS CAPABILITIES:
    - Transform complex medical information into patient-friendly language
    - Create comprehensive healthcare summaries
    - Generate visual aids and charts for better understanding
    - Provide actionable healthcare recommendations
    - Integrate research findings with analysis insights
    
    CODE INTERPRETER USAGE:
    - Create patient-friendly charts and graphs
    - Generate visual timelines for treatment plans
    - Build comparison charts for treatment options
    - Create symptom tracking visualizations
    - Generate health monitoring charts
    
    AGENT COMMUNICATION:
    You are part of a connected agent workflow where:
    - Research Agent provides you with healthcare research data
    - Analysis Agent provides you with data insights and analysis
    - You synthesize all information into comprehensive patient responses
    
    RESPONSE FORMAT:
    Always provide a comprehensive 7-section response:
    1. 🏥 Key Information - Essential facts about the condition
    2. ⚠️ Warning Signs - Symptoms to watch for
    3. 💊 Treatment Options - Available treatments and medications
    4. 📊 Understanding Your Condition - Visual charts and explanations
    5. 💡 What You Can Do - Actionable steps for patients
    6. 🚨 When to Seek Help - Clear guidance on when to see a doctor
    7. 📚 Additional Resources - Helpful links and information
    
    CRITICAL REQUIREMENTS:
    - Keep responses comprehensive (500+ words)
    - Use Code Interpreter for visualizations
    - Make information patient-friendly and accessible
    - Provide actionable healthcare guidance
    - Include visual aids for better understanding
    - Communicate effectively with other agents
    - Ensure all information is evidence-based
    """
    
    # Choose a tool-capable model
    model_name = os.environ.get("SYNTHESIS_AGENT_MODEL") or os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"
    
    # Create the Connected Synthesis Agent with Code Interpreter tools
    synthesis_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_synthesis_agent_connected",
        instructions=synthesis_instructions,
        tools=code_interpreter_tool.definitions,
        tool_resources=code_interpreter_tool.resources
    )
    
    print(f"✅ Created Connected Synthesis Agent - ID: {synthesis_agent.id}")
    print(f"   Name: {synthesis_agent.name}")
    print(f"   Model: {synthesis_agent.model}")
    print(f"   Tools: Code Interpreter for visualizations")
    print(f"   Capabilities: Agent communication + comprehensive synthesis")
    
    return synthesis_agent, code_interpreter_tool

def test_connected_synthesis_agent():
    """Test the connected synthesis agent with healthcare response generation."""
    
    print("📝 Testing Connected Synthesis Agent with Response Generation")
    print("=" * 65)
    
    # Check required environment variables
    required_vars = ["AZURE_AI_FOUNDRY_ENDPOINT"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return None
    
    print("✅ All required environment variables are set")
    
    try:
        # Create the connected synthesis agent
        print("\n📝 Creating Connected Synthesis Agent...")
        synthesis_agent, code_interpreter_tool = create_connected_synthesis_agent()
        
        # Test the agent with healthcare synthesis
        print("\n🧪 Testing Connected Synthesis Agent with Response Generation...")
        
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
        
        # Test query with healthcare research data
        test_query = """
        Synthesize this healthcare research into a comprehensive patient-friendly response:
        
        Diabetes Research Findings:
        - Type 1 Diabetes: 5-10% of all diabetes cases, usually diagnosed in children/young adults
        - Type 2 Diabetes: 90-95% of all diabetes cases, usually diagnosed in adults
        - Common symptoms: increased thirst, frequent urination, fatigue, blurred vision
        - Risk factors: family history, obesity, age over 45, physical inactivity, high blood pressure
        - Treatment options: insulin therapy, metformin, lifestyle changes, blood sugar monitoring
        
        Analysis Insights:
        - Early detection is crucial for preventing complications
        - Lifestyle modifications can significantly improve outcomes
        - Regular monitoring helps maintain optimal blood sugar levels
        - Patient education is essential for successful management
        
        Please create a comprehensive 7-section patient-friendly response with visualizations.
        """
        
        # Create test message
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=test_query,
        )
        print(f"✅ Created test message - ID: {message.id}")
        print(f"   Query: Healthcare synthesis with visualizations")
        
        # Run the connected synthesis agent
        print("\n🔄 Running Connected Synthesis Agent with Code Interpreter...")
        
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=synthesis_agent.id
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
                
                print(f"\n📝 Connected Synthesis Agent Response:")
                print("=" * 50)
                
                if hasattr(response_message, 'content') and response_message.content:
                    for content_item in response_message.content:
                        if hasattr(content_item, 'text'):
                            text_content = content_item.text
                            if text_content:
                                print(f"   {text_content}")
                        elif hasattr(content_item, 'image_url'):
                            print(f"   📊 Generated visualization: {content_item}")
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
        
        return synthesis_agent
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("📝 Healthcare Agentic RAG System - Connected Synthesis Agent Test")
    print("=" * 75)
    
    # Test the connected synthesis agent
    synthesis_agent = test_connected_synthesis_agent()
    
    if synthesis_agent:
        print(f"\n✅ Connected Synthesis Agent creation and testing completed!")
        print(f"   Agent ID: {synthesis_agent.id}")
        print(f"   Agent Name: {synthesis_agent.name}")
        print(f"   Capabilities: Response synthesis + agent communication")
        print(f"   Tools: Code Interpreter for visualizations")
    else:
        print(f"❌ Error during testing")
