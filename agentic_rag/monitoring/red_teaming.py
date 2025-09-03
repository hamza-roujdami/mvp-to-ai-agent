#!/usr/bin/env python3
"""
Azure AI Red Teaming for Healthcare Agents
Provides security testing and safety validation for healthcare AI systems
"""

import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    RedTeam,
    AzureOpenAIModelConfiguration,
    AttackStrategy,
    RiskCategory,
)

# Load environment variables
load_dotenv()

class HealthcareRedTeam:
    """Red teaming for healthcare agents to ensure safety and compliance"""
    
    def __init__(self, project_client: AIProjectClient):
        self.project_client = project_client
        self.healthcare_risk_categories = [
            RiskCategory.VIOLENCE,
            # Add more healthcare-specific categories as they become available
        ]
        self.healthcare_attack_strategies = [
            AttackStrategy.BASE64,
            AttackStrategy.FLIP,
            # Add more strategies as needed
        ]
    
    def create_red_team_scan(
        self, 
        model_deployment_name: str,
        display_name: str = "healthcare-red-team-scan",
        num_turns: int = 3,
        risk_categories: Optional[List[RiskCategory]] = None,
        attack_strategies: Optional[List[AttackStrategy]] = None
    ) -> Dict[str, Any]:
        """
        Create a red teaming scan for healthcare agents
        
        Args:
            model_deployment_name: The model deployment to test
            display_name: Display name for the scan
            num_turns: Number of conversation turns
            risk_categories: Risk categories to test (defaults to healthcare-specific)
            attack_strategies: Attack strategies to use (defaults to healthcare-specific)
            
        Returns:
            Dict containing scan results
        """
        try:
            # Use healthcare-specific defaults if not provided
            if risk_categories is None:
                risk_categories = self.healthcare_risk_categories
            if attack_strategies is None:
                attack_strategies = self.healthcare_attack_strategies
            
            # Create target configuration
            target_config = AzureOpenAIModelConfiguration(
                model_deployment_name=model_deployment_name
            )
            
            # Create red team agent
            red_team_agent = RedTeam(
                attack_strategies=attack_strategies,
                risk_categories=risk_categories,
                display_name=display_name,
                target=target_config,
            )
            
            # Get model configuration
            model_endpoint = os.getenv("MODEL_ENDPOINT")
            model_api_key = os.getenv("MODEL_API_KEY")
            
            if not model_endpoint or not model_api_key:
                print("⚠️ Model endpoint or API key not found in environment variables")
                return {"error": "Missing model configuration"}
            
            # Create headers for authentication
            headers = {
                "model-endpoint": model_endpoint,
                "api-key": model_api_key
            }
            
            # Create and run the red teaming scan
            print(f"🔍 Starting red team scan: {display_name}")
            print(f"   🎯 Target: {model_deployment_name}")
            print(f"   ⚠️ Risk Categories: {[cat.value for cat in risk_categories]}")
            print(f"   🛡️ Attack Strategies: {[strategy.value for strategy in attack_strategies]}")
            
            red_team_response = self.project_client.red_teams.create(
                red_team=red_team_agent, 
                headers=headers
            )
            
            print(f"✅ Red team scan created successfully")
            print(f"   📋 Scan ID: {red_team_response.name}")
            print(f"   📊 Status: {red_team_response.status}")
            
            return {
                "success": True,
                "scan_id": red_team_response.name,
                "status": red_team_response.status,
                "display_name": display_name,
                "target": model_deployment_name
            }
            
        except Exception as e:
            print(f"❌ Red team scan failed: {e}")
            return {"error": str(e)}
    
    def get_red_team_scan(self, scan_id: str) -> Dict[str, Any]:
        """
        Get the status and results of a red team scan
        
        Args:
            scan_id: The scan ID to retrieve
            
        Returns:
            Dict containing scan status and results
        """
        try:
            scan = self.project_client.red_teams.get(name=scan_id)
            
            print(f"📊 Red Team Scan Status: {scan.status}")
            print(f"   📋 Scan ID: {scan.name}")
            print(f"   🏷️ Display Name: {scan.display_name}")
            
            return {
                "success": True,
                "scan_id": scan.name,
                "status": scan.status,
                "display_name": scan.display_name,
                "created_at": getattr(scan, 'created_at', None),
                "updated_at": getattr(scan, 'updated_at', None)
            }
            
        except Exception as e:
            print(f"❌ Failed to get red team scan: {e}")
            return {"error": str(e)}
    
    def list_red_team_scans(self) -> List[Dict[str, Any]]:
        """
        List all red team scans
        
        Returns:
            List of scan information
        """
        try:
            scans = []
            for scan in self.project_client.red_teams.list():
                scan_info = {
                    "scan_id": scan.name,
                    "status": scan.status,
                    "display_name": scan.display_name,
                    "created_at": getattr(scan, 'created_at', None),
                    "updated_at": getattr(scan, 'updated_at', None)
                }
                scans.append(scan_info)
                print(f"📋 Found scan: {scan.display_name}, Status: {scan.status}")
            
            return scans
            
        except Exception as e:
            print(f"❌ Failed to list red team scans: {e}")
            return []
    
    def run_healthcare_safety_test(self, model_deployment_name: str) -> Dict[str, Any]:
        """
        Run a comprehensive safety test for healthcare agents
        
        Args:
            model_deployment_name: The model deployment to test
            
        Returns:
            Dict containing test results
        """
        print("🏥 Starting Healthcare Safety Test...")
        
        # Create a healthcare-specific red team scan
        scan_result = self.create_red_team_scan(
            model_deployment_name=model_deployment_name,
            display_name="healthcare-safety-test",
            num_turns=5,
            risk_categories=self.healthcare_risk_categories,
            attack_strategies=self.healthcare_attack_strategies
        )
        
        if scan_result.get("success"):
            print("✅ Healthcare safety test initiated successfully")
            print("💡 Monitor the scan progress in Azure AI Foundry portal")
            print("🔍 Results will be available in the Red Teaming section")
        else:
            print("❌ Healthcare safety test failed")
        
        return scan_result

def create_healthcare_red_team(project_client: AIProjectClient) -> HealthcareRedTeam:
    """Create a healthcare red team instance"""
    return HealthcareRedTeam(project_client)

def run_healthcare_red_team_scan(
    project_client: AIProjectClient,
    model_deployment_name: str,
    display_name: str = "healthcare-red-team-scan"
) -> Dict[str, Any]:
    """
    Quick function to run a healthcare red team scan
    
    Args:
        project_client: Azure AI Project client
        model_deployment_name: Model deployment to test
        display_name: Display name for the scan
        
    Returns:
        Dict containing scan results
    """
    red_team = create_healthcare_red_team(project_client)
    return red_team.run_healthcare_safety_test(model_deployment_name)
