#!/usr/bin/env python3
"""
Single-click deployment for GenAI Pipeline
"""

import boto3
import json
import zipfile
import os
import time
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_vars = {}
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
                    os.environ[key] = value
    return env_vars

def create_deployment_package():
    """Create deployment ZIP package"""
    print("Creating deployment package...")
    
    zip_path = 'lambda_deployment.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add main Lambda function
        zipf.write('lambda_function.py')
        
        # Add src modules
        for py_file in Path('src').glob('*.py'):
            zipf.write(py_file, f'src/{py_file.name}')
    
    print(f"Package created: {zip_path}")
    return zip_path

def deploy_lambda(zip_path):
    """Deploy Lambda function"""
    print("Deploying Lambda function...")
    
    lambda_client = boto3.client('lambda')
    function_name = 'GenAIPipelineTest'
    
    # Read ZIP file
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    try:
        # Try to update existing function
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content
        )
        print(f"Updated existing function: {function_name}")
    except lambda_client.exceptions.ResourceNotFoundException:
        # Create new function
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.11',
            Role=os.environ.get('LAMBDA_ROLE_ARN', 'arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-bedrock-role'),
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_content},
            Architecture=['arm64'],
            Timeout=30,
            MemorySize=512,
            Environment={
                'Variables': {
                    'AWS_DEFAULT_REGION': os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
                }
            }
        )
        print(f"Created new function: {function_name}")
    
    # Create function URL
    try:
        url_response = lambda_client.create_function_url_config(
            FunctionName=function_name,
            AuthType='NONE',
            Cors={
                'AllowCredentials': False,
                'AllowHeaders': ['*'],
                'AllowMethods': ['*'],
                'AllowOrigins': ['*']
            }
        )
        function_url = url_response['FunctionUrl']
        print(f"Function URL: {function_url}")
    except lambda_client.exceptions.ResourceConflictException:
        # URL already exists, get it
        url_response = lambda_client.get_function_url_config(FunctionName=function_name)
        function_url = url_response['FunctionUrl']
        print(f"Existing Function URL: {function_url}")
    
    return function_url

def update_test_files(function_url):
    """Update test files with new function URL"""
    print("Updating test files...")
    
    files_to_update = [
        ('test_complete.py', 'API_URL = "'),
        ('test_web.html', "const API_URL = '")
    ]
    
    for filename, search_pattern in files_to_update:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find and replace URL
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if search_pattern in line:
                    if 'test_complete.py' in filename:
                        lines[i] = f'API_URL = "{function_url}"'
                    else:
                        lines[i] = f"        const API_URL = '{function_url}';"
                    break
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            print(f"Updated {filename}")

def main():
    """Main deployment function"""
    print("GenAI Pipeline - Single Click Deployment")
    print("=" * 50)
    
    # Load environment
    env_vars = load_env()
    if not env_vars.get('AWS_ACCESS_KEY_ID'):
        print("AWS credentials not found in .env file")
        return
    
    try:
        # Create package
        zip_path = create_deployment_package()
        
        # Deploy
        function_url = deploy_lambda(zip_path)
        
        # Update test files
        update_test_files(function_url)
        
        # Cleanup
        os.remove(zip_path)
        
        print("\n" + "=" * 50)
        print("Deployment Complete!")
        print(f"API URL: {function_url}")
        print("\nTest your deployment:")
        print("   python test_complete.py")
        print("   python test_web_server.py")
        print("=" * 50)
        
    except Exception as e:
        print(f"Deployment failed: {str(e)}")

if __name__ == "__main__":
    main()