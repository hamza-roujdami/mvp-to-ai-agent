"""
End-to-End Flow Test for Healthcare Connected Agents System
Tests the complete workflow from user query to final response
"""

import sys
import os
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator_agent import test_orchestrator_agent


def main():
    """Run the end-to-end flow test."""
    load_dotenv()
    
    print("🧪 Testing End-to-End Healthcare Connected Agents Flow")
    print("=" * 70)
    print("This test will:")
    print("1. Create all connected agents (Research, Analysis, Synthesis)")
    print("2. Create the main orchestrator agent")
    print("3. Test a complete healthcare query workflow")
    print("4. Verify the response contains research, analysis, and synthesis")
    print("=" * 70)
    
    result = test_orchestrator_agent()
    
    print("\n📋 End-to-End Test Results:")
    print("-" * 50)
    print(result)
    
    # Check if the response contains expected components
    success_indicators = [
        "research" in result.lower(),
        "analysis" in result.lower(),
        "treatment" in result.lower() or "diabetes" in result.lower(),
        len(result) > 500  # Substantial response
    ]
    
    success_count = sum(success_indicators)
    
    print(f"\n📊 Success Indicators: {success_count}/4")
    print(f"   - Contains research content: {'✅' if success_indicators[0] else '❌'}")
    print(f"   - Contains analysis content: {'✅' if success_indicators[1] else '❌'}")
    print(f"   - Contains treatment/diabetes info: {'✅' if success_indicators[2] else '❌'}")
    print(f"   - Substantial response length: {'✅' if success_indicators[3] else '❌'}")
    
    if "Error" in result or "failed" in result.lower() or success_count < 3:
        print("\n❌ End-to-End Flow Test Failed")
        return False
    else:
        print("\n✅ End-to-End Flow Test Passed")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
