#!/usr/bin/env python3
"""
🧪 Test Analysis Agent - Code Interpreter Integration

This script tests the Analysis Agent's ability to analyze healthcare data
using Code Interpreter and create visualizations and insights.
"""

import sys
import os

# Add parent directory to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.analysis_agent import create_analysis_agent, test_analysis_agent

def main():
    """Test the Analysis Agent."""
    print("📊 ANALYSIS AGENT TEST")
    print("=" * 40)
    
    try:
        # Create and test the Analysis Agent
        analysis_agent, toolset = create_analysis_agent()
        test_analysis_agent(analysis_agent.id, toolset)
        print("✅ Analysis Agent test completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Analysis Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
