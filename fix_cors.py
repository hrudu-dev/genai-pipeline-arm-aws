#!/usr/bin/env python3
"""
Fix CORS configuration for Lambda Function URL
"""

import boto3
import json
import os
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def fix_cors():
    """Update CORS configuration"""
    load_env()
    lambda_client = boto3.client('lambda')
    function_name = 'GenAIPipelineTest'
    
    try:
        # Update CORS configuration
        response = lambda_client.update_function_url_config(
            FunctionName=function_name,
            Cors={
                'AllowCredentials': False,
                'AllowHeaders': ['*'],
                'AllowMethods': ['*'],
                'AllowOrigins': ['*'],
                'MaxAge': 86400
            }
        )
        
        print("CORS configuration updated successfully!")
        print(f"Function URL: {response['FunctionUrl']}")
        print(f"CORS: {json.dumps(response['Cors'], indent=2)}")
        
    except Exception as e:
        print(f"Error updating CORS: {e}")

if __name__ == "__main__":
    fix_cors()