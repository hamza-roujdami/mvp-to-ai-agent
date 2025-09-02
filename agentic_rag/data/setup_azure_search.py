"""
Azure AI Search Setup Script for HealthAI Nexus
Creates the Azure AI Search resource, index, and data source for healthcare data
"""

import os
import json
import time
from typing import Dict, List, Optional
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticSearch,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SearchFieldDataType
)
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AzureSearchSetup:
    """Handles Azure AI Search resource setup and configuration."""
    
    def __init__(self):
        """Initialize the Azure Search setup."""
        self.search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.search_key = os.getenv("AZURE_SEARCH_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "healthcare-documents")
        
        if not self.search_endpoint:
            raise ValueError("AZURE_SEARCH_ENDPOINT environment variable is required")
        
        # Use key-based authentication if available, otherwise use DefaultAzureCredential
        if self.search_key:
            self.credential = AzureKeyCredential(self.search_key)
        else:
            self.credential = DefaultAzureCredential()
        
        self.index_client = SearchIndexClient(
            endpoint=self.search_endpoint,
            credential=self.credential
        )
        
        self.search_client = SearchClient(
            endpoint=self.search_endpoint,
            index_name=self.index_name,
            credential=self.credential
        )

    def create_healthcare_index(self) -> bool:
        """
        Create the healthcare documents search index.
        
        Returns:
            bool: True if index was created successfully, False otherwise
        """
        try:
            print(f"🏗️ Creating Azure AI Search index: {self.index_name}")
            
            # Define the search index schema
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
                SearchableField(name="title", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
                SearchableField(name="content", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
                SearchableField(name="summary", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
                SimpleField(name="category", type=SearchFieldDataType.String, filterable=True, facetable=True),
                SimpleField(name="source", type=SearchFieldDataType.String, filterable=True),
                SimpleField(name="last_updated", type=SearchFieldDataType.DateTimeOffset, filterable=True, sortable=True),
                SimpleField(name="relevance_score", type=SearchFieldDataType.Double, filterable=True, sortable=True),
                SearchableField(name="tags", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True, facetable=True),
                SearchableField(name="medical_terms", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
            ]
            
            # Create semantic search configuration
            semantic_config = SemanticConfiguration(
                name="healthcare-semantic-config",
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=SemanticField(field_name="title"),
                    content_fields=[
                        SemanticField(field_name="content"),
                        SemanticField(field_name="summary")
                    ],
                    keywords_fields=[
                        SemanticField(field_name="tags"),
                        SemanticField(field_name="medical_terms")
                    ]
                )
            )
            
            # Create the search index
            index = SearchIndex(
                name=self.index_name,
                fields=fields,
                semantic_search=SemanticSearch(configurations=[semantic_config])
            )
            
            # Create the index
            result = self.index_client.create_or_update_index(index)
            print(f"✅ Index '{self.index_name}' created successfully!")
            print(f"   Index status: {result.status}")
            
            # Wait for index to be ready
            print("⏳ Waiting for index to be ready...")
            time.sleep(10)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create index: {e}")
            return False

    def check_index_exists(self) -> bool:
        """
        Check if the index already exists.
        
        Returns:
            bool: True if index exists, False otherwise
        """
        try:
            self.index_client.get_index(self.index_name)
            print(f"✅ Index '{self.index_name}' already exists")
            return True
        except Exception:
            print(f"ℹ️ Index '{self.index_name}' does not exist")
            return False

    def delete_index(self) -> bool:
        """
        Delete the existing index.
        
        Returns:
            bool: True if index was deleted successfully, False otherwise
        """
        try:
            print(f"🗑️ Deleting index: {self.index_name}")
            self.index_client.delete_index(self.index_name)
            print(f"✅ Index '{self.index_name}' deleted successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to delete index: {e}")
            return False

    def get_index_stats(self) -> Dict:
        """
        Get statistics about the index.
        
        Returns:
            Dict: Index statistics
        """
        try:
            stats = self.index_client.get_index_statistics(self.index_name)
            return {
                "document_count": stats.document_count,
                "storage_size": stats.storage_size,
                "vector_index_size": stats.vector_index_size
            }
        except Exception as e:
            print(f"❌ Failed to get index stats: {e}")
            return {}


def main():
    """Main function to set up Azure AI Search."""
    print("🚀 Setting up Azure AI Search for HealthAI Nexus")
    print("=" * 60)
    
    try:
        # Initialize the setup
        setup = AzureSearchSetup()
        
        # Check if index exists
        if setup.check_index_exists():
            print("\n📊 Current Index Statistics:")
            stats = setup.get_index_stats()
            for key, value in stats.items():
                print(f"   {key}: {value}")
            
            # Ask if user wants to recreate
            response = input("\n❓ Do you want to recreate the index? (y/N): ").strip().lower()
            if response == 'y':
                setup.delete_index()
                setup.create_healthcare_index()
            else:
                print("✅ Using existing index")
        else:
            # Create new index
            setup.create_healthcare_index()
        
        print("\n🎉 Azure AI Search setup completed successfully!")
        print(f"📋 Index Name: {setup.index_name}")
        print(f"🔗 Endpoint: {setup.search_endpoint}")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
