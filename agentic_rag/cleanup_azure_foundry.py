#!/usr/bin/env python3
"""
Azure AI Foundry Cleanup Script
Cleans up all agents and threads from your Azure AI Foundry project
"""

import os
import sys
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from datetime import datetime, timedelta

def cleanup_application_insights_traces():
    """Clean up traces from Application Insights"""
    
    print("🧹 Cleaning up Application Insights traces...")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get Application Insights connection string
    connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
    if not connection_string:
        print("   ⚠️  No Application Insights connection string found")
        print("   💡 Make sure APPLICATIONINSIGHTS_CONNECTION_STRING is set in your .env file")
        return False
    
    try:
        # Extract workspace ID from connection string
        # Format: InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/
        parts = connection_string.split(';')
        workspace_id = None
        for part in parts:
            if part.startswith('IngestionEndpoint='):
                endpoint = part.split('=')[1]
                # Extract workspace ID from endpoint
                if '.in.applicationinsights.azure.com' in endpoint:
                    # Remove https:// and .in.applicationinsights.azure.com/
                    workspace_id = endpoint.replace('https://', '').replace('.in.applicationinsights.azure.com/', '')
                    break
        
        if not workspace_id:
            print("   ⚠️  Could not extract workspace ID from connection string")
            return False
        
        print(f"   📊 Found Application Insights workspace: {workspace_id}")
        
        print("   ℹ️  Application Insights traces cannot be deleted via API")
        print("   💡 Traces will automatically expire based on your retention policy")
        print("   💡 You can adjust retention settings in the Azure portal")
        print("   💡 Default retention is usually 90 days")
        print("   💡 To view traces, go to Azure AI Foundry → Monitoring → Application analytics")
        print("   💡 To view detailed traces, go to Azure AI Foundry → Tracing tab")
        
        return True
        
    except Exception as e:
        print(f"   ⚠️  Error querying Application Insights: {e}")
        return False

def cleanup_azure_foundry():
    """Clean up all agents and threads from Azure AI Foundry"""
    
    # Load environment variables
    load_dotenv()
    
    # Extract project name from endpoint
    endpoint = os.getenv('AZURE_AI_FOUNDRY_ENDPOINT')
    if not endpoint:
        print("❌ AZURE_AI_FOUNDRY_ENDPOINT not found in environment variables")
        return False
        
    if 'projects' in endpoint:
        parts = endpoint.split('/')
        project_index = parts.index('projects')
        if project_index + 1 < len(parts):
            os.environ['AZURE_AI_FOUNDRY_PROJECT_NAME'] = parts[project_index + 1]
    
    print("🧹 Azure AI Foundry Cleanup")
    print("=" * 50)
    
    try:
        # Create client
        project_client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(),
        )
        
        # Clean up threads first
        print("🧵 Cleaning up threads...")
        threads_deleted = 0
        try:
            threads = list(project_client.agents.threads.list())
            for thread in threads:
                try:
                    project_client.agents.threads.delete(thread.id)
                    threads_deleted += 1
                    print(f"   ✅ Deleted thread: {thread.id}")
                except Exception as e:
                    print(f"   ⚠️  Failed to delete thread {thread.id}: {e}")
        except Exception as e:
            print(f"   ⚠️  Error listing threads: {e}")
        
        print(f"🧵 Deleted {threads_deleted} threads")
        
        # Clean up agents
        print("🤖 Cleaning up agents...")
        agents_deleted = 0
        try:
            agents = list(project_client.agents.list())
            for agent in agents:
                try:
                    project_client.agents.delete(agent.id)
                    agents_deleted += 1
                    print(f"   ✅ Deleted agent: {agent.name} ({agent.id})")
                except Exception as e:
                    print(f"   ⚠️  Failed to delete agent {agent.name}: {e}")
        except Exception as e:
            print(f"   ⚠️  Error listing agents: {e}")
        
        print(f"🤖 Deleted {agents_deleted} agents")
        
        # Clean up Application Insights traces
        cleanup_application_insights_traces()
        
        print("\n✅ Cleanup completed!")
        print(f"   - {threads_deleted} threads deleted")
        print(f"   - {agents_deleted} agents deleted")
        print("   - Application Insights traces checked")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_traces_only():
    """Clean up only Application Insights traces"""
    print("🧹 Application Insights Traces Cleanup")
    print("=" * 50)
    
    success = cleanup_application_insights_traces()
    
    if success:
        print("\n🎉 Application Insights traces checked successfully!")
    else:
        print("\n❌ Trace cleanup failed!")

if __name__ == "__main__":
    print("🧹 Azure AI Foundry Cleanup Options")
    print("=" * 50)
    print("1. Clean everything (agents, threads, and check traces)")
    print("2. Clean only Application Insights traces")
    print("3. Cancel")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        print("\n⚠️  WARNING: This will delete ALL agents and threads!")
        response = input("Are you sure you want to continue? (yes/no): ")
        
        if response.lower() in ['yes', 'y']:
            success = cleanup_azure_foundry()
            if success:
                print("\n🎉 Azure AI Foundry cleaned up successfully!")
            else:
                print("\n❌ Cleanup failed!")
        else:
            print("❌ Cleanup cancelled.")
    
    elif choice == "2":
        cleanup_traces_only()
    
    elif choice == "3":
        print("❌ Cleanup cancelled.")
    
    else:
        print("❌ Invalid choice. Cleanup cancelled.")
