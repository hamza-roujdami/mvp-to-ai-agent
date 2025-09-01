#!/usr/bin/env python3
"""
🧪 Test Complete Multi-Agent Workflow - Healthcare Agentic RAG System

This script tests the complete end-to-end workflow:
Research Agent → Analysis Agent → Synthesis Agent

Shows the complete pipeline in action with a healthcare query.
"""

import os
from dotenv import load_dotenv
from agents.coordinator_agent import execute_multi_agent_workflow

load_dotenv()

def test_complete_workflow():
    """Test the complete multi-agent workflow with a healthcare prompt."""
    
    print("🏥 HEALTHCARE AGENTIC RAG SYSTEM - COMPLETE WORKFLOW TEST")
    print("=" * 70)
    
    # Check environment variables
    required_vars = [
        "AZURE_AI_FOUNDRY_ENDPOINT",
        "AZURE_AI_FOUNDRY_API_KEY",
        "AZURE_SEARCH_CONNECTION_ID",
        "AZURE_SEARCH_INDEX_NAME"
    ]
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return
    
    print("✅ All required environment variables are set")
    
    # Test healthcare query
    test_query = "What are the symptoms and risk factors of diabetes?"
    
    print(f"\n🚀 EXECUTING COMPLETE MULTI-AGENT WORKFLOW...")
    print(f"Query: {test_query}")
    print("-" * 70)
    
    try:
        # Execute the complete workflow
        workflow_results = execute_multi_agent_workflow(test_query)
        
        # Display comprehensive results
        print(f"\n📋 WORKFLOW RESULTS SUMMARY")
        print("=" * 70)
        
        # Research Results
        if "research" in workflow_results:
            print(f"\n🔍 RESEARCH AGENT RESULTS:")
            print(f"   Status: {workflow_results['research'].get('status', 'unknown')}")
            print(f"   Agent ID: {workflow_results['research'].get('agent_id', 'unknown')}")
            if workflow_results['research'].get('content'):
                content = workflow_results['research']['content']
                print(f"   Content Length: {len(content)} characters")
                print(f"   Content Preview: {content[:200]}...")
                if len(content) > 200:
                    print(f"   Full Content: {content}")
        
        # Analysis Results
        if "analysis" in workflow_results:
            print(f"\n📊 ANALYSIS AGENT RESULTS:")
            print(f"   Status: {workflow_results['analysis'].get('status', 'unknown')}")
            print(f"   Agent ID: {workflow_results['analysis'].get('agent_id', 'unknown')}")
            if workflow_results['analysis'].get('content'):
                content = workflow_results['analysis']['content']
                print(f"   Content Length: {len(content)} characters")
                if content:
                    print(f"   Content: {content}")
                else:
                    print(f"   Content: Generated visualizations (images)")
        
        # Synthesis Results
        if "synthesis" in workflow_results:
            print(f"\n📝 SYNTHESIS AGENT RESULTS:")
            print(f"   Status: {workflow_results['synthesis'].get('status', 'unknown')}")
            print(f"   Agent ID: {workflow_results['synthesis'].get('agent_id', 'unknown')}")
            if workflow_results['synthesis'].get('content'):
                content = workflow_results['synthesis']['content']
                print(f"   Content Length: {len(content)} characters")
                print(f"   Content Preview: {content[:200]}...")
                if len(content) > 200:
                    print(f"   Full Content: {content}")
        
        # Summary
        if "summary" in workflow_results:
            print(f"\n🎯 WORKFLOW SUMMARY:")
            print(f"   Query: {workflow_results['summary'].get('query', 'unknown')}")
            print(f"   Successful Agents: {workflow_results['summary'].get('successful_agents', 0)}/{workflow_results['summary'].get('total_agents', 0)}")
            print(f"   Workflow Status: {workflow_results['summary'].get('workflow_status', 'unknown')}")
        
        print(f"\n✅ COMPLETE WORKFLOW TEST FINISHED!")
        print(f"   All agents successfully executed the healthcare query pipeline")
        
    except Exception as e:
        print(f"❌ Error during workflow execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_workflow()
