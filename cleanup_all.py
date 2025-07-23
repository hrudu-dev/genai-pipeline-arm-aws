#!/usr/bin/env python3
"""
Script to remove credentials and stop all AWS services
"""

import boto3
import os
import dotenv
import sys

# Load environment variables from .env file
dotenv.load_dotenv()

def get_aws_credentials():
    """Get AWS credentials from environment variables"""
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    
    if not aws_access_key or not aws_secret_key:
        print("AWS credentials not found in environment variables.")
        return None, None, aws_region
    
    return aws_access_key, aws_secret_key, aws_region

def delete_lambda_function(lambda_client, function_name):
    """Delete Lambda function"""
    try:
        # Delete function URL if it exists
        try:
            lambda_client.delete_function_url_config(
                FunctionName=function_name
            )
            print(f"Deleted function URL for {function_name}")
        except:
            pass
        
        # Delete the function
        lambda_client.delete_function(
            FunctionName=function_name
        )
        print(f"Deleted Lambda function: {function_name}")
        return True
    except Exception as e:
        print(f"Error deleting Lambda function {function_name}: {str(e)}")
        return False

def delete_cloudwatch_logs(logs_client, function_name):
    """Delete CloudWatch log group for Lambda function"""
    log_group_name = f"/aws/lambda/{function_name}"
    try:
        logs_client.delete_log_group(
            logGroupName=log_group_name
        )
        print(f"Deleted CloudWatch log group: {log_group_name}")
        return True
    except Exception as e:
        print(f"Error deleting CloudWatch log group {log_group_name}: {str(e)}")
        return False

def cleanup_aws_resources():
    """Clean up AWS resources"""
    aws_access_key, aws_secret_key, aws_region = get_aws_credentials()
    
    if not aws_access_key or not aws_secret_key:
        print("Cannot clean up AWS resources without credentials.")
        return False
    
    # Create AWS clients
    lambda_client = boto3.client('lambda',
                               region_name=aws_region,
                               aws_access_key_id=aws_access_key,
                               aws_secret_access_key=aws_secret_key)
    
    logs_client = boto3.client('logs',
                             region_name=aws_region,
                             aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key)
    
    # Delete Lambda function
    function_name = "GenAIPipelineTest2"
    delete_lambda_function(lambda_client, function_name)
    
    # Delete CloudWatch logs
    delete_cloudwatch_logs(logs_client, function_name)
    
    return True

def remove_credentials():
    """Remove credentials from .env file"""
    try:
        # Create a clean .env file without credentials
        with open('.env', 'w') as f:
            f.write("# AWS credentials have been removed for security\n")
            f.write("PROJECT_NAME=GenAIPipeline\n")
            f.write("ENVIRONMENT=dev\n")
        
        print("Removed credentials from .env file")
        return True
    except Exception as e:
        print(f"Error removing credentials: {str(e)}")
        return False

def main():
    """Main function"""
    print("Cleaning up AWS resources and removing credentials...")
    
    # Confirm action
    confirm = input("This will delete all AWS resources and remove credentials. Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Clean up AWS resources
    cleanup_success = cleanup_aws_resources()
    
    # Remove credentials
    creds_success = remove_credentials()
    
    if cleanup_success and creds_success:
        print("\nCleanup completed successfully!")
        print("All AWS resources have been deleted and credentials have been removed.")
    else:
        print("\nCleanup completed with some errors.")
        print("Please check the output above for details.")

if __name__ == "__main__":
    main()