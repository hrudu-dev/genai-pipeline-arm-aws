#!/usr/bin/env python3
"""
Script to set up AWS credentials and push to Git
"""

import os
import subprocess
import getpass
import sys
import json

def run_command(command):
    """Run a shell command and return the output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout.strip()

def setup_aws_credentials():
    """Set up AWS credentials"""
    print("\n=== Setting Up AWS Credentials ===")
    
    # Get AWS credentials from user
    aws_access_key = input("Enter AWS Access Key ID: ")
    aws_secret_key = getpass.getpass("Enter AWS Secret Access Key: ")
    aws_region = input("Enter AWS Region (default: us-east-1): ") or "us-east-1"
    
    # Update .env file
    with open(".env", "w") as f:
        f.write(f"AWS_ACCESS_KEY_ID={aws_access_key}\n")
        f.write(f"AWS_SECRET_ACCESS_KEY={aws_secret_key}\n")
        f.write(f"AWS_DEFAULT_REGION={aws_region}\n")
        f.write("\n# Project configuration\n")
        f.write("PROJECT_NAME=GenAIPipeline\n")
        f.write("ENVIRONMENT=dev\n")
        f.write("S3_BUCKET=genai-pipeline-artifacts-12345\n")
        f.write("STACK_NAME=GenAIPipelineStack\n")
    
    print("AWS credentials saved to .env file")
    
    # Create IAM resources
    create_iam = input("Create IAM resources for testing? (y/n): ").lower()
    if create_iam == 'y':
        print("Running IAM setup script...")
        if os.name == 'nt':  # Windows
            os.system("py iam/setup-iam.py")
        else:  # Linux/Mac
            os.system("python iam/setup-iam.py")

def setup_git():
    """Set up Git repository and push changes"""
    print("\n=== Setting Up Git Repository ===")
    
    # Check if .gitignore exists, create if not
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
            f.write(".env\n")
            f.write("__pycache__/\n")
            f.write("*.pyc\n")
            f.write("*.pyo\n")
            f.write("*.pyd\n")
            f.write(".Python\n")
            f.write("env/\n")
            f.write("venv/\n")
            f.write("ENV/\n")
            f.write("build/\n")
            f.write("develop-eggs/\n")
            f.write("dist/\n")
            f.write("downloads/\n")
            f.write("eggs/\n")
            f.write(".eggs/\n")
            f.write("lib/\n")
            f.write("lib64/\n")
            f.write("parts/\n")
            f.write("sdist/\n")
            f.write("var/\n")
            f.write("*.egg-info/\n")
            f.write(".installed.cfg\n")
            f.write("*.egg\n")
            f.write("*.zip\n")
            f.write("function.zip\n")
            f.write("simple_function.zip\n")
            f.write("genai-pipeline-arm64.zip\n")
            f.write("genai-pipeline-minimal.zip\n")
            f.write("multi_region_function.zip\n")
        print("Created .gitignore file")
    
    # Get Git repository URL
    git_url = input("Enter Git repository URL (leave blank to use existing): ")
    
    if git_url:
        # Initialize Git repository
        run_command("git init")
        run_command(f"git remote add origin {git_url}")
        print(f"Git repository initialized with remote: {git_url}")
    
    # Add all files
    run_command("git add .")
    
    # Commit changes
    commit_message = input("Enter commit message (default: 'Initial commit'): ") or "Initial commit"
    run_command(f'git commit -m "{commit_message}"')
    
    # Push to remote
    push = input("Push to remote repository? (y/n): ").lower()
    if push == 'y':
        branch_name = input("Enter branch name (default: main): ") or "main"
        result = run_command(f"git push -u origin {branch_name}")
        if result:
            print(f"Successfully pushed to {branch_name} branch")
        else:
            print("Failed to push to remote repository")
    
    # Set up GitHub Actions
    setup_actions = input("Set up GitHub Actions secrets for CI/CD? (y/n): ").lower()
    if setup_actions == 'y':
        print("\nTo set up GitHub Actions secrets:")
        print("1. Go to your GitHub repository")
        print("2. Click on Settings > Secrets and variables > Actions")
        print("3. Add the following secrets:")
        print("   - AWS_ACCESS_KEY_ID")
        print("   - AWS_SECRET_ACCESS_KEY")
        print("   - AWS_DEFAULT_REGION")

def main():
    print("GenAI Pipeline Setup and Push")
    print("============================")
    
    # Setup AWS credentials
    setup_aws = input("Set up AWS credentials? (y/n): ").lower()
    if setup_aws == 'y':
        setup_aws_credentials()
    
    # Setup Git
    setup_git_repo = input("Set up Git repository and push changes? (y/n): ").lower()
    if setup_git_repo == 'y':
        setup_git()
    
    print("\nSetup complete!")

if __name__ == "__main__":
    main()