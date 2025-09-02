"""
Run all tests for the Healthcare Connected Agents System
"""

import sys
import os
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_research_agent import main as test_research
from test_analysis_agent import main as test_analysis
from test_synthesis_agent import main as test_synthesis
from test_end_to_end_flow import main as test_e2e
from test_azure_search import main as test_azure_search


def main():
    """Run all tests in sequence."""
    load_dotenv()
    
    print("🧪 Running All Healthcare Connected Agents Tests")
    print("=" * 70)
    
    tests = [
        ("Azure AI Search", test_azure_search),
        ("Research Agent", test_research),
        ("Analysis Agent", test_analysis),
        ("Synthesis Agent", test_synthesis),
        ("End-to-End Flow", test_e2e)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} Test...")
        print("-" * 40)
        
        try:
            success = test_func()
            results.append((test_name, success))
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"\n{test_name} Test: {status}")
        except Exception as e:
            print(f"\n❌ {test_name} Test: ERROR - {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:20} {status}")
    
    print("-" * 70)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The Healthcare Connected Agents System is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the individual test results.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
