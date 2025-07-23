#!/usr/bin/env python3
"""
Deploy Lambda function for GenAI Pipeline with hardcoded credentials
"""

import os
import sys
import json
import boto3
import zipfile
import tempfile
import shutil
from pathlib import Path

# Hardcoded credentials - only for testing
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def create_lambda_package():
    """Create Lambda deployment package"""
    print_header("Creating Lambda Package")
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary directory: {temp_dir}")
    
    try:
        # Copy source files
        src_dir = Path("src")
        for file in src_dir.glob("*.py"):
            shutil.copy(file, temp_dir)
            print(f"Copied {file} to package")
        
        # Install dependencies
        print("Installing dependencies...")
        os.system(f"pip install -r requirements.txt -t {temp_dir} --quiet")
        
        # Create zip file
        zip_path = "function.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"Created Lambda package: {zip_path}")
        return zip_path
    
    finally:
        # Clean up
        shutil.rmtree(temp_dir)
        print("Cleaned up temporary directory")

def deploy_lambda(package_path):
    """Deploy Lambda function"""
    print_header("Deploying Lambda Function")
    
    # Create Lambda client with hardcoded credentials
    lambda_client = boto3.client('lambda',
                               region_name=AWS_DEFAULT_REGION,
                               aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    function_name = "GenAIPipeline"
    
    # Check if function exists
    try:
        lambda_client.get_function(FunctionName=function_name)
        print(f"Function {function_name} already exists, updating...")
        
        # Update function code
        with open(package_path, 'rb') as f:
            lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=f.read(),
                Architectures=['arm64']
            )
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"Function {function_name} does not exist, creating...")
        
        # Get or create execution role
        iam_client = boto3.client('iam',
                                region_name=AWS_DEFAULT_REGION,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        
        role_name = "lambda-bedrock-role"
        try:
            role = iam_client.get_role(RoleName=role_name)
            role_arn = role['Role']['Arn']
            print(f"Using existing role: {role_arn}")
        except iam_client.exceptions.NoSuchEntityException:
            print(f"Creating role {role_name}...")
            
            # Create trust policy
            trust_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "lambda.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
            
            # Create role
            role = iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy)
            )
            role_arn = role['Role']['Arn']
            
            # Attach policies
            iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
            )
            
            # Create Bedrock policy
            bedrock_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "bedrock:InvokeModel"
                        ],
                        "Resource": "*"
                    }
                ]
            }
            
            # Attach Bedrock policy
            iam_client.put_role_policy(
                RoleName=role_name,
                PolicyName="bedrock-access",
                PolicyDocument=json.dumps(bedrock_policy)
            )
            
            print(f"Created role: {role_arn}")
            
            # Wait for role to propagate
            print("Waiting for role to propagate...")
            import time
            time.sleep(10)
        
        # Create function
        with open(package_path, 'rb') as f:
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.9',
                Role=role_arn,
                Handler='inference.lambda_handler',
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
                'AllowMethods': ['POST', 'OPTIONS'],
                'AllowHeaders': ['Content-Type'],
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
    print("GenAI Pipeline Lambda Deployment\n")
    
    # Create Lambda package
    package_path = create_lambda_package()
    
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