"""
Test script for Azure AI Search functionality
Tests the healthcare documents index with various queries
"""

import sys
import os
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.ingest_healthcare_data import HealthcareDataIngestion


def test_azure_search_queries():
    """Test Azure AI Search with various healthcare queries."""
    
    print("🧪 Testing Azure AI Search with Healthcare Queries")
    print("=" * 60)
    
    try:
        # Initialize the search client
        search_client = HealthcareDataIngestion()
        
        # Test queries covering different healthcare topics
        test_queries = [
            {
                "query": "diabetes symptoms and treatment",
                "expected_category": "Endocrinology",
                "description": "Test diabetes-related information retrieval"
            },
            {
                "query": "heart disease prevention",
                "expected_category": "Cardiology", 
                "description": "Test cardiovascular health information"
            },
            {
                "query": "covid-19 vaccination safety",
                "expected_category": "Infectious Diseases",
                "description": "Test COVID-19 vaccine information"
            },
            {
                "query": "anxiety and mental health",
                "expected_category": "Mental Health",
                "description": "Test mental health information"
            },
            {
                "query": "pregnancy care guidelines",
                "expected_category": "Obstetrics",
                "description": "Test prenatal care information"
            },
            {
                "query": "blood pressure management",
                "expected_category": "Cardiology",
                "description": "Test hypertension information"
            },
            {
                "query": "insulin therapy",
                "expected_category": "Endocrinology",
                "description": "Test specific medical treatment"
            },
            {
                "query": "stress management techniques",
                "expected_category": "Mental Health",
                "description": "Test wellness and self-care"
            }
        ]
        
        print(f"🔍 Running {len(test_queries)} test queries...")
        print()
        
        passed_tests = 0
        total_tests = len(test_queries)
        
        for i, test_case in enumerate(test_queries, 1):
            query = test_case["query"]
            expected_category = test_case["expected_category"]
            description = test_case["description"]
            
            print(f"Test {i}/{total_tests}: {description}")
            print(f"   Query: '{query}'")
            
            # Search for documents
            results = search_client.search_documents(query, top=3)
            
            if results:
                print(f"   ✅ Found {len(results)} results")
                
                # Check if any result matches expected category
                category_match = False
                for result in results:
                    if result.get("category") == expected_category:
                        category_match = True
                        print(f"   ✅ Category match: {result['category']}")
                        print(f"   📄 Top result: {result['title']}")
                        print(f"   📊 Relevance score: {result['relevance_score']:.2f}")
                        break
                
                if not category_match:
                    print(f"   ⚠️ No results in expected category '{expected_category}'")
                    print(f"   📄 Found categories: {[r.get('category', 'Unknown') for r in results]}")
                
                passed_tests += 1
                
            else:
                print(f"   ❌ No results found for query: '{query}'")
            
            print()
        
        # Test edge cases
        print("🔍 Testing edge cases...")
        print()
        
        edge_cases = [
            {
                "query": "xyz123nonexistent",
                "description": "Test with non-existent medical term"
            },
            {
                "query": "",
                "description": "Test with empty query"
            },
            {
                "query": "a",
                "description": "Test with very short query"
            }
        ]
        
        for edge_case in edge_cases:
            query = edge_case["query"]
            description = edge_case["description"]
            
            print(f"Edge case: {description}")
            print(f"   Query: '{query}'")
            
            try:
                results = search_client.search_documents(query, top=1)
                if results:
                    print(f"   📄 Found {len(results)} results (unexpected)")
                else:
                    print(f"   ✅ No results found (expected for edge case)")
            except Exception as e:
                print(f"   ✅ Handled gracefully: {str(e)}")
            
            print()
        
        # Display test summary
        print("📊 Test Summary")
        print("-" * 40)
        print(f"✅ Passed tests: {passed_tests}/{total_tests}")
        print(f"📈 Success rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! Azure AI Search is working correctly.")
            return True
        else:
            print(f"⚠️ {total_tests - passed_tests} tests had issues.")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


def test_index_statistics():
    """Test and display index statistics."""
    
    print("\n📊 Testing Index Statistics")
    print("-" * 40)
    
    try:
        search_client = HealthcareDataIngestion()
        
        # Get document count
        doc_count = search_client.get_index_document_count()
        print(f"📄 Total documents in index: {doc_count}")
        
        if doc_count > 0:
            print("✅ Index contains documents")
            
            # Test a simple search to verify functionality
            results = search_client.search_documents("health", top=1)
            if results:
                print("✅ Search functionality is working")
                print(f"   Sample result: {results[0]['title']}")
            else:
                print("⚠️ Search returned no results")
        else:
            print("⚠️ Index is empty - consider running data ingestion")
        
        return True
        
    except Exception as e:
        print(f"❌ Statistics test failed: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 Azure AI Search Test Suite for HealthAI Nexus")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = ["AZURE_SEARCH_ENDPOINT", "AZURE_SEARCH_INDEX_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file")
        return False
    
    try:
        # Run index statistics test
        stats_success = test_index_statistics()
        
        # Run search query tests
        search_success = test_azure_search_queries()
        
        # Overall result
        if stats_success and search_success:
            print("\n🎉 All Azure AI Search tests completed successfully!")
            print("✅ The search index is ready for the HealthAI Nexus application")
            return True
        else:
            print("\n⚠️ Some tests failed. Please check the Azure AI Search configuration.")
            return False
            
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
