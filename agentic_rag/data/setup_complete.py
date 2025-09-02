"""
Complete Setup Script for HealthAI Nexus Data Infrastructure
Sets up Azure AI Search and ingests healthcare data in one go
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.setup_azure_search import AzureSearchSetup
from data.ingest_healthcare_data import HealthcareDataIngestion

# Load environment variables
load_dotenv()


def check_environment_variables():
    """Check if all required environment variables are set."""
    required_vars = [
        "AZURE_SEARCH_ENDPOINT",
        "AZURE_SEARCH_INDEX_NAME"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file")
        return False
    
    # Check if at least one authentication method is available
    if not os.getenv("AZURE_SEARCH_KEY") and not os.getenv("AZURE_CLIENT_ID"):
        print("⚠️ Warning: No authentication method found.")
        print("   Please set either AZURE_SEARCH_KEY or configure Azure CLI authentication")
        return False
    
    return True


def main():
    """Main function to set up the complete data infrastructure."""
    print("🚀 HealthAI Nexus - Complete Data Infrastructure Setup")
    print("=" * 70)
    
    # Check environment variables
    if not check_environment_variables():
        return False
    
    try:
        # Step 1: Set up Azure AI Search
        print("\n📋 Step 1: Setting up Azure AI Search...")
        print("-" * 50)
        
        search_setup = AzureSearchSetup()
        
        # Check if index exists
        if search_setup.check_index_exists():
            print("✅ Index already exists")
            stats = search_setup.get_index_stats()
            if stats:
                print(f"   Documents: {stats.get('document_count', 0)}")
                print(f"   Storage: {stats.get('storage_size', 0)} bytes")
        else:
            # Create new index
            if not search_setup.create_healthcare_index():
                print("❌ Failed to create Azure AI Search index")
                return False
        
        # Step 2: Ingest healthcare data
        print("\n📋 Step 2: Ingesting healthcare data...")
        print("-" * 50)
        
        data_ingestion = HealthcareDataIngestion()
        
        # Check current document count
        current_count = data_ingestion.get_index_document_count()
        print(f"📊 Current documents in index: {current_count}")
        
        if current_count == 0:
            # Get and ingest sample documents
            documents = data_ingestion.get_sample_healthcare_documents()
            print(f"📋 Prepared {len(documents)} healthcare documents for ingestion")
            
            if not data_ingestion.ingest_documents(documents):
                print("❌ Failed to ingest healthcare data")
                return False
            
            # Verify ingestion
            new_count = data_ingestion.get_index_document_count()
            print(f"✅ Successfully added {new_count - current_count} documents")
        else:
            print("✅ Index already contains documents")
        
        # Step 3: Test the setup
        print("\n📋 Step 3: Testing the setup...")
        print("-" * 50)
        
        test_queries = [
            "diabetes symptoms and treatment",
            "heart disease prevention strategies",
            "covid-19 vaccination guidelines",
            "mental health and anxiety management",
            "pregnancy care and prenatal health"
        ]
        
        print("🔍 Testing search functionality with sample queries:")
        for query in test_queries:
            results = data_ingestion.search_documents(query, top=1)
            if results:
                print(f"   ✅ '{query}' -> Found: {results[0]['title']}")
            else:
                print(f"   ❌ '{query}' -> No results found")
        
        # Step 4: Display final status
        print("\n📋 Step 4: Final Status...")
        print("-" * 50)
        
        final_stats = search_setup.get_index_stats()
        if final_stats:
            print(f"📊 Index Statistics:")
            print(f"   Index Name: {search_setup.index_name}")
            print(f"   Document Count: {final_stats.get('document_count', 0)}")
            print(f"   Storage Size: {final_stats.get('storage_size', 0)} bytes")
            print(f"   Endpoint: {search_setup.search_endpoint}")
        
        print("\n🎉 HealthAI Nexus data infrastructure setup completed successfully!")
        print("✅ Azure AI Search index is ready")
        print("✅ Healthcare documents are ingested")
        print("✅ Search functionality is working")
        print("\n🚀 You can now run the HealthAI Nexus application!")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
