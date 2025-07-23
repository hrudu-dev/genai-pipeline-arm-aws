#!/usr/bin/env python3
"""
Update IAM role with Bedrock permissions
"""

import json
import boto3

# Hardcoded credentials - only for testing
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

# Role ARN
ROLE_ARN = "arn:aws:iam::004909959584:role/AmazonBedrockLambdaExecutionRole-c96welgwfhk7xj-4ww5ti7q6jr7hj"
ROLE_NAME = ROLE_ARN.split("/")[-1]

def update_role():
    """Update IAM role with Bedrock permissions"""
    print(f"Updating IAM role: {ROLE_NAME}")
    
    # Create IAM client
    iam_client = boto3.client('iam',
                            region_name=AWS_DEFAULT_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Load policy document
    with open("bedrock-policy.json", "r") as f:
        policy_document = f.read()
    
    # Create or update inline policy
    try:
        iam_client.put_role_policy(
            RoleName=ROLE_NAME,
            PolicyName="bedrock-access",
            PolicyDocument=policy_document
        )
        print("Added Bedrock access policy to role")
    except Exception as e:
        print(f"Error updating role: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    update_role()