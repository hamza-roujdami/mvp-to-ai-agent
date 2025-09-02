#!/usr/bin/env python3
"""
📊 Connected Analysis Agent - Healthcare Data Analysis with Agent Communication

This agent specializes in analyzing healthcare data and can communicate with other agents
in the connected agent workflow.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import CodeInterpreterTool, MessageRole
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def create_connected_analysis_agent():
    """
    Create the Connected Analysis Agent for healthcare data analysis.
    
    This agent:
    1. Analyzes healthcare research data
    2. Creates insights and patterns
    3. Generates visualizations using Code Interpreter
    4. Can communicate with other connected agents
    
    Returns:
        The created connected analysis agent with Code Interpreter tools
    """
    
    # Initialize the Azure AI Projects client
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    
    # Create Code Interpreter tool for data analysis
    code_interpreter_tool = CodeInterpreterTool()
    
    # Connected Analysis Agent instructions with agent communication capabilities
    analysis_instructions = """
    You are a Connected Healthcare Analysis Agent specializing in data analysis and insights.
    
    Your role is to:
    1. Analyze healthcare research data and findings
    2. Identify patterns, trends, and insights
    3. Create visualizations and charts using Code Interpreter
    4. Provide actionable data-driven recommendations
    5. Communicate effectively with other connected agents
    
    ANALYSIS CAPABILITIES:
    - Statistical analysis of healthcare data
    - Pattern recognition in symptoms and treatments
    - Risk factor analysis and correlations
    - Treatment effectiveness comparisons
    - Data visualization and chart creation
    
    CODE INTERPRETER USAGE:
    - Create charts and graphs to illustrate health trends
    - Generate statistical analyses of healthcare data
    - Build visual comparisons of treatment options
    - Create timeline visualizations for disease progression
    - Generate risk assessment charts
    
    AGENT COMMUNICATION:
    You are part of a connected agent workflow where:
    - Research Agent provides you with healthcare research data
    - You analyze the data and provide insights
    - Your analysis helps inform patient care decisions
    
    RESPONSE FORMAT:
    When analyzing healthcare data, provide:
    1. 📊 Key Data Insights
    2. 📈 Statistical Analysis
    3. 🔍 Pattern Recognition
    4. 📋 Risk Assessment
    5. 💡 Actionable Recommendations
    6. 📊 Visualizations (using Code Interpreter)
    
    CRITICAL REQUIREMENTS:
    - Keep analysis concise but comprehensive
    - Use Code Interpreter for visualizations
    - Focus on actionable insights
    - Provide evidence-based recommendations
    - Create clear, patient-friendly visualizations
    - Communicate effectively with other agents
    """
    
    # Choose a tool-capable model
    model_name = os.environ.get("ANALYSIS_AGENT_MODEL") or os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"
    
    # Create the Connected Analysis Agent with Code Interpreter tools
    analysis_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_analysis_agent_connected",
        instructions=analysis_instructions,
        tools=code_interpreter_tool.definitions,
        tool_resources=code_interpreter_tool.resources
    )
    
    print(f"✅ Created Connected Analysis Agent - ID: {analysis_agent.id}")
    print(f"   Name: {analysis_agent.name}")
    print(f"   Model: {analysis_agent.model}")
    print(f"   Tools: Code Interpreter for data analysis")
    print(f"   Capabilities: Agent communication + data visualization")
    
    return analysis_agent, code_interpreter_tool

def test_connected_analysis_agent():
    """Test the connected analysis agent with healthcare data analysis."""
    
    print("📊 Testing Connected Analysis Agent with Data Analysis")
    print("=" * 60)
    
    # Check required environment variables
    required_vars = ["AZURE_AI_FOUNDRY_ENDPOINT"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return None
    
    print("✅ All required environment variables are set")
    
    try:
        # Create the connected analysis agent
        print("\n📊 Creating Connected Analysis Agent...")
        analysis_agent, code_interpreter_tool = create_connected_analysis_agent()
        
        # Test the agent with healthcare data analysis
        print("\n🧪 Testing Connected Analysis Agent with Data Analysis...")
        
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
        
        # Test query with healthcare data
        test_query = """
        Analyze this healthcare research data:
        
        Diabetes Research Findings:
        - Type 1 Diabetes: 5-10% of all diabetes cases
        - Type 2 Diabetes: 90-95% of all diabetes cases
        - Common symptoms: increased thirst, frequent urination, fatigue
        - Risk factors: family history, obesity, age, physical inactivity
        - Treatment options: insulin therapy, metformin, lifestyle changes
        
        Please analyze this data and create visualizations showing:
        1. Distribution of diabetes types
        2. Risk factor correlations
        3. Treatment effectiveness comparison
        """
        
        # Create test message
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=test_query,
        )
        print(f"✅ Created test message - ID: {message.id}")
        print(f"   Query: Healthcare data analysis with visualizations")
        
        # Run the connected analysis agent
        print("\n🔄 Running Connected Analysis Agent with Code Interpreter...")
        
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=analysis_agent.id
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
                
                print(f"\n📊 Connected Analysis Agent Response:")
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
        
        return analysis_agent
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("📊 Healthcare Agentic RAG System - Connected Analysis Agent Test")
    print("=" * 70)
    
    # Test the connected analysis agent
    analysis_agent = test_connected_analysis_agent()
    
    if analysis_agent:
        print(f"\n✅ Connected Analysis Agent creation and testing completed!")
        print(f"   Agent ID: {analysis_agent.id}")
        print(f"   Agent Name: {analysis_agent.name}")
        print(f"   Capabilities: Data analysis + agent communication")
        print(f"   Tools: Code Interpreter for visualizations")
    else:
        print(f"❌ Error during testing")
