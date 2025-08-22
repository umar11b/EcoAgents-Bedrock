#!/usr/bin/env python3
"""
Test script for EcoAgents
Tests both the simple agent and Bedrock agent (if available)
"""

from agent import EcoAgent
from bedrock_agent import BedrockEcoAgent

def test_simple_agent():
    """Test the simple keyword-based agent."""
    print("=== Testing Simple Agent ===")
    agent = EcoAgent()
    
    test_cases = [
        "What is the air quality in Toronto?",
        "How much CO2 for a trip from Toronto to Vancouver?",
        "Are there any wildfire alerts in BC?",
        "Hello, how are you?"
    ]
    
    for test_case in test_cases:
        print(f"\nQ: {test_case}")
        response = agent.chat(test_case)
        print(f"A: {response}")

def test_bedrock_agent():
    """Test the Bedrock-powered agent."""
    print("\n=== Testing Bedrock Agent ===")
    try:
        agent = BedrockEcoAgent()
        
        test_cases = [
            "What is the air quality in Toronto?",
            "How much CO2 for a trip from Toronto to Vancouver?",
            "Are there any wildfire alerts in BC?",
            "Hello, how are you?"
        ]
        
        for test_case in test_cases:
            print(f"\nQ: {test_case}")
            response = agent.chat(test_case)
            print(f"A: {response}")
            
    except Exception as e:
        print(f"Bedrock agent not available: {e}")
        print("Make sure AWS Bedrock is set up and credentials are configured.")

if __name__ == "__main__":
    test_simple_agent()
    test_bedrock_agent()
