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
        
        print("\n✅ Cleanup completed!")
        print(f"   - {threads_deleted} threads deleted")
        print(f"   - {agents_deleted} agents deleted")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("⚠️  WARNING: This will delete ALL agents and threads!")
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        success = cleanup_azure_foundry()
        if success:
            print("\n🎉 Azure AI Foundry cleaned up successfully!")
        else:
            print("\n❌ Cleanup failed!")
    else:
        print("❌ Cleanup cancelled.")
