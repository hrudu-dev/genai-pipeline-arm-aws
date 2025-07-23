#!/usr/bin/env python3
"""
Create IAM role for Lambda function
"""

import json
import boto3

# Hardcoded credentials - only for testing
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

def create_lambda_role():
    """Create IAM role for Lambda function"""
    print("Creating IAM role for Lambda function...")
    
    # Create IAM client
    iam_client = boto3.client('iam',
                            region_name=AWS_DEFAULT_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    role_name = "lambda-bedrock-role"
    
    # Check if role exists
    try:
        role = iam_client.get_role(RoleName=role_name)
        print(f"Role {role_name} already exists: {role['Role']['Arn']}")
        return role['Role']['Arn']
    except iam_client.exceptions.NoSuchEntityException:
        print(f"Role {role_name} does not exist")
    
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
    
    print(json.dumps(bedrock_policy, indent=2))
    
    return None

if __name__ == "__main__":
    create_lambda_role()