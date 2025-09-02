"""
Test script for Healthcare Analysis Agent
"""

import sys
import os
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.analysis_agent import test_analysis_agent


def main():
    """Run the analysis agent test."""
    load_dotenv()
    
    print("🧪 Testing Healthcare Analysis Agent")
    print("=" * 60)
    
    result = test_analysis_agent()
    
    print("\n📋 Test Results:")
    print("-" * 40)
    print(result)
    
    if "Error" in result or "failed" in result.lower():
        print("\n❌ Analysis Agent Test Failed")
        return False
    else:
        print("\n✅ Analysis Agent Test Passed")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
