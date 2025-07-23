#!/usr/bin/env python3
"""Local test script for GenAI Pipeline"""

import os
import sys
import json
import dotenv
sys.path.append('src')

# Load environment variables from .env file
dotenv.load_dotenv()

import boto3

def run_inference(data):
    """Run GenAI model inference using credentials from environment variables."""
    try:
        # Get credentials from environment variables
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
        
        if not aws_access_key or not aws_secret_key:
            raise ValueError("AWS credentials not found in environment variables. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
        
        bedrock = boto3.client('bedrock-runtime',
                              region_name=aws_region,
                              aws_access_key_id=aws_access_key,
                              aws_secret_access_key=aws_secret_key)
        
        # Prepare prompt
        prompt = data.get('prompt', 'Hello, how can I help you?')
        
        # Call Bedrock model with correct indentation
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',  # Use this exact ID
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 500,
                'messages': [{'role': 'user', 'content': prompt}]
            })
        )
        
        response_body = json.loads(response.get('body').read())
        return {
            'inference_complete': True,
            'result': response_body['content'][0]['text'],
            'data': data
        }
    except Exception as e:
        return {
            'inference_complete': False,
            'error': str(e),
            'data': data
        }

def test_inference():
    """Test inference function locally"""
    test_data = {'prompt': 'What is artificial intelligence?'}
    
    print("[TEST] Testing GenAI Pipeline locally...")
    print(f"Input: {test_data}")
    
    # Use the function with credentials from environment variables
    result = run_inference(test_data)
    print(f"Result: {result}")
    
    if result.get('inference_complete'):
        print("[SUCCESS] Inference successful!")
    else:
        print(f"[WARNING] Inference failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_inference()