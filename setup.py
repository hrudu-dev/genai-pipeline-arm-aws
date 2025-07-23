#!/usr/bin/env python3
"""
Setup script for GenAI Pipeline
This script helps configure AWS credentials and deploy the Lambda function
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def setup_credentials():
    """Setup AWS credentials"""
    print_header("AWS Credentials Setup")
    
    # Check if credentials are already set
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if 'your_access_key' not in content:
                print("AWS credentials already configured in .env file.")
                return True
    
    # Get AWS credentials from user
    print("Please enter your AWS credentials:")
    aws_access_key = input("AWS Access Key ID: ").strip()
    aws_secret_key = input("AWS Secret Access Key: ").strip()
    aws_region = input("AWS Region (default: us-east-1): ").strip() or "us-east-1"
    
    # Update .env file
    with open('.env', 'r') as f:
        content = f.read()
    
    content = content.replace('your_access_key', aws_access_key)
    content = content.replace('your_secret_key', aws_secret_key)
    content = content.replace('us-east-1', aws_region)
    
    with open('.env', 'w') as f:
        f.write(content)
    
    print("\nAWS credentials saved to .env file.")
    return True

def check_bedrock_access():
    """Check if the user has access to Amazon Bedrock"""
    print_header("Checking Amazon Bedrock Access")
    
    try:
        # Import boto3 here to avoid dependency issues
        import boto3
        
        # Load environment variables from .env
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        
        # Create a Bedrock client
        bedrock = boto3.client('bedrock-runtime')
        
        # List available models (this will fail if no access)
        print("Checking Bedrock access...")
        try:
            bedrock.list_foundation_models()
            print("✓ You have access to Amazon Bedrock!")
            return True
        except Exception as e:
            if 'AccessDeniedException' in str(e):
                print("✗ You don't have access to Amazon Bedrock.")
                print("\nTo request access to Amazon Bedrock:")
                print("1. Go to AWS Console > Amazon Bedrock")
                print("2. Click 'Request model access'")
                print("3. Select Claude 3 Haiku model and submit request")
                return False
            else:
                print(f"✗ Error checking Bedrock access: {str(e)}")
                return False
    except ImportError:
        print("boto3 not installed. Please run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def deploy_lambda():
    """Deploy the Lambda function"""
    print_header("Deploy Lambda Function")
    
    print("This will deploy the GenAI Pipeline Lambda function to your AWS account.")
    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        return False
    
    print("\nDeploying Lambda function...")
    
    # Check if we're on Windows or Unix
    if platform.system() == 'Windows':
        # Use the Windows batch file
        result = subprocess.run(['scripts\\deploy.bat'], shell=True, capture_output=True, text=True)
    else:
        # Use the Unix shell script
        result = subprocess.run(['./scripts/deploy-lambda.sh'], shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Lambda function deployed successfully!")
        
        # Extract function URL from output if available
        output = result.stdout
        if "https://" in output:
            import re
            urls = re.findall(r'https://[^\s"\']+\.lambda-url\.[^\/\s"\']+-aws\/', output)
            if urls:
                function_url = urls[0]
                print(f"\nFunction URL: {function_url}")
                
                # Update test scripts with the new URL
                update_function_url(function_url)
        return True
    else:
        print("✗ Lambda deployment failed.")
        print(f"\nError: {result.stderr}")
        return False

def update_function_url(url):
    """Update test scripts with the new function URL"""
    files_to_update = [
        'run_test.py',
        'test_api.bat',
        'TESTING.md'
    ]
    
    for file in files_to_update:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
            
            # Replace old URL with new URL
            content = content.replace(
                "https://2fu2iveexbqvfe74qqehldjeky0urivd.lambda-url.us-east-1.on.aws/", 
                url
            )
            
            with open(file, 'w') as f:
                f.write(content)
    
    print("✓ Test scripts updated with new function URL")

def main():
    """Main function"""
    clear_screen()
    print("\nGenAI Pipeline Setup\n")
    
    # Setup credentials
    if not setup_credentials():
        print("Failed to setup AWS credentials. Exiting.")
        return
    
    # Check Bedrock access
    has_bedrock = check_bedrock_access()
    if not has_bedrock:
        print("\nYou need access to Amazon Bedrock to use this project.")
        print("Please request access and try again.")
    
    # Deploy Lambda function
    if has_bedrock:
        deploy_lambda()
    
    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Run local tests: python test_local.py")
    print("2. Test API endpoint: python run_test.py")

if __name__ == "__main__":
    main()