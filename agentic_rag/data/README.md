# 📊 Data Infrastructure for HealthAI Nexus

This folder contains scripts to set up and manage the Azure AI Search infrastructure for the HealthAI Nexus system.

## 🏗️ Files Overview

### Core Setup Scripts

- **`setup_azure_search.py`** - Creates and configures the Azure AI Search index
- **`ingest_healthcare_data.py`** - Ingests sample healthcare documents into the search index
- **`setup_complete.py`** - Complete setup script that runs both index creation and data ingestion

### Test Scripts

- **`../tests/test_azure_search.py`** - Tests the Azure AI Search functionality with various queries

## 🚀 Quick Start

### 1. Environment Setup

Make sure you have the following environment variables set in your `.env` file:

```bash
# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_KEY=your-search-service-key
AZURE_SEARCH_INDEX_NAME=healthcare-documents

# Alternative: Use Azure CLI authentication (no key needed)
# AZURE_CLIENT_ID=your-client-id
# AZURE_TENANT_ID=your-tenant-id
```

### 2. Complete Setup (Recommended)

Run the complete setup script to create the index and ingest data:

```bash
cd agentic_rag
python data/setup_complete.py
```

This will:
- ✅ Create the Azure AI Search index with proper schema
- ✅ Ingest sample healthcare documents
- ✅ Test the search functionality
- ✅ Display index statistics

### 3. Individual Setup Steps

If you prefer to run steps individually:

#### Create the Search Index
```bash
python data/setup_azure_search.py
```

#### Ingest Healthcare Data
```bash
python data/ingest_healthcare_data.py
```

## 🧪 Testing

### Test Azure AI Search
```bash
python tests/test_azure_search.py
```

### Run All Tests
```bash
python tests/run_all_tests.py
```


### Search Capabilities
- **Full-text search** across title, content, and summary
- **Category filtering** by medical specialty
- **Tag-based search** for specific topics
- **Medical terminology** search
- **Relevance scoring** for result ranking

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure `AZURE_SEARCH_KEY` is set correctly
   - Or configure Azure CLI authentication

2. **Index Creation Fails**
   - Check if the search service exists
   - Verify endpoint URL format
   - Ensure sufficient permissions

3. **No Search Results**
   - Run data ingestion to populate the index
   - Check if documents were uploaded successfully
   - Verify search query format

### Verification Steps

1. Check index statistics:
   ```bash
   python -c "from data.ingest_healthcare_data import HealthcareDataIngestion; print(HealthcareDataIngestion().get_index_document_count())"
   ```

2. Test a simple search:
   ```bash
   python -c "from data.ingest_healthcare_data import HealthcareDataIngestion; print(HealthcareDataIngestion().search_documents('diabetes', top=1))"
   ```

## 📈 Next Steps

After setting up the data infrastructure:

1. **Run the HealthAI Nexus application**:
   ```bash
   python app.py
   ```

2. **Test the enhanced version**:
   ```bash
   python app_enhanced.py
   ```

3. **Verify agent functionality** with healthcare queries

The Research Agent will use this search index to find relevant medical information for user queries.
