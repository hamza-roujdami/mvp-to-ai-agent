#!/usr/bin/env python3
"""
🧪 Test Coordinator Agent - Multi-Agent Orchestration

This script tests the Coordinator Agent's ability to orchestrate the complete
multi-agent workflow: Research → Analysis → Synthesis.
"""

import sys
import os

# Add parent directory to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.coordinator_agent import create_coordinator_agent, test_coordinator_agent

def main():
    """Test the Coordinator Agent."""
    print("🎯 COORDINATOR AGENT TEST")
    print("=" * 40)
    
    try:
        # Create and test the Coordinator Agent
        coordinator_agent, toolset = create_coordinator_agent()
        test_coordinator_agent()
        print("✅ Coordinator Agent test completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Coordinator Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
