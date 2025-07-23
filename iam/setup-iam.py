#!/usr/bin/env python3
"""
IAM Setup Script for GenAI Pipeline
This script helps create the necessary IAM resources for testing
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def run_command(command):
    """Run a shell command and return the output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout

def create_lambda_role():
    """Create the Lambda execution role"""
    print_header("Creating Lambda Execution Role")
    
    # Check if role already exists
    check_role = run_command("aws iam get-role --role-name lambda-bedrock-role 2>&1")
    if check_role and "NoSuchEntity" not in check_role:
        print("Role 'lambda-bedrock-role' already exists.")
        return True
    
    # Create the role
    print("Creating role 'lambda-bedrock-role'...")
    create_role = run_command("aws iam create-role --role-name lambda-bedrock-role --assume-role-policy-document file://iam/lambda-trust-policy.json")
    if not create_role:
        return False
    
    # Attach the policy
    print("Attaching execution policy...")
    attach_policy = run_command("aws iam put-role-policy --role-name lambda-bedrock-role --policy-name lambda-bedrock-execution --policy-document file://iam/lambda-execution-role-policy.json")
    if not attach_policy:
        return False
    
    print("Lambda execution role created successfully.")
    return True

def create_test_policy():
    """Create the test policy"""
    print_header("Creating Test Policy")
    
    # Check if policy already exists
    check_policy = run_command("aws iam list-policies --query \"Policies[?PolicyName=='GenAIPipelineTestPolicy'].Arn\" --output text")
    if check_policy and check_policy.strip():
        print(f"Policy 'GenAIPipelineTestPolicy' already exists: {check_policy.strip()}")
        return check_policy.strip()
    
    # Create the policy
    print("Creating policy 'GenAIPipelineTestPolicy'...")
    create_policy = run_command("aws iam create-policy --policy-name GenAIPipelineTestPolicy --policy-document file://iam/genai-pipeline-test-policy.json")
    if not create_policy:
        return None
    
    # Get the policy ARN
    policy_data = json.loads(create_policy)
    policy_arn = policy_data['Policy']['Arn']
    
    print(f"Test policy created successfully: {policy_arn}")
    return policy_arn

def create_test_user(policy_arn):
    """Create a test user"""
    print_header("Creating Test User")
    
    # Check if user already exists
    check_user = run_command("aws iam get-user --user-name genai-pipeline-tester 2>&1")
    if check_user and "NoSuchEntity" not in check_user:
        print("User 'genai-pipeline-tester' already exists.")
        create_new_keys = input("Create new access keys? (y/n): ").strip().lower()
        if create_new_keys == 'y':
            create_access_keys()
        return True
    
    # Create the user
    print("Creating user 'genai-pipeline-tester'...")
    create_user = run_command("aws iam create-user --user-name genai-pipeline-tester")
    if not create_user:
        return False
    
    # Attach the policy
    print("Attaching test policy...")
    attach_policy = run_command(f"aws iam attach-user-policy --user-name genai-pipeline-tester --policy-arn {policy_arn}")
    if not attach_policy:
        return False
    
    # Create access keys
    create_access_keys()
    
    print("Test user created successfully.")
    return True

def create_access_keys():
    """Create access keys for the test user"""
    print("Creating access keys...")
    create_keys = run_command("aws iam create-access-key --user-name genai-pipeline-tester")
    if not create_keys:
        return False
    
    # Parse the access keys
    keys_data = json.loads(create_keys)
    access_key = keys_data['AccessKey']['AccessKeyId']
    secret_key = keys_data['AccessKey']['SecretAccessKey']
    
    # Update .env file
    env_file = Path('../.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace or add AWS credentials
        if 'AWS_ACCESS_KEY_ID' in content:
            content = content.replace('AWS_ACCESS_KEY_ID=your_access_key', f'AWS_ACCESS_KEY_ID={access_key}')
        else:
            content += f'\nAWS_ACCESS_KEY_ID={access_key}'
        
        if 'AWS_SECRET_ACCESS_KEY' in content:
            content = content.replace('AWS_SECRET_ACCESS_KEY=your_secret_key', f'AWS_SECRET_ACCESS_KEY={secret_key}')
        else:
            content += f'\nAWS_SECRET_ACCESS_KEY={secret_key}'
        
        with open(env_file, 'w') as f:
            f.write(content)
    
    print("\n===== IMPORTANT: SAVE THESE CREDENTIALS =====")
    print(f"Access Key ID: {access_key}")
    print(f"Secret Access Key: {secret_key}")
    print("===========================================")
    
    return True

def main():
    """Main function"""
    print("GenAI Pipeline IAM Setup\n")
    
    # Create Lambda role
    if not create_lambda_role():
        print("Failed to create Lambda role. Exiting.")
        return
    
    # Create test policy
    policy_arn = create_test_policy()
    if not policy_arn:
        print("Failed to create test policy. Exiting.")
        return
    
    # Create test user
    if not create_test_user(policy_arn):
        print("Failed to create test user. Exiting.")
        return
    
    print("\nIAM setup complete!")
    print("\nNext steps:")
    print("1. Make sure your AWS account has access to Amazon Bedrock")
    print("2. Run local tests: python test_local.py")
    print("3. Deploy Lambda: python setup.py")

if __name__ == "__main__":
    main()