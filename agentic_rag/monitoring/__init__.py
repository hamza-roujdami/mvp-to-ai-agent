"""
🔍 Azure AI Foundry Monitoring Package

This package provides comprehensive monitoring capabilities for Azure AI Foundry applications
following the official Microsoft documentation for Application Insights integration.
"""

from .setup_monitoring import (
    AzureAIFoundryMonitor,
    get_monitor,
    setup_monitoring,
    azure_monitor
)

__all__ = [
    "AzureAIFoundryMonitor",
    "get_monitor", 
    "setup_monitoring",
    "azure_monitor"
]
