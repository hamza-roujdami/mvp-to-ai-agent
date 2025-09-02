"""
Healthcare Synthesis Agent - Connected Agents Implementation
Synthesizes research findings and creates comprehensive reports using Code Interpreter
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import CodeInterpreterTool, MessageRole
from azure.identity import DefaultAzureCredential


def create_synthesis_agent(project_client=None, model_name=None):
    """
    Create a healthcare synthesis agent with Code Interpreter capabilities.
    
    Args:
        project_client: Optional AIProjectClient instance
        model_name: Optional model name override
        
    Returns:
        tuple: (synthesis_agent, code_interpreter_tool)
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
    
    # Create the synthesis agent
    synthesis_agent = project_client.agents.create_agent(
        model=model_name,
        name="healthcare_synthesis_agent",
        instructions="""You are a healthcare synthesis specialist. Your responsibilities include:

- Synthesize research findings and analysis results
- Create comprehensive healthcare reports and summaries
- Generate patient-friendly explanations of complex medical information
- Create visual summaries and infographics
- Provide actionable healthcare recommendations
- Format information in clear, structured ways

Use the code interpreter to create visual summaries and reports. Focus on making complex medical information accessible and actionable for patients and healthcare providers.""",
        tools=code_interpreter_tool.definitions,
        tool_resources=code_interpreter_tool.resources,
    )
    
    return synthesis_agent, code_interpreter_tool


def test_synthesis_agent():
    """Test the synthesis agent with healthcare report generation."""
    try:
        # Create the synthesis agent
        synthesis_agent, code_interpreter_tool = create_synthesis_agent()
        
        # Initialize client for testing
        project_client = AIProjectClient(
            endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
        
        # Create a thread and test query
        thread = project_client.agents.threads.create()
        test_query = "Create a comprehensive patient-friendly summary of diabetes treatment options with visual elements."
        
        # Add test message
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=test_query,
        )
        
        # Run the agent
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id, 
            agent_id=synthesis_agent.id
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
                return "No response received from synthesis agent"
        else:
            project_client.agents.threads.delete(thread.id)
            return f"Synthesis agent test failed: {run.last_error}"
            
    except Exception as e:
        return f"Error testing synthesis agent: {str(e)}"


if __name__ == "__main__":
    result = test_synthesis_agent()
    print("Synthesis Agent Test Result:")
    print("=" * 50)
    print(result)
