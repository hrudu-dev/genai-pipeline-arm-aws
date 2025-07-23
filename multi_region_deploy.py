#!/usr/bin/env python3
"""
Multi-region deployment for GenAI Pipeline
"""

import os
import json
import boto3
import zipfile
import tempfile
import shutil
from pathlib import Path
import concurrent.futures
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Regions to deploy to
REGIONS = [
    "us-east-1",
    "us-west-2",
    "eu-west-1"
]

# Lambda function name
LAMBDA_FUNCTION_NAME = "GenAIPipelineMultiRegion"

# Role name (must exist in each region)
ROLE_NAME = "lambda-execution-role"

def create_zip_package():
    """Create a simple zip package with just the Lambda function"""
    print("Creating Lambda package...")
    
    # Create zip file
    zip_path = "multi_region_function.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("lambda_function.py")
    
    print(f"Created Lambda package: {zip_path}")
    return zip_path

def deploy_to_region(region, package_path):
    """Deploy Lambda function to a specific region"""
    print(f"Deploying to region: {region}")
    
    try:
        # Get credentials from environment variables
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        
        if not aws_access_key or not aws_secret_key:
            raise ValueError("AWS credentials not found in environment variables. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
        
        # Create Lambda client for the region
        lambda_client = boto3.client('lambda',
                                   region_name=region,
                                   aws_access_key_id=aws_access_key,
                                   aws_secret_access_key=aws_secret_key)
        
        # Create IAM client for the region
        iam_client = boto3.client('iam',
                                region_name=region,
                                aws_access_key_id=aws_access_key,
                                aws_secret_access_key=aws_secret_key)
        
        # Get role ARN
        try:
            role = iam_client.get_role(RoleName=ROLE_NAME)
            role_arn = role['Role']['Arn']
        except Exception as e:
            print(f"Error getting role in {region}: {str(e)}")
            return None
        
        # Check if function exists
        try:
            lambda_client.get_function(FunctionName=LAMBDA_FUNCTION_NAME)
            print(f"Function {LAMBDA_FUNCTION_NAME} already exists in {region}, updating...")
            
            # Update function code
            with open(package_path, 'rb') as f:
                lambda_client.update_function_code(
                    FunctionName=LAMBDA_FUNCTION_NAME,
                    ZipFile=f.read()
                )
        except lambda_client.exceptions.ResourceNotFoundException:
            print(f"Function {LAMBDA_FUNCTION_NAME} does not exist in {region}, creating...")
            
            # Create function
            with open(package_path, 'rb') as f:
                response = lambda_client.create_function(
                    FunctionName=LAMBDA_FUNCTION_NAME,
                    Runtime='python3.9',
                    Role=role_arn,
                    Handler='lambda_function.lambda_handler',
                    Code={'ZipFile': f.read()},
                    Timeout=30,
                    MemorySize=256,
                    Architectures=['arm64']
                )
        
        # Create or update function URL
        try:
            url_config = lambda_client.get_function_url_config(FunctionName=LAMBDA_FUNCTION_NAME)
            print(f"Function URL already exists in {region}: {url_config['FunctionUrl']}")
            function_url = url_config['FunctionUrl']
        except lambda_client.exceptions.ResourceNotFoundException:
            print(f"Creating function URL in {region}...")
            url_config = lambda_client.create_function_url_config(
                FunctionName=LAMBDA_FUNCTION_NAME,
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
                FunctionName=LAMBDA_FUNCTION_NAME,
                StatementId='FunctionURLAllowPublicAccess',
                Action='lambda:InvokeFunctionUrl',
                Principal='*',
                FunctionUrlAuthType='NONE'
            )
            
            function_url = url_config['FunctionUrl']
            print(f"Created function URL in {region}: {function_url}")
        
        return {
            'region': region,
            'function_arn': f"arn:aws:lambda:{region}:{role_arn.split(':')[4]}:function:{LAMBDA_FUNCTION_NAME}",
            'function_url': function_url
        }
    except Exception as e:
        print(f"Error deploying to {region}: {str(e)}")
        return None

def deploy_multi_region():
    """Deploy Lambda function to multiple regions"""
    print(f"Deploying to {len(REGIONS)} regions...")
    
    # Create Lambda package
    package_path = create_zip_package()
    
    # Deploy to each region
    results = []
    for region in REGIONS:
        result = deploy_to_region(region, package_path)
        if result:
            results.append(result)
    
    # Write results to file
    with open('multi_region_deployment.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Deployment complete. Deployed to {len(results)}/{len(REGIONS)} regions.")
    print("Results written to multi_region_deployment.json")
    
    return results

if __name__ == "__main__":
    deploy_multi_region()