#!/usr/bin/env python3
"""
Simple deployment script for GenAI Pipeline Lambda function
"""

import os
import json
import boto3
import zipfile
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

def create_zip_package():
    """Create a simple zip package with just the Lambda function"""
    print("Creating Lambda package...")
    
    # Create zip file
    zip_path = "simple_function.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("lambda_function.py")
    
    print(f"Created Lambda package: {zip_path}")
    return zip_path

def deploy_lambda(package_path):
    """Deploy Lambda function"""
    print("Deploying Lambda function...")
    
    # Get credentials from environment variables
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    role_arn = os.environ.get('LAMBDA_ROLE_ARN')
    
    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not found in environment variables. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
    
    if not role_arn:
        raise ValueError("Lambda role ARN not found in environment variables. Please set LAMBDA_ROLE_ARN.")
    
    # Create Lambda client
    lambda_client = boto3.client('lambda',
                               region_name=aws_region,
                               aws_access_key_id=aws_access_key,
                               aws_secret_access_key=aws_secret_key)
    
    function_name = "GenAIPipelineTest2"
    
    # Check if function exists
    try:
        lambda_client.get_function(FunctionName=function_name)
        print(f"Function {function_name} already exists, updating...")
        
        # Update function code
        with open(package_path, 'rb') as f:
            lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=f.read()
            )
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"Function {function_name} does not exist, creating...")
        
        # Create function
        with open(package_path, 'rb') as f:
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.9',
                Role=role_arn,
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': f.read()},
                Timeout=30,
                MemorySize=256,
                Architectures=['arm64']
            )
        
        print(f"Created function: {response['FunctionArn']}")
    
    # Create or update function URL
    try:
        url_config = lambda_client.get_function_url_config(FunctionName=function_name)
        print(f"Function URL already exists: {url_config['FunctionUrl']}")
    except lambda_client.exceptions.ResourceNotFoundException:
        print("Creating function URL...")
        url_config = lambda_client.create_function_url_config(
            FunctionName=function_name,
            AuthType='NONE',
            Cors={
                'AllowOrigins': ['*'],
                'AllowMethods': ['*'],
                'AllowHeaders': ['*'],
                'MaxAge': 86400
            }
        )
        
        # Add permission for function URL
        lambda_client.add_permission(
            FunctionName=function_name,
            StatementId='FunctionURLAllowPublicAccess',
            Action='lambda:InvokeFunctionUrl',
            Principal='*',
            FunctionUrlAuthType='NONE'
        )
        
        print(f"Created function URL: {url_config['FunctionUrl']}")
    
    return url_config['FunctionUrl']

def main():
    """Main function"""
    print("GenAI Pipeline Simple Lambda Deployment\n")
    
    # Create Lambda package
    package_path = create_zip_package()
    
    # Deploy Lambda function
    function_url = deploy_lambda(package_path)
    
    if function_url:
        print("\nDeployment complete!")
        print(f"Function URL: {function_url}")
        print("\nTest with:")
        print(f"curl -X POST \"{function_url}\" \\")
        print("  -H \"Content-Type: application/json\" \\")
        print("  -d '{\"prompt\": \"What is artificial intelligence?\"}'")
    else:
        print("\nDeployment failed!")

if __name__ == "__main__":
    main()