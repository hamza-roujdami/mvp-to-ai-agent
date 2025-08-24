#!/usr/bin/env python3
"""
MVP RAG Healthcare AI Assistant Demo

This demonstrates a real RAG system using local AI tools:
- Ollama for LLM and embeddings
- Qdrant for vector storage
- Real semantic search and generation
"""

import sys
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from core.rag_engine import RAGEngine
from utils.logger import get_logger

logger = get_logger("main")

def main():
    """Run the MVP RAG demo."""
    print("🏥 MVP RAG Healthcare AI Assistant Demo")
    print("=" * 60)
    print("🚀 Real RAG with Local AI Tools: Ollama + Qdrant")
    print()
    
    # Initialize the RAG engine
    print("🔧 Initializing RAG Engine...")
    try:
        rag_engine = RAGEngine()
        print("✅ RAG Engine initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize RAG Engine: {e}")
        print("Please ensure Ollama and Qdrant are running")
        return
    
    # Health check
    print("\n🏥 Health Check:")
    health = rag_engine.health_check()
    for service, status in health.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {service}: {'Healthy' if status else 'Unhealthy'}")
    
    if not health["overall"]:
        print("\n❌ System health check failed. Please check services.")
        return
    
    # System info
    print("\n📊 System Information:")
    system_info = rag_engine._get_system_info()
    print(f"   RAG Engine: {system_info['rag_engine']}")
    print(f"   LLM Model: {system_info['llm_model']}")
    print(f"   Embedding Model: {system_info['embedding_model']}")
    print(f"   Vector Store: {system_info['vector_store']}")
    
    # Demo queries
    demo_queries = [
        "What are the symptoms of diabetes?",
        "How do I check my blood pressure at home?",
        "What should I do if I have chest pain?",
        "How do I manage stress and anxiety?",
        "What are the benefits of regular exercise?"
    ]
    
    print(f"\n💡 Demo Queries Available: {len(demo_queries)}")
    for i, query in enumerate(demo_queries, 1):
        print(f"   {i}. {query}")
    
    # Interactive demo
    print(f"\n🎭 Interactive Demo Mode")
    print("Type 'quit' to exit, 'demo' to run sample queries, or ask a health question.")
    print("Type 'health' to check system status.")
    
    while True:
        try:
            user_input = input("\n🏥 Your health question: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Thanks for trying the MVP RAG Healthcare AI Assistant!")
                break
            
            elif user_input.lower() == 'demo':
                print("\n🎬 Running sample queries...")
                for query in demo_queries[:3]:  # Show first 3
                    print(f"\n--- Query: {query} ---")
                    result = rag_engine.query(query)
                    print(f"Response: {result['response'][:200]}...")
                    print(f"Documents Retrieved: {result['metrics']['documents_retrieved']}")
                    print(f"Total Time: {result['metrics']['total_time_ms']}ms")
                continue
            
            elif user_input.lower() == 'health':
                print("\n🏥 System Health Check:")
                health = rag_engine.health_check()
                for service, status in health.items():
                    status_icon = "✅" if status else "❌"
                    print(f"   {status_icon} {service}: {'Healthy' if status else 'Unhealthy'}")
                continue
            
            elif not user_input:
                continue
            
            # Process the user's health question
            print(f"\n🔍 Processing: {user_input}")
            start_time = time.time()
            
            result = rag_engine.query(user_input)
            
            # Display results
            print(f"\n📝 Response:")
            print(result['response'])
            
            print(f"\n📊 Performance Metrics:")
            print(f"   Total Time: {result['metrics']['total_time_ms']}ms")
            print(f"   Embedding Time: {result['metrics']['embedding_time_ms']}ms")
            print(f"   Search Time: {result['metrics']['search_time_ms']}ms")
            print(f"   Generation Time: {result['metrics']['generation_time_ms']}ms")
            print(f"   Documents Retrieved: {result['metrics']['documents_retrieved']}")
            print(f"   Average Similarity Score: {result['metrics']['average_similarity_score']}")
            
            # Show retrieved context
            if result['context']['retrieved_documents']:
                print(f"\n📚 Retrieved Context:")
                print(f"   {result['context']['context_summary']}")
                
                # Show top document
                top_doc = result['context']['retrieved_documents'][0]
                print(f"\n   Top Document (Score: {top_doc['score']:.3f}):")
                print(f"   Source: {top_doc.get('source', 'Unknown')}")
                print(f"   Content: {top_doc['content'][:150]}...")
            
            # Show what this demonstrates
            print(f"\n💡 What This Demonstrates:")
            print(f"   ✅ Real RAG with local AI tools")
            print(f"   ✅ Semantic search with embeddings")
            print(f"   ✅ Dynamic LLM responses")
            print(f"   ✅ Performance metrics and monitoring")
            
            # Show next steps
            print(f"\n🚀 Next Steps to Production:")
            print(f"   🔄 Replace Ollama with Azure OpenAI")
            print(f"   🔄 Replace Qdrant with Azure AI Search")
            print(f"   🔄 Add Content Safety and compliance")
            print(f"   🔄 Add agentic workflow and tools")
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Thanks for trying!")
            break
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            print(f"\n❌ Error: {e}")
            print("This demonstrates another limitation of the MVP - error handling.")
    
    # Final summary
    print(f"\n🎯 Demo Complete!")
    print("This MVP shows a REAL RAG system working with local AI tools.")
    print("The production version will have:")
    print("   ✅ Azure OpenAI for enterprise LLM")
    print("   ✅ Azure AI Search for scalable vectors")
    print("   ✅ Content Safety for compliance")
    print("   ✅ Full observability and monitoring")

if __name__ == "__main__":
    main()
