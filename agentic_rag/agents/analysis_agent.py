"""
Healthcare Analysis Agent - Connected Agents Implementation
Analyzes healthcare data and creates visualizations using Code Interpreter
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import CodeInterpreterTool, MessageRole
from azure.identity import DefaultAzureCredential


def create_analysis_agent(project_client=None, model_name=None):
    """
    Create a healthcare analysis agent with Code Interpreter capabilities.
    
    Args:
        project_client: Optional AIProjectClient instance
        model_name: Optional model name override
        
    Returns:
        tuple: (analysis_agent, code_interpreter_tool)
    """
    if project_client is None:
        project_client = AIProjectClient(
            endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
    
    if model_name is None:
        model_name = os.environ.get("GPT4O_DEPLOYMENT") or "gpt-4o"
    
    # Create Code Interpreter tool
    code_interpreter_tool = CodeInterpreterTool()
    
    # Create the analysis agent
    analysis_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_analysis_agent",
        instructions="""You are a healthcare data analysis specialist. Your responsibilities include:

- Analyze healthcare data and research findings
- Create visualizations, charts, and graphs
- Perform statistical analysis on medical data
- Interpret medical data trends and patterns
- Generate insights from research data
- Create structured tables and comparisons

Use the code interpreter to analyze data and create visualizations. Focus on making complex medical data understandable through clear analysis and visual representations.""",
        tools=code_interpreter_tool.definitions,
        tool_resources=code_interpreter_tool.resources,
    )
    
    return analysis_agent, code_interpreter_tool


def test_analysis_agent():
    """Test the analysis agent with healthcare data analysis."""
    try:
        # Create the analysis agent
        analysis_agent, code_interpreter_tool = create_analysis_agent()
        
        # Initialize client for testing
        project_client = AIProjectClient(
            endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
        
        # Create a thread and test query
        thread = project_client.agents.threads.create()
        test_query = "Analyze the effectiveness of different diabetes treatments and create a comparison table with metrics."
        
        # Add test message
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=test_query,
        )
        
        # Run the agent
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id, 
            agent_id=analysis_agent.id
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
                return "No response received from analysis agent"
        else:
            project_client.agents.threads.delete(thread.id)
            return f"Analysis agent test failed: {run.last_error}"
            
    except Exception as e:
        return f"Error testing analysis agent: {str(e)}"


if __name__ == "__main__":
    result = test_analysis_agent()
    print("Analysis Agent Test Result:")
    print("=" * 50)
    print(result)
