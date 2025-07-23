#!/usr/bin/env python3
"""
Create IAM role for Lambda function
"""

import json
import boto3
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

def create_lambda_role():
    """Create IAM role for Lambda function"""
    print("Creating IAM role for Lambda function...")
    
    # Get credentials from environment variables
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    
    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not found in environment variables. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
    
    # Create IAM client
    iam_client = boto3.client('iam',
                            region_name=aws_region,
                            aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_key)
    
    role_name = "lambda-bedrock-role"
    
    # Check if role exists
    try:
        role = iam_client.get_role(RoleName=role_name)
        print(f"Role {role_name} already exists: {role['Role']['Arn']}")
        return role['Role']['Arn']
    except iam_client.exceptions.NoSuchEntityException:
        print(f"Role {role_name} does not exist")
    
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
    try:
        role = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Role for Lambda function to access Bedrock"
        )
        
        print(f"Created role: {role['Role']['Arn']}")
        
        # Attach Lambda basic execution policy
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
        )
        
        print("Attached AWSLambdaBasicExecutionRole policy")
        
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
        
        print("Attached Bedrock access policy")
        
        return role['Role']['Arn']
    except Exception as e:
        print(f"Error creating role: {str(e)}")
        
        # List existing roles
        print("\nListing existing roles:")
        response = iam_client.list_roles(MaxItems=10)
        for role in response['Roles']:
            print(f"- {role['RoleName']}: {role['Arn']}")
        
        print("\nTo create a role, you need iam:CreateRole permission.")
        print("Please create the role manually in the AWS Console:")
        print("1. Go to IAM > Roles > Create role")
        print("2. Select 'AWS service' and 'Lambda'")
        print("3. Click 'Next: Permissions'")
        print("4. Attach the 'AWSLambdaBasicExecutionRole' policy")
        print("5. Click 'Next: Tags'")
        print("6. Click 'Next: Review'")
        print("7. Name the role 'lambda-bedrock-role'")
        print("8. Click 'Create role'")
        print("9. Go to the role and add an inline policy for Bedrock access:")
        
        print(json.dumps(bedrock_policy, indent=2))
        
        return None

if __name__ == "__main__":
    role_arn = create_lambda_role()
    if role_arn:
        print(f"\nRole ARN: {role_arn}")
        print("Add this to your .env file as LAMBDA_ROLE_ARN={role_arn}")