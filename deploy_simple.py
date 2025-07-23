#!/usr/bin/env python3
"""
Simple deployment script for GenAI Pipeline Lambda function
"""

import os
import json
import boto3
import zipfile
import dotenv
import sys
import argparse

# Load environment variables from .env file
dotenv.load_dotenv()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Deploy Lambda function')
    parser.add_argument('--function', type=str, default='lambda_function.py',
                        help='Lambda function file to deploy')
    return parser.parse_args()

def create_zip_package(function_file='lambda_function.py'):
    """Create a simple zip package with just the Lambda function"""
    print(f"Creating Lambda package from {function_file}...")
    
    # Check if function file exists
    if not os.path.exists(function_file):
        print(f"Error: Function file {function_file} not found")
        sys.exit(1)
    
    # Create zip file
    zip_path = "simple_function.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add the function file as lambda_function.py (the entry point)
        zipf.write(function_file, arcname="lambda_function.py")
    
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
    
    # Print debug info (without secrets)
    print(f"AWS Region: {aws_region}")
    print(f"Lambda Role ARN is set: {'Yes' if role_arn else 'No'}")
    
    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not found in environment variables. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
    
    if not role_arn:
        raise ValueError("Lambda role ARN not found in environment variables. Please set LAMBDA_ROLE_ARN.")
    
    # Create Lambda client
    try:
        lambda_client = boto3.client('lambda',
                                   region_name=aws_region,
                                   aws_access_key_id=aws_access_key,
                                   aws_secret_access_key=aws_secret_key)
        
        # Test connection
        lambda_client.list_functions(MaxItems=1)
        print("AWS Lambda connection successful")
    except Exception as e:
        print(f"Error connecting to AWS Lambda: {str(e)}")
        sys.exit(1)
    
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
        
        try:
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
        except Exception as e:
            print(f"Error creating Lambda function: {str(e)}")
            sys.exit(1)
    except Exception as e:
        print(f"Error checking Lambda function: {str(e)}")
        sys.exit(1)
    
    # Create or update function URL
    try:
        url_config = lambda_client.get_function_url_config(FunctionName=function_name)
        print(f"Function URL already exists: {url_config['FunctionUrl']}")
    except lambda_client.exceptions.ResourceNotFoundException:
        print("Creating function URL...")
        try:
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
        except Exception as e:
            print(f"Error creating function URL: {str(e)}")
            sys.exit(1)
    except Exception as e:
        print(f"Error checking function URL: {str(e)}")
        sys.exit(1)
    
    # Save function URL to file for GitHub Actions
    try:
        with open("function_url.txt", "w") as f:
            f.write(url_config['FunctionUrl'])
    except Exception as e:
        print(f"Warning: Could not save function URL to file: {str(e)}")
    
    return url_config['FunctionUrl']

def main():
    """Main function"""
    print("GenAI Pipeline Simple Lambda Deployment\n")
    
    # Parse command line arguments
    args = parse_args()
    
    # Create Lambda package
    package_path = create_zip_package(args.function)
    
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
        sys.exit(1)

if __name__ == "__main__":
    main()