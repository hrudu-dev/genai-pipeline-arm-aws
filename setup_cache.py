#!/usr/bin/env python3
"""
Set up DynamoDB cache table for GenAI Pipeline
"""

import boto3
import json
import time

# AWS credentials
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

def setup_cache_table():
    """Set up DynamoDB cache table"""
    print("Setting up DynamoDB cache table...")
    
    # Create DynamoDB client
    dynamodb = boto3.client('dynamodb',
                          region_name=AWS_DEFAULT_REGION,
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    table_name = 'GenAIPipelineCache'
    
    # Check if table exists
    try:
        response = dynamodb.describe_table(TableName=table_name)
        print(f"Table {table_name} already exists")
        return table_name
    except dynamodb.exceptions.ResourceNotFoundException:
        print(f"Table {table_name} does not exist, creating...")
    
    # Create table
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'cache_key',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'cache_key',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        print(f"Table {table_name} is being created...")
        
        # Wait for table to be created
        print("Waiting for table to be created...")
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        
        print(f"Table {table_name} created successfully")
        
        # Add TTL attribute
        dynamodb.update_time_to_live(
            TableName=table_name,
            TimeToLiveSpecification={
                'Enabled': True,
                'AttributeName': 'expiration_time'
            }
        )
        
        print(f"TTL enabled for table {table_name}")
        
        return table_name
    except Exception as e:
        print(f"Error creating table: {str(e)}")
        return None

def main():
    """Main function"""
    setup_cache_table()

if __name__ == "__main__":
    main()