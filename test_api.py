#!/usr/bin/env python3
"""
Test the GenAI Pipeline API directly
"""

import requests
import json
import argparse

# API endpoint URL
API_URL = "https://cr7c7lxj5mt2lwvyi57s2o6arq0paars.lambda-url.us-east-1.on.aws/"

def test_api(prompt):
    """Test the API with a prompt"""
    print(f"Testing API with prompt: {prompt}")
    
    # Prepare request
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt
    }
    
    # Send request
    print("Sending request...")
    response = requests.post(API_URL, headers=headers, json=data)
    
    # Print response
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("inference_complete"):
            print("\nResponse:")
            print("-" * 80)
            print(response_json["result"])
            print("-" * 80)
        else:
            print(f"Error: {response_json.get('error', 'Unknown error')}")
    else:
        print(f"Error: {response.text}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Test the GenAI Pipeline API")
    parser.add_argument("prompt", nargs="?", default="What is artificial intelligence?", help="Prompt to send to the API")
    
    args = parser.parse_args()
    
    test_api(args.prompt)

if __name__ == "__main__":
    main()