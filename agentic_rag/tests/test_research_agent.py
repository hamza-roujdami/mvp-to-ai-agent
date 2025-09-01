#!/usr/bin/env python3
"""
🧪 Test Research Agent - Azure AI Search Integration

This script tests the Research Agent's ability to search healthcare documents
using Azure AI Search and provide relevant medical information with sources.
"""

import sys
import os

# Add parent directory to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.research_agent import create_research_agent, test_research_agent

def main():
    """Test the Research Agent."""
    print("🔍 RESEARCH AGENT TEST")
    print("=" * 40)
    
    try:
        # Create and test the Research Agent
        research_agent, toolset = create_research_agent()
        test_research_agent(research_agent.id, toolset)
        print("✅ Research Agent test completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Research Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
