#!/usr/bin/env python3
"""
Test script for the deployed GenAI Pipeline API
"""

import requests
import json
import sys
import argparse

# Default Function URL from deployment
DEFAULT_FUNCTION_URL = "https://btjml6cwvtetuz4mraonqwyqbq0aeotc.lambda-url.us-east-1.on.aws/"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Test the GenAI Pipeline API')
    parser.add_argument('prompt', nargs='?', default="What is artificial intelligence?",
                        help='Prompt to send to the API')
    parser.add_argument('--url', type=str, default=DEFAULT_FUNCTION_URL,
                        help='Function URL to test')
    return parser.parse_args()

def test_api(prompt, function_url):
    """Test the API with a prompt"""
    print(f"Testing API with prompt: '{prompt}'")
    print(f"Using URL: {function_url}")
    
    # Prepare request
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt
    }
    
    try:
        # Send request
        response = requests.post(function_url, headers=headers, json=data)
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            print("\nAPI Response:")
            print(f"Status: {'Success' if result.get('inference_complete') else 'Failed'}")
            print(f"\nResult:\n{result.get('result')}")
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    
    # Test the API
    success = test_api(args.prompt, args.url)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)