#!/usr/bin/env python3
"""
📚 Data Ingestion Script for MVP RAG Healthcare AI Assistant

This script populates the Qdrant vector database with healthcare documents
and their embeddings. It demonstrates:

- Sample healthcare document creation
- Embedding generation using Ollama
- Vector database population
- Health monitoring and validation
- Error handling and logging

The documents cover common healthcare topics including:
- Diabetes symptoms and management
- Blood pressure monitoring
- Emergency symptoms recognition
- Stress management and mental health
- Exercise benefits and guidelines
- Sleep health and recommendations
- Preventive healthcare guidelines
- First aid essentials

Author: AI Evolution Demo Team
Purpose: Populate MVP RAG system with healthcare knowledge base
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.llm_client import OllamaClient
from core.vector_store import QdrantVectorStore
from utils.logger import get_logger

# Initialize logging for data ingestion
logger = get_logger("data_ingestion")


def create_sample_documents():
    """
    Create comprehensive sample healthcare documents for the MVP.
    
    This function creates a diverse set of healthcare documents covering:
    - Common chronic conditions (diabetes, cardiovascular health)
    - Emergency situations and symptoms
    - Mental health and stress management
    - Lifestyle and preventive care
    - First aid and emergency preparedness
    
    Each document includes:
    - Descriptive title for easy identification
    - Comprehensive content with actionable information
    - Source attribution for credibility
    - Metadata for categorization and filtering
    
    Returns:
        List of document dictionaries ready for embedding and storage
    """
    documents = [
        {
            "title": "Diabetes Symptoms and Management",
            "content": "Diabetes is a chronic condition that affects how your body turns food into energy. Common symptoms include frequent urination, increased thirst, extreme hunger, unexplained weight loss, fatigue, blurred vision, slow-healing sores, and frequent infections. Management involves monitoring blood sugar, healthy eating, regular exercise, and medication when prescribed by healthcare providers.",
            "source": "Healthcare Guidelines",
            "metadata": {"category": "diabetes", "type": "symptoms"}
        },
        {
            "title": "Blood Pressure Monitoring at Home",
            "content": "Home blood pressure monitoring is an important part of managing cardiovascular health. Use a validated automatic monitor, sit quietly for 5 minutes before measuring, place the cuff on your upper arm at heart level, take multiple readings and average them, and record readings in a log. Normal blood pressure is typically below 120/80 mmHg.",
            "source": "Cardiovascular Health Guide",
            "metadata": {"category": "cardiovascular", "type": "monitoring"}
        },
        {
            "title": "Emergency Symptoms - When to Seek Help",
            "content": "Certain symptoms require immediate medical attention. Chest pain, especially if severe, crushing, or accompanied by shortness of breath, nausea, or pain radiating to your arm or jaw, can indicate a heart attack. Sudden severe headache, confusion, trouble walking, and vision problems can indicate a stroke. Call emergency services immediately for these symptoms.",
            "source": "Emergency Medicine Guidelines",
            "metadata": {"category": "emergency", "type": "symptoms"}
        },
        {
            "title": "Stress Management and Mental Health",
            "content": "Effective stress management is crucial for overall health. Techniques include regular exercise, deep breathing exercises, meditation, getting adequate sleep, maintaining a healthy diet, limiting caffeine and alcohol, and seeking professional help when needed. It's important to identify stress triggers and develop healthy coping mechanisms.",
            "source": "Mental Health Resources",
            "metadata": {"category": "mental_health", "type": "management"}
        },
        {
            "title": "Exercise Benefits for Health",
            "content": "Regular exercise provides numerous health benefits including improved cardiovascular health, stronger muscles and bones, better mental health, weight management, improved sleep, increased energy, reduced risk of chronic diseases, and enhanced immune function. Aim for at least 150 minutes of moderate exercise per week.",
            "source": "Physical Activity Guidelines",
            "metadata": {"category": "lifestyle", "type": "exercise"}
        },
        {
            "title": "Sleep and Health",
            "content": "Quality sleep is essential for health and well-being. Adults typically need 7-9 hours of sleep per night. Signs of adequate sleep include feeling rested upon waking, maintaining energy throughout the day, not needing caffeine to function, and falling asleep within 15-20 minutes of going to bed. Poor sleep can affect mood, cognitive function, and physical health.",
            "source": "Sleep Medicine Research",
            "metadata": {"category": "lifestyle", "type": "sleep"}
        },
        {
            "title": "Preventive Healthcare Guidelines",
            "content": "Preventive healthcare helps catch health issues early and maintain wellness. Most healthy adults should get physical exams every 1-3 years, with frequency varying based on age, health status, and risk factors. Adults over 50 may need annual exams, while younger adults with no health issues might only need exams every 2-3 years.",
            "source": "Preventive Medicine Standards",
            "metadata": {"category": "prevention", "type": "guidelines"}
        },
        {
            "title": "First Aid Essentials",
            "content": "A basic first aid kit should contain adhesive bandages, sterile gauze pads, medical tape, antiseptic wipes, pain relievers, tweezers, scissors, instant cold packs, emergency blanket, and emergency contact information. Knowing basic first aid can make a significant difference in emergency situations.",
            "source": "First Aid Training Manual",
            "metadata": {"category": "emergency", "type": "first_aid"}
        }
    ]
    
    logger.info(f"📚 Created {len(documents)} sample healthcare documents")
    return documents


def ingest_documents(documents, llm_client, vector_store):
    """
    Ingest documents into the vector database with embeddings.
    
    This function:
    - Generates embeddings for each document using Ollama
    - Stores documents and embeddings in Qdrant
    - Provides progress tracking and error handling
    - Validates the ingestion process
    
    Args:
        documents: List of document dictionaries
        llm_client: Initialized Ollama client for embeddings
        vector_store: Initialized Qdrant vector store
        
    Returns:
        bool: True if ingestion successful, False otherwise
    """
    print(f"\n🚀 Starting document ingestion...")
    print(f"   Documents to process: {len(documents)}")
    
    try:
        # Generate embeddings for all documents
        print("   🔍 Generating embeddings...")
        embeddings = []
        
        for i, doc in enumerate(documents, 1):
            try:
                # Generate embedding using nomic-embed-text model
                embedding = llm_client.embed("nomic-embed-text", doc["content"])
                embeddings.append(embedding)
                
                # Progress indicator
                if i % 2 == 0 or i == len(documents):
                    print(f"      Processed {i}/{len(documents)} documents")
                    
            except Exception as e:
                logger.error(f"❌ Failed to generate embedding for document {i}: {e}")
                print(f"      ❌ Failed to embed document {i}: {doc['title']}")
                return False
        
        print(f"   ✅ Generated {len(embeddings)} embeddings successfully")
        
        # Store documents and embeddings in vector database
        print("   💾 Storing in vector database...")
        doc_ids = vector_store.add_documents(documents, embeddings)
        
        if len(doc_ids) == len(documents):
            print(f"   ✅ Stored {len(doc_ids)} documents successfully")
            
            # Verify storage
            collection_info = vector_store.get_collection_info()
            print(f"   📊 Collection status: {collection_info.get('points_count', 0)} documents stored")
            
            return True
        else:
            print(f"   ❌ Document count mismatch: expected {len(documents)}, got {len(doc_ids)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Document ingestion failed: {e}")
        print(f"   ❌ Ingestion failed: {e}")
        return False


def main():
    """
    Main data ingestion function for the MVP RAG system.
    
    This function orchestrates the entire ingestion process:
    1. Client initialization and health checks
    2. Sample document creation
    3. Document embedding generation
    4. Vector database population
    5. Validation and status reporting
    
    The process demonstrates:
    - Production-ready error handling
    - Health monitoring and validation
    - Progress tracking and user feedback
    - Comprehensive logging and reporting
    """
    print("📚 Data Ingestion for MVP RAG Healthcare AI Assistant")
    print("=" * 60)
    
    # Step 1: Initialize clients
    print("\n🔧 Initializing clients...")
    try:
        llm_client = OllamaClient()
        vector_store = QdrantVectorStore()
        print("   ✅ Clients initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize clients: {e}")
        print(f"   ❌ Failed to initialize clients: {e}")
        print("\n💡 Troubleshooting:")
        print("   - Ensure Ollama is running: ollama serve")
        print("   - Ensure Qdrant is running: docker run -d --name qdrant -p 6333:6333 qdrant/qdrant")
        return
    
    # Step 2: Health checks
    print("\n🏥 Health Checks:")
    ollama_healthy = llm_client.health_check()
    qdrant_healthy = vector_store.health_check()
    
    print(f"   {'✅' if ollama_healthy else '❌'} Ollama: {'Healthy' if ollama_healthy else 'Unhealthy'}")
    print(f"   {'✅' if qdrant_healthy else '❌'} Qdrant: {'Healthy' if qdrant_healthy else 'Unhealthy'}")
    
    if not (ollama_healthy and qdrant_healthy):
        print("\n❌ Health checks failed. Please ensure services are running.")
        print("\n💡 Service Status:")
        print("   - Ollama: ollama list")
        print("   - Qdrant: curl http://localhost:6333/collections")
        return
    
    # Step 3: Create sample documents
    print("\n📝 Creating sample healthcare documents...")
    documents = create_sample_documents()
    print(f"   ✅ Created {len(documents)} documents")
    
    # Step 4: Ingest documents
    success = ingest_documents(documents, llm_client, vector_store)
    
    # Step 5: Final status and next steps
    if success:
        print("\n🎉 Data ingestion completed successfully!")
        print("\n🚀 Next steps:")
        print("   1. Launch the Gradio UI: python app.py")
        print("   2. Open your browser to: http://localhost:7860")
        print("   3. Ask healthcare questions to test the RAG system")
        print("\n💡 Sample questions to try:")
        print("   - What are the symptoms of diabetes?")
        print("   - How do I check my blood pressure at home?")
        print("   - What should I do if I have chest pain?")
        print("   - How do I manage stress and anxiety?")
    else:
        print("\n❌ Data ingestion failed. Please check the logs and try again.")
        print("\n💡 Common issues:")
        print("   - Ensure Ollama has the nomic-embed-text model: ollama pull nomic-embed-text")
        print("   - Check Qdrant container is running: docker ps | grep qdrant")
        print("   - Verify network connectivity to localhost:6333")


if __name__ == "__main__":
    main()
