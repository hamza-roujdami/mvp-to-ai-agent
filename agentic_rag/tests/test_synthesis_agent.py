"""
Test script for Healthcare Synthesis Agent
"""

import sys
import os
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.synthesis_agent import test_synthesis_agent


def main():
    """Run the synthesis agent test."""
    load_dotenv()
    
    print("🧪 Testing Healthcare Synthesis Agent")
    print("=" * 60)
    
    result = test_synthesis_agent()
    
    print("\n📋 Test Results:")
    print("-" * 40)
    print(result)
    
    if "Error" in result or "failed" in result.lower():
        print("\n❌ Synthesis Agent Test Failed")
        return False
    else:
        print("\n✅ Synthesis Agent Test Passed")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
