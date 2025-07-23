#!/usr/bin/env python3
"""
Test script for the deployed GenAI Pipeline API
"""

import requests
import json
import sys

# Function URL from deployment
FUNCTION_URL = "https://btjml6cwvtetuz4mraonqwyqbq0aeotc.lambda-url.us-east-1.on.aws/"

def test_api(prompt):
    """Test the API with a prompt"""
    print(f"Testing API with prompt: '{prompt}'")
    
    # Prepare request
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt
    }
    
    # Send request
    response = requests.post(FUNCTION_URL, headers=headers, json=data)
    
    # Check response
    if response.status_code == 200:
        result = response.json()
        print("\nAPI Response:")
        print(f"Status: {'Success' if result.get('inference_complete') else 'Failed'}")
        print(f"\nResult:\n{result.get('result')}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Get prompt from command line or use default
    prompt = sys.argv[1] if len(sys.argv) > 1 else "What is artificial intelligence?"
    test_api(prompt)