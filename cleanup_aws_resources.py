#!/usr/bin/env python3
"""
Script to clean up old AWS resources created by the GenAI Pipeline
"""

import boto3
import argparse
import os
import datetime
import dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
dotenv.load_dotenv()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Clean up old AWS resources')
    parser.add_argument('--older-than', type=int, default=30,
                        help='Delete resources older than this many days')
    parser.add_argument('--dry-run', action='store_true',
                        help='Dry run (do not actually delete resources)')
    parser.add_argument('--region', type=str,
                        default=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1'),
                        help='AWS region')
    parser.add_argument('--prefix', type=str,
                        default=os.environ.get('PROJECT_NAME', 'GenAIPipeline'),
                        help='Resource name prefix')
    return parser.parse_args()

def cleanup_lambda_functions(args):
    """Clean up old Lambda functions"""
    print(f"Cleaning up Lambda functions older than {args.older_than} days...")
    
    lambda_client = boto3.client('lambda', region_name=args.region)
    
    # Get current time
    now = datetime.now()
    cutoff_date = now - timedelta(days=args.older_than)
    
    # List Lambda functions
    response = lambda_client.list_functions()
    functions = response.get('Functions', [])
    
    # Filter functions by prefix and age
    for function in functions:
        function_name = function['FunctionName']
        if function_name.startswith(args.prefix):
            # Get function last modified time
            last_modified = datetime.strptime(
                function['LastModified'].split('.')[0],
                '%Y-%m-%dT%H:%M:%S'
            )
            
            if last_modified < cutoff_date:
                print(f"Found old function: {function_name} (Last modified: {last_modified})")
                
                if not args.dry_run:
                    try:
                        # Delete function URL if it exists
                        try:
                            lambda_client.delete_function_url_config(
                                FunctionName=function_name
                            )
                            print(f"  Deleted function URL for {function_name}")
                        except lambda_client.exceptions.ResourceNotFoundException:
                            pass
                        
                        # Delete the function
                        lambda_client.delete_function(
                            FunctionName=function_name
                        )
                        print(f"  Deleted function: {function_name}")
                    except Exception as e:
                        print(f"  Error deleting function {function_name}: {str(e)}")

def cleanup_cloudwatch_logs(args):
    """Clean up old CloudWatch log groups"""
    print(f"Cleaning up CloudWatch log groups older than {args.older_than} days...")
    
    logs_client = boto3.client('logs', region_name=args.region)
    
    # Get current time
    now = datetime.now()
    cutoff_date = now - timedelta(days=args.older_than)
    
    # List log groups
    response = logs_client.describe_log_groups(
        logGroupNamePrefix=f"/aws/lambda/{args.prefix}"
    )
    log_groups = response.get('logGroups', [])
    
    # Filter log groups by age
    for log_group in log_groups:
        log_group_name = log_group['logGroupName']
        creation_time = datetime.fromtimestamp(log_group['creationTime'] / 1000)
        
        if creation_time < cutoff_date:
            print(f"Found old log group: {log_group_name} (Created: {creation_time})")
            
            if not args.dry_run:
                try:
                    logs_client.delete_log_group(
                        logGroupName=log_group_name
                    )
                    print(f"  Deleted log group: {log_group_name}")
                except Exception as e:
                    print(f"  Error deleting log group {log_group_name}: {str(e)}")

def cleanup_dynamodb_tables(args):
    """Clean up old DynamoDB tables"""
    print(f"Cleaning up DynamoDB tables older than {args.older_than} days...")
    
    dynamodb_client = boto3.client('dynamodb', region_name=args.region)
    
    # Get current time
    now = datetime.now()
    cutoff_date = now - timedelta(days=args.older_than)
    
    # List tables
    response = dynamodb_client.list_tables()
    tables = response.get('TableNames', [])
    
    # Filter tables by prefix and age
    for table_name in tables:
        if table_name.startswith(args.prefix):
            # Get table creation time
            table_info = dynamodb_client.describe_table(TableName=table_name)
            creation_time = table_info['Table']['CreationDateTime']
            
            if creation_time < cutoff_date:
                print(f"Found old table: {table_name} (Created: {creation_time})")
                
                if not args.dry_run:
                    try:
                        dynamodb_client.delete_table(
                            TableName=table_name
                        )
                        print(f"  Deleted table: {table_name}")
                    except Exception as e:
                        print(f"  Error deleting table {table_name}: {str(e)}")

def main():
    """Main function"""
    args = parse_args()
    
    print(f"{'DRY RUN: ' if args.dry_run else ''}Cleaning up resources older than {args.older_than} days with prefix '{args.prefix}' in region '{args.region}'")
    
    cleanup_lambda_functions(args)
    cleanup_cloudwatch_logs(args)
    cleanup_dynamodb_tables(args)
    
    print("Cleanup complete!")

if __name__ == "__main__":
    main()