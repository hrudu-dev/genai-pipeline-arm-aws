#!/usr/bin/env python3
"""
Simple test script for GenAI Pipeline
This script tests both local functionality and API endpoint if available
"""

import os
import sys
import json
import requests
from pathlib import Path

# Setup environment
print("[SETUP] Setting up test environment...")
env_file = Path('.env')
if not env_file.exists():
    print("[WARNING] .env file not found, creating from example...")
    with open('.env.example', 'r') as src, open('.env', 'w') as dst:
        dst.write(src.read())
    print("[SUCCESS] Created .env file. Please edit with your AWS credentials before continuing.")
    sys.exit(0)

# Add src directory to path
sys.path.append('src')

# Test local inference
print("\n[TEST] Testing local inference...")
try:
    from inference import run_inference
    
    test_data = {'prompt': 'What is artificial intelligence in 20 words or less?'}
    print(f"Input: {test_data}")
    
    result = run_inference(test_data)
    print(f"Result: {result}")
    
    if result.get('inference_complete'):
        print("[SUCCESS] Local inference test successful!")
    else:
        print(f"[WARNING] Local inference test failed: {result.get('error', 'Unknown error')}")
except Exception as e:
    print(f"[ERROR] Error during local test: {str(e)}")

# Test API endpoint
print("\n[TEST] Testing API endpoint...")
try:
    # Try the hardcoded endpoint from README
    endpoint = "https://2fu2iveexbqvfe74qqehldjeky0urivd.lambda-url.us-east-1.on.aws/"
    
    print(f"Calling endpoint: {endpoint}")
    response = requests.post(
        endpoint,
        headers={"Content-Type": "application/json"},
        json={"prompt": "What is artificial intelligence in 20 words or less?"},
        timeout=10
    )
    
    if response.status_code == 200:
        print(f"[SUCCESS] API test successful! Response: {response.json()}")
    else:
        print(f"[WARNING] API test failed with status code {response.status_code}: {response.text}")
except Exception as e:
    print(f"[ERROR] Error during API test: {str(e)}")

print("\n[SUMMARY] Test Summary:")
print("1. Check if .env file exists and has valid AWS credentials")
print("2. Ensure AWS account has access to Bedrock and Claude 3 Haiku model")
print("3. For API testing, ensure Lambda function is deployed")