#!/usr/bin/env python3
"""
🧪 Test Synthesis Agent - Response Generation

This script tests the Synthesis Agent's ability to synthesize research findings
and analysis insights into comprehensive, patient-friendly healthcare responses.
"""

import sys
import os

# Add parent directory to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.synthesis_agent import create_synthesis_agent, test_synthesis_agent

def main():
    """Test the Synthesis Agent."""
    print("📝 SYNTHESIS AGENT TEST")
    print("=" * 40)
    
    try:
        # Create and test the Synthesis Agent
        synthesis_agent, toolset = create_synthesis_agent()
        test_synthesis_agent(synthesis_agent.id, toolset)
        print("✅ Synthesis Agent test completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Synthesis Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
