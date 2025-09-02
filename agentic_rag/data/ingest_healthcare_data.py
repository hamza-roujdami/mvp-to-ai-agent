"""
Healthcare Data Ingestion Script for HealthAI Nexus
Ingests sample healthcare documents into Azure AI Search index
"""

import os
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class HealthcareDataIngestion:
    """Handles ingestion of healthcare documents into Azure AI Search."""
    
    def __init__(self):
        """Initialize the data ingestion."""
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
        
        self.search_client = SearchClient(
            endpoint=self.search_endpoint,
            index_name=self.index_name,
            credential=self.credential
        )

    def get_sample_healthcare_documents(self) -> List[Dict[str, Any]]:
        """
        Get sample healthcare documents for ingestion.
        
        Returns:
            List[Dict[str, Any]]: List of healthcare documents
        """
        documents = [
            {
                "id": str(uuid.uuid4()),
                "title": "Diabetes Management and Treatment Guidelines",
                "content": """
                Diabetes is a chronic condition that affects how your body processes blood sugar (glucose). 
                There are two main types: Type 1 diabetes, where the body doesn't produce insulin, and 
                Type 2 diabetes, where the body doesn't use insulin effectively.
                
                Common symptoms include frequent urination, excessive thirst, unexplained weight loss, 
                fatigue, blurred vision, and slow-healing sores. Early detection and proper management 
                are crucial for preventing complications.
                
                Treatment typically involves lifestyle changes, blood sugar monitoring, and medications 
                such as metformin, insulin therapy, or other glucose-lowering drugs. Regular exercise, 
                a balanced diet, and maintaining a healthy weight are essential components of diabetes care.
                
                Complications can include heart disease, stroke, kidney disease, nerve damage, and 
                eye problems. Regular check-ups with healthcare providers are important for monitoring 
                and preventing these complications.
                """,
                "summary": "Comprehensive guide to diabetes types, symptoms, treatment options, and management strategies.",
                "category": "Endocrinology",
                "source": "Medical Guidelines Database",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "relevance_score": 0.95,
                "tags": ["diabetes", "blood sugar", "insulin", "chronic condition", "treatment"],
                "medical_terms": ["glucose", "metformin", "insulin therapy", "hyperglycemia", "hypoglycemia"]
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Heart Disease Prevention and Risk Factors",
                "content": """
                Heart disease, also known as cardiovascular disease, is the leading cause of death 
                worldwide. It encompasses various conditions affecting the heart and blood vessels, 
                including coronary artery disease, heart attacks, and heart failure.
                
                Major risk factors include high blood pressure, high cholesterol, smoking, diabetes, 
                obesity, physical inactivity, and family history. Age and gender also play significant 
                roles in heart disease risk.
                
                Prevention strategies include maintaining a healthy diet rich in fruits, vegetables, 
                and whole grains, regular physical activity, avoiding tobacco use, managing stress, 
                and controlling blood pressure and cholesterol levels.
                
                Warning signs of a heart attack include chest pain or discomfort, shortness of breath, 
                nausea, lightheadedness, and pain in the arms, back, neck, or jaw. Immediate medical 
                attention is crucial if these symptoms occur.
                """,
                "summary": "Overview of heart disease risk factors, prevention strategies, and warning signs.",
                "category": "Cardiology",
                "source": "Cardiovascular Health Institute",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "relevance_score": 0.92,
                "tags": ["heart disease", "cardiovascular", "prevention", "risk factors", "heart attack"],
                "medical_terms": ["coronary artery disease", "hypertension", "cholesterol", "myocardial infarction"]
            },
            {
                "id": str(uuid.uuid4()),
                "title": "COVID-19 Vaccination Guidelines and Safety Information",
                "content": """
                COVID-19 vaccines have been developed and authorized for emergency use to help prevent 
                severe illness, hospitalization, and death from COVID-19. Multiple vaccine types are 
                available, including mRNA vaccines, viral vector vaccines, and protein subunit vaccines.
                
                Vaccination is recommended for all eligible individuals, with priority given to 
                healthcare workers, elderly populations, and those with underlying health conditions. 
                Booster doses are recommended for certain populations to maintain immunity.
                
                Common side effects include pain at the injection site, fatigue, headache, muscle pain, 
                chills, fever, and nausea. These side effects are typically mild and resolve within 
                a few days. Severe allergic reactions are rare but require immediate medical attention.
                
                The vaccines have undergone rigorous testing for safety and efficacy. They significantly 
                reduce the risk of severe COVID-19 and help prevent transmission of the virus to others.
                """,
                "summary": "Comprehensive information about COVID-19 vaccines, safety, efficacy, and vaccination guidelines.",
                "category": "Infectious Diseases",
                "source": "CDC and WHO Guidelines",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "relevance_score": 0.88,
                "tags": ["covid-19", "vaccination", "immunity", "public health", "pandemic"],
                "medical_terms": ["mRNA vaccine", "viral vector", "booster dose", "immunization", "antibodies"]
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Mental Health and Anxiety Management Strategies",
                "content": """
                Mental health is an essential component of overall well-being, affecting how we think, 
                feel, and act. Anxiety disorders are among the most common mental health conditions, 
                affecting millions of people worldwide.
                
                Symptoms of anxiety include excessive worry, restlessness, fatigue, difficulty 
                concentrating, irritability, muscle tension, and sleep disturbances. These symptoms 
                can significantly impact daily functioning and quality of life.
                
                Treatment options include psychotherapy (such as cognitive-behavioral therapy), 
                medications (like selective serotonin reuptake inhibitors), lifestyle modifications, 
                and stress management techniques. Early intervention is crucial for effective treatment.
                
                Self-care strategies include regular exercise, adequate sleep, healthy eating, 
                mindfulness practices, social connections, and avoiding excessive alcohol and caffeine. 
                Professional help should be sought when symptoms persist or interfere with daily life.
                """,
                "summary": "Guide to understanding anxiety, treatment options, and self-care strategies for mental health.",
                "category": "Mental Health",
                "source": "Mental Health Foundation",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "relevance_score": 0.90,
                "tags": ["mental health", "anxiety", "therapy", "wellness", "stress management"],
                "medical_terms": ["cognitive-behavioral therapy", "SSRI", "psychotherapy", "mindfulness"]
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Pregnancy Care and Prenatal Health Guidelines",
                "content": """
                Pregnancy is a transformative period that requires special attention to maternal and 
                fetal health. Proper prenatal care is essential for ensuring a healthy pregnancy and 
                delivery.
                
                Key aspects of prenatal care include regular check-ups with healthcare providers, 
                prenatal vitamins (especially folic acid), proper nutrition, regular exercise, 
                and avoiding harmful substances like alcohol, tobacco, and certain medications.
                
                Common pregnancy symptoms include nausea and vomiting (morning sickness), fatigue, 
                frequent urination, breast tenderness, and mood changes. While most symptoms are 
                normal, some may require medical attention.
                
                Important milestones include the first trimester screening, anatomy ultrasound, 
                glucose tolerance test, and group B strep testing. Regular monitoring helps identify 
                and manage potential complications early.
                
                Warning signs that require immediate medical attention include severe abdominal pain, 
                vaginal bleeding, severe headaches, vision changes, and decreased fetal movement.
                """,
                "summary": "Comprehensive guide to prenatal care, pregnancy health, and important milestones.",
                "category": "Obstetrics",
                "source": "American College of Obstetricians and Gynecologists",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "relevance_score": 0.93,
                "tags": ["pregnancy", "prenatal care", "maternal health", "fetal development", "obstetrics"],
                "medical_terms": ["prenatal vitamins", "folic acid", "ultrasound", "glucose tolerance test"]
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Blood Pressure Management and Hypertension Treatment",
                "content": """
                Hypertension, or high blood pressure, is a common condition that affects millions of 
                people worldwide. It's often called the "silent killer" because it typically has no 
                symptoms but can lead to serious health complications.
                
                Blood pressure is measured in millimeters of mercury (mmHg) and consists of two numbers: 
                systolic pressure (when the heart beats) and diastolic pressure (when the heart rests). 
                Normal blood pressure is less than 120/80 mmHg.
                
                Risk factors for hypertension include age, family history, obesity, physical inactivity, 
                excessive salt intake, alcohol consumption, and stress. Certain medical conditions like 
                diabetes and kidney disease also increase the risk.
                
                Treatment typically involves lifestyle modifications such as the DASH diet, regular 
                exercise, weight management, limiting alcohol and sodium intake, and stress reduction. 
                Medications may include ACE inhibitors, diuretics, beta-blockers, and calcium channel blockers.
                
                Regular monitoring and adherence to treatment plans are essential for preventing 
                complications such as heart disease, stroke, and kidney damage.
                """,
                "summary": "Comprehensive guide to understanding, preventing, and treating high blood pressure.",
                "category": "Cardiology",
                "source": "American Heart Association",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "relevance_score": 0.91,
                "tags": ["hypertension", "blood pressure", "cardiovascular health", "DASH diet", "medication"],
                "medical_terms": ["ACE inhibitors", "diuretics", "beta-blockers", "systolic", "diastolic"]
            }
        ]
        
        return documents

    def ingest_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """
        Ingest documents into the Azure AI Search index.
        
        Args:
            documents: List of documents to ingest
            
        Returns:
            bool: True if ingestion was successful, False otherwise
        """
        try:
            print(f"📥 Ingesting {len(documents)} healthcare documents into index '{self.index_name}'")
            
            # Upload documents in batches
            batch_size = 5
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                result = self.search_client.upload_documents(batch)
                
                # Check for any failures
                failed_docs = [doc for doc in result if not doc.succeeded]
                if failed_docs:
                    print(f"⚠️ {len(failed_docs)} documents failed to upload in batch {i//batch_size + 1}")
                    for doc in failed_docs:
                        print(f"   Error: {doc.error_message}")
                else:
                    print(f"✅ Batch {i//batch_size + 1}: {len(batch)} documents uploaded successfully")
            
            print(f"🎉 Document ingestion completed!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to ingest documents: {e}")
            return False

    def get_index_document_count(self) -> int:
        """
        Get the current document count in the index.
        
        Returns:
            int: Number of documents in the index
        """
        try:
            stats = self.search_client.get_document_count()
            return stats
        except Exception as e:
            print(f"❌ Failed to get document count: {e}")
            return 0

    def search_documents(self, query: str, top: int = 5) -> List[Dict]:
        """
        Search for documents in the index.
        
        Args:
            query: Search query
            top: Number of results to return
            
        Returns:
            List[Dict]: Search results
        """
        try:
            results = self.search_client.search(
                search_text=query,
                top=top,
                include_total_count=True
            )
            
            documents = []
            for result in results:
                documents.append({
                    "title": result.get("title", ""),
                    "summary": result.get("summary", ""),
                    "category": result.get("category", ""),
                    "relevance_score": result.get("@search.score", 0)
                })
            
            return documents
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []


