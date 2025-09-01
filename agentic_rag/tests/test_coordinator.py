#!/usr/bin/env python3
"""
🧪 Test Coordinator with Streaming

This script tests the coordinator that implements:
- True parallel execution
- Real-time progress streaming
- Advanced performance optimization
"""

import time
import sys
import os

# Add parent directory to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def progress_callback(message: str):
    """Progress callback function for streaming updates."""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def test_coordinator():
    """Test the coordinator with streaming."""
    print("🚀 Testing Coordinator with Streaming...")
    print("=" * 60)
    
    try:
        from agents.coordinator_agent import execute_multi_agent_workflow
        
        start_time = time.time()
        
        # Execute with streaming progress updates
        result = execute_multi_agent_workflow(
            "What are the symptoms and risk factors of diabetes?",
            progress_callback=progress_callback
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("📊 COORDINATOR RESULTS")
        print("=" * 60)
        
        # Show results summary
        if 'summary' in result:
            print(f"✅ Workflow Status: {result['summary']['workflow_status']}")
            print(f"✅ Successful Agents: {result['summary']['successful_agents']}/{result['summary']['total_agents']}")
            print(f"⏱️  Execution Time: {result['summary'].get('execution_time', duration):.2f} seconds")
        
        # Show content lengths
        if 'research' in result and result['research']['status'] == 'completed':
            print(f"🔍 Research Content: {len(result['research']['content'])} characters")
        
        if 'analysis' in result and result['analysis']['status'] == 'completed':
            print(f"📊 Analysis Content: {len(result['analysis']['content'])} characters")
        
        if 'synthesis' in result and result['synthesis']['status'] == 'completed':
            print(f"📝 Synthesis Content: {len(result['synthesis']['content'])} characters")
        
        print(f"\n🎉 COORDINATOR COMPLETED!")
        print(f"⏱️  Total Time: {duration:.2f} seconds")
        
        return duration, result
        
    except Exception as e:
        print(f"❌ Coordinator test failed: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def main():
    """Run coordinator test."""
    print("🧪 COORDINATOR PERFORMANCE TEST")
    print("=" * 60)
    print("💡 This coordinator implements:")
    print("   • True parallel execution of Research + Analysis agents")
    print("   • Real-time progress streaming")
    print("   • Advanced connection pooling")
    print("   • Performance metrics tracking")
    print("=" * 60)
    
    # Test coordinator
    duration, result = test_coordinator()
    
    if duration:
        print(f"\n🎉 SUCCESS: Coordinator completed in {duration:.2f} seconds!")
        print(f"💡 Expected improvements:")
        print(f"   • Parallel execution should reduce Analysis + Synthesis time")
        print(f"   • Streaming provides real-time progress updates")
        print(f"   • Connection pooling reduces Azure API overhead")
    else:
        print("\n❌ Test failed - check the error above")

if __name__ == "__main__":
    main()
