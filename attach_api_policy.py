#!/usr/bin/env python3
"""
Attach API Gateway policy to IAM user
"""

import boto3
import json

# Hardcoded credentials - only for testing
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

# IAM user name
USER_NAME = "arm"

def attach_policy():
    """Attach API Gateway policy to IAM user"""
    print(f"Attaching API Gateway policy to user: {USER_NAME}")
    
    # Create IAM client
    iam_client = boto3.client('iam',
                            region_name=AWS_DEFAULT_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Load policy document
    with open("iam/api-gateway-policy.json", "r") as f:
        policy_document = f.read()
    
    # Create policy
    try:
        policy_response = iam_client.create_policy(
            PolicyName="GenAIPipelineAPIGatewayPolicy",
            PolicyDocument=policy_document,
            Description="Policy for API Gateway access"
        )
        policy_arn = policy_response['Policy']['Arn']
        print(f"Created policy: {policy_arn}")
    except iam_client.exceptions.EntityAlreadyExistsException:
        # Get account ID
        sts_client = boto3.client('sts',
                                region_name=AWS_DEFAULT_REGION,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        account_id = sts_client.get_caller_identity()['Account']
        policy_arn = f"arn:aws:iam::{account_id}:policy/GenAIPipelineAPIGatewayPolicy"
        print(f"Policy already exists: {policy_arn}")
    except Exception as e:
        print(f"Error creating policy: {str(e)}")
        return False
    
    # Attach policy to user
    try:
        iam_client.attach_user_policy(
            UserName=USER_NAME,
            PolicyArn=policy_arn
        )
        print(f"Attached policy to user: {USER_NAME}")
        return True
    except Exception as e:
        print(f"Error attaching policy: {str(e)}")
        return False

if __name__ == "__main__":
    attach_policy()