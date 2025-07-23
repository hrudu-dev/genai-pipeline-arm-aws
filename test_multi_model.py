#!/usr/bin/env python3
"""
Test multi-model support
"""

import requests
import json
import argparse
import time

# API endpoint URL
API_URL = "https://cr7c7lxj5mt2lwvyi57s2o6arq0paars.lambda-url.us-east-1.on.aws/"

def test_model(prompt, model_name):
    """Test a specific model"""
    print(f"Testing model: {model_name}")
    print(f"Prompt: {prompt}")
    
    # Prepare request
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": model_name
    }
    
    # Send request
    print("Sending request...")
    start_time = time.time()
    response = requests.post(API_URL, headers=headers, json=data)
    end_time = time.time()
    
    # Print response
    print(f"Status code: {response.status_code}")
    print(f"Response time: {end_time - start_time:.2f} seconds")
    
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("inference_complete"):
            print("\nResponse:")
            print("-" * 80)
            print(response_json["result"])
            print("-" * 80)
            print(f"Model: {response_json.get('model', 'unknown')}")
            print(f"Model ID: {response_json.get('model_id', 'unknown')}")
        else:
            print(f"Error: {response_json.get('error', 'Unknown error')}")
    else:
        print(f"Error: {response.text}")

def compare_models(prompt, models=None):
    """Compare multiple models"""
    if models is None:
        models = ['claude-haiku', 'claude-sonnet', 'titan-text', 'llama3']
    
    print(f"Comparing {len(models)} models")
    print(f"Prompt: {prompt}")
    
    results = {}
    
    for model_name in models:
        print(f"\nTesting model: {model_name}")
        
        # Prepare request
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "model": model_name
        }
        
        # Send request
        print("Sending request...")
        start_time = time.time()
        response = requests.post(API_URL, headers=headers, json=data)
        end_time = time.time()
        
        # Process response
        response_time = end_time - start_time
        print(f"Response time: {response_time:.2f} seconds")
        
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("inference_complete"):
                results[model_name] = {
                    'result': response_json["result"],
                    'response_time': response_time,
                    'model_id': response_json.get('model_id', 'unknown')
                }
                print(f"Success: Response received ({len(response_json['result'])} characters)")
            else:
                print(f"Error: {response_json.get('error', 'Unknown error')}")
        else:
            print(f"Error: {response.text}")
    
    # Print comparison
    print("\nModel Comparison:")
    print("-" * 80)
    print(f"{'Model':<15} {'Response Time':<15} {'Response Length':<20} {'Model ID'}")
    print("-" * 80)
    
    for model_name, result in results.items():
        print(f"{model_name:<15} {result['response_time']:.2f}s {len(result['result']):<20} {result['model_id']}")
    
    # Save results to file
    with open('model_comparison.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to model_comparison.json")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Test multi-model support')
    parser.add_argument('--prompt', '-p', default='Explain the benefits of ARM64 architecture in cloud computing', help='Prompt to send to the API')
    parser.add_argument('--model', '-m', help='Model to test (omit to compare all models)')
    parser.add_argument('--compare', '-c', action='store_true', help='Compare multiple models')
    
    args = parser.parse_args()
    
    if args.compare or args.model is None:
        compare_models(args.prompt)
    else:
        test_model(args.prompt, args.model)

if __name__ == "__main__":
    main()