def main():
    """Main function to ingest healthcare data."""
    print("🚀 Ingesting Healthcare Data into Azure AI Search")
    print("=" * 60)
    
    try:
        # Initialize the ingestion
        ingestion = HealthcareDataIngestion()
        
        # Check current document count
        current_count = ingestion.get_index_document_count()
        print(f"📊 Current documents in index: {current_count}")
        
        # Get sample documents
        documents = ingestion.get_sample_healthcare_documents()
        print(f"📋 Prepared {len(documents)} healthcare documents for ingestion")
        
        # Ingest documents
        success = ingestion.ingest_documents(documents)
        
        if success:
            # Verify ingestion
            new_count = ingestion.get_index_document_count()
            print(f"📊 Documents after ingestion: {new_count}")
            print(f"✅ Successfully added {new_count - current_count} documents")
            
            # Test search functionality
            print("\n🔍 Testing search functionality...")
            test_queries = [
                "diabetes symptoms",
                "heart disease prevention",
                "covid-19 vaccination",
                "mental health anxiety",
                "pregnancy care"
            ]
            
            for query in test_queries:
                results = ingestion.search_documents(query, top=2)
                print(f"   Query: '{query}' -> {len(results)} results")
                if results:
                    print(f"      Top result: {results[0]['title']}")
        
        print("\n🎉 Healthcare data ingestion completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
