#!/usr/bin/env python3
"""
Check AWS connection and permissions
"""

import boto3
import json
from pathlib import Path

def load_env():
    """Load environment variables"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    import os
                    os.environ[key] = value

def check_aws_connection():
    """Check AWS connection"""
    print("Checking AWS Connection...")
    print("=" * 40)
    
    try:
        # Check basic AWS connection
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print(f"AWS Account ID: {identity['Account']}")
        print(f"User ARN: {identity['Arn']}")
        print("AWS Connection: SUCCESS")
        
        return identity['Account']
        
    except Exception as e:
        print(f"AWS Connection: FAILED - {str(e)}")
        return None

def check_bedrock_access():
    """Check Bedrock access"""
    print("\nChecking Bedrock Access...")
    print("=" * 40)
    
    try:
        bedrock = boto3.client('bedrock-runtime')
        
        # Try a simple test call
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hi"}]
            })
        )
        
        print("Bedrock Access: SUCCESS")
        return True
        
    except Exception as e:
        print(f"Bedrock Access: FAILED - {str(e)}")
        if "AccessDeniedException" in str(e):
            print("\nNeed to request Bedrock model access:")
            print("1. Go to AWS Console > Amazon Bedrock")
            print("2. Click 'Model access' in left menu")
            print("3. Click 'Request model access'")
            print("4. Select 'Anthropic Claude 3 Haiku'")
            print("5. Submit request")
        return False

def check_lambda_permissions():
    """Check Lambda permissions"""
    print("\nChecking Lambda Permissions...")
    print("=" * 40)
    
    try:
        lambda_client = boto3.client('lambda')
        
        # Try to list functions
        response = lambda_client.list_functions()
        print("Lambda List Functions: SUCCESS")
        
        # Check if our function exists
        functions = [f['FunctionName'] for f in response['Functions']]
        if 'GenAIPipelineTest' in functions:
            print("Existing Function Found: GenAIPipelineTest")
        else:
            print("No existing function found (will create new)")
        
        return True
        
    except Exception as e:
        print(f"Lambda Permissions: FAILED - {str(e)}")
        return False

def check_iam_role():
    """Check IAM role"""
    print("\nChecking IAM Role...")
    print("=" * 40)
    
    import os
    role_arn = os.environ.get('LAMBDA_ROLE_ARN', '')
    
    if 'YOUR_ACCOUNT_ID' in role_arn:
        print("IAM Role: NOT CONFIGURED")
        print("Need to update LAMBDA_ROLE_ARN in .env file")
        return False
    
    try:
        iam = boto3.client('iam')
        role_name = role_arn.split('/')[-1]
        
        # Check if role exists
        response = iam.get_role(RoleName=role_name)
        print(f"IAM Role Found: {role_name}")
        
        # Check role policies
        policies = iam.list_attached_role_policies(RoleName=role_name)
        inline_policies = iam.list_role_policies(RoleName=role_name)
        
        print(f"Attached Policies: {len(policies['AttachedPolicies'])}")
        print(f"Inline Policies: {len(inline_policies['PolicyNames'])}")
        
        return True
        
    except Exception as e:
        print(f"IAM Role Check: FAILED - {str(e)}")
        return False

def main():
    """Main check function"""
    print("AWS Connection & Permissions Check")
    print("=" * 50)
    
    # Load environment
    load_env()
    
    # Run checks
    account_id = check_aws_connection()
    if not account_id:
        return
    
    bedrock_ok = check_bedrock_access()
    lambda_ok = check_lambda_permissions()
    role_ok = check_iam_role()
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"AWS Connection: {'OK' if account_id else 'FAILED'}")
    print(f"Bedrock Access: {'OK' if bedrock_ok else 'FAILED'}")
    print(f"Lambda Permissions: {'OK' if lambda_ok else 'FAILED'}")
    print(f"IAM Role: {'OK' if role_ok else 'FAILED'}")
    
    if all([account_id, bedrock_ok, lambda_ok, role_ok]):
        print("\nAll checks passed! Ready to deploy.")
    else:
        print("\nSome checks failed. Fix issues before deploying.")
        
        if not role_ok:
            print(f"\nUpdate .env file with correct role ARN:")
            print(f"LAMBDA_ROLE_ARN=arn:aws:iam::{account_id}:role/lambda-bedrock-role")

if __name__ == "__main__":
    main()