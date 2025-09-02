"""
Test script for Healthcare Research Agent
"""

import sys
import os
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.research_agent import test_research_agent


def main():
    """Run the research agent test."""
    load_dotenv()
    
    print("🧪 Testing Healthcare Research Agent")
    print("=" * 60)
    
    result = test_research_agent()
    
    print("\n📋 Test Results:")
    print("-" * 40)
    print(result)
    
    if "Error" in result or "failed" in result.lower():
        print("\n❌ Research Agent Test Failed")
        return False
    else:
        print("\n✅ Research Agent Test Passed")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
