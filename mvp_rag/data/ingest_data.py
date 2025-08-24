#!/usr/bin/env python3
"""
Data ingestion script for the MVP RAG system.

This script populates the Qdrant vector database with
healthcare documents and their embeddings.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.llm_client import OllamaClient
from core.vector_store import QdrantVectorStore
from utils.logger import get_logger

logger = get_logger("data_ingestion")

def create_sample_documents():
    """Create sample healthcare documents for the MVP."""
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
    
    return documents

def main():
    """Main data ingestion function."""
    print("📚 Data Ingestion for MVP RAG System")
    print("=" * 50)
    
    # Initialize clients
    print("🔧 Initializing clients...")
    try:
        llm_client = OllamaClient()
        vector_store = QdrantVectorStore()
        print("✅ Clients initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize clients: {e}")
        return
    
    # Health checks
    print("\n🏥 Health Checks:")
    ollama_healthy = llm_client.health_check()
    qdrant_healthy = vector_store.health_check()
    
    print(f"   {'✅' if ollama_healthy else '❌'} Ollama: {'Healthy' if ollama_healthy else 'Unhealthy'}")
    print(f"   {'✅' if qdrant_healthy else '❌'} Qdrant: {'Healthy' if qdrant_healthy else 'Unhealthy'}")
    
    if not (ollama_healthy and qdrant_healthy):
        print("\n❌ Health checks failed. Please ensure services are running.")
        return
    
    # Create sample documents
    print("\n📝 Creating sample healthcare documents...")
    documents = create_sample_documents()
    print(f"✅ Created {len(documents)} sample documents")
    
    # Generate embeddings
    print("\n🧠 Generating embeddings...")
    embeddings = []
    embedding_model = "bge-m3"
    
    for i, doc in enumerate(documents):
        print(f"   Embedding document {i+1}/{len(documents)}: {doc['title']}")
        try:
            embedding = llm_client.embed(embedding_model, doc['content'])
            embeddings.append(embedding)
        except Exception as e:
            print(f"   ❌ Failed to embed document {i+1}: {e}")
            return
    
    print(f"✅ Generated {len(embeddings)} embeddings")
    
    # Store in vector database
    print("\n💾 Storing documents in vector database...")
    try:
        doc_ids = vector_store.add_documents(documents, embeddings)
        print(f"✅ Stored {len(doc_ids)} documents in vector database")
    except Exception as e:
        print(f"❌ Failed to store documents: {e}")
        return
    
    # Verify storage
    print("\n🔍 Verifying storage...")
    try:
        collection_info = vector_store.get_collection_info()
        print(f"✅ Collection info: {collection_info}")
    except Exception as e:
        print(f"⚠️  Could not verify collection info: {e}")
    
    print("\n🎉 Data ingestion completed successfully!")
    print(f"📊 Summary:")
    print(f"   Documents processed: {len(documents)}")
    print(f"   Embeddings generated: {len(embeddings)}")
    print(f"   Vector dimensions: {len(embeddings[0]) if embeddings else 'Unknown'}")
    print(f"   Collection: {vector_store.collection_name}")
    
    print("\n🚀 Ready to run the MVP RAG demo!")
    print("Run: python main.py")

if __name__ == "__main__":
    main()
