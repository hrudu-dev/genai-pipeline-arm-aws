#!/usr/bin/env python3
"""
Interactive CLI for testing the GenAI Pipeline API
"""

import requests
import json
import sys
import os
import time

# Function URL from deployment
FUNCTION_URL = "https://btjml6cwvtetuz4mraonqwyqbq0aeotc.lambda-url.us-east-1.on.aws/"

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the header"""
    print("=" * 80)
    print("GenAI Pipeline Interactive CLI".center(80))
    print("=" * 80)
    print("Type 'exit' to quit\n")

def call_api(prompt):
    """Call the API with a prompt"""
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt
    }
    
    try:
        print("Sending request to API...")
        response = requests.post(FUNCTION_URL, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('inference_complete'):
                return result.get('result')
            else:
                return f"Error: {result.get('error', 'Unknown error')}"
        else:
            return f"Error: HTTP {response.status_code}\n{response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main function"""
    clear_screen()
    print_header()
    
    while True:
        # Get prompt from user
        prompt = input("Enter your prompt (or 'exit' to quit): ")
        
        if prompt.lower() == 'exit':
            print("\nGoodbye!")
            break
        
        if not prompt.strip():
            print("Please enter a prompt")
            continue
        
        # Call API
        print("\nCalling API...\n")
        start_time = time.time()
        result = call_api(prompt)
        end_time = time.time()
        
        # Print result
        print("\n" + "=" * 80)
        print(f"Response (took {end_time - start_time:.2f} seconds):")
        print("=" * 80)
        print(result)
        print("=" * 80 + "\n")

if __name__ == "__main__":
    main()