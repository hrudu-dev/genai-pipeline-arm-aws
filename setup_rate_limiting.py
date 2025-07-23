#!/usr/bin/env python3
"""
Set up rate limiting and quota management for API Gateway
"""

import boto3
import json
import argparse
import time
import uuid

# AWS credentials
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

def setup_rate_limiting(api_id, rate_limit=10, burst_limit=20, quota_limit=1000, quota_period='MONTH'):
    """Set up rate limiting and quota management for API Gateway"""
    print(f"Setting up rate limiting and quota management for API Gateway: {api_id}")
    
    # Create API Gateway client
    apigateway = boto3.client('apigateway',
                            region_name=AWS_DEFAULT_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Create usage plan
    try:
        usage_plan_response = apigateway.create_usage_plan(
            name=f"GenAIPipeline-UsagePlan-{uuid.uuid4()}",
            description='Usage plan for GenAI Pipeline API with rate limiting and quota management',
            apiStages=[
                {
                    'apiId': api_id,
                    'stage': 'prod'
                }
            ],
            throttle={
                'rateLimit': rate_limit,
                'burstLimit': burst_limit
            },
            quota={
                'limit': quota_limit,
                'period': quota_period
            }
        )
        
        usage_plan_id = usage_plan_response['id']
        
        print(f"Created usage plan: {usage_plan_id}")
        print(f"- Rate limit: {rate_limit} requests per second")
        print(f"- Burst limit: {burst_limit} requests")
        print(f"- Quota limit: {quota_limit} requests per {quota_period.lower()}")
        
        # Create API key
        api_key_response = apigateway.create_api_key(
            name=f"GenAIPipeline-Key-{uuid.uuid4()}",
            description='API key for GenAI Pipeline API with rate limiting and quota management',
            enabled=True
        )
        
        api_key_id = api_key_response['id']
        api_key_value = api_key_response['value']
        
        print(f"Created API key: {api_key_id}")
        
        # Add API key to usage plan
        apigateway.create_usage_plan_key(
            usagePlanId=usage_plan_id,
            keyId=api_key_id,
            keyType='API_KEY'
        )
        
        print(f"Added API key to usage plan")
        
        # Save API key to file
        with open('api_key_with_rate_limiting.txt', 'w') as f:
            f.write(f"API Key: {api_key_value}\n")
            f.write(f"Usage Plan ID: {usage_plan_id}\n")
            f.write(f"Rate Limit: {rate_limit} requests per second\n")
            f.write(f"Burst Limit: {burst_limit} requests\n")
            f.write(f"Quota Limit: {quota_limit} requests per {quota_period.lower()}\n")
        
        print("API key and usage plan details saved to api_key_with_rate_limiting.txt")
        
        # Create method settings for throttling
        try:
            apigateway.update_stage(
                restApiId=api_id,
                stageName='prod',
                patchOperations=[
                    {
                        'op': 'replace',
                        'path': '/*/*/throttling/rateLimit',
                        'value': str(rate_limit)
                    },
                    {
                        'op': 'replace',
                        'path': '/*/*/throttling/burstLimit',
                        'value': str(burst_limit)
                    }
                ]
            )
            
            print("Updated stage with throttling settings")
        except Exception as e:
            print(f"Error updating stage: {str(e)}")
        
        return {
            'usage_plan_id': usage_plan_id,
            'api_key_id': api_key_id,
            'api_key_value': api_key_value
        }
    except Exception as e:
        print(f"Error setting up rate limiting: {str(e)}")
        return None

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Set up rate limiting and quota management for API Gateway')
    parser.add_argument('--api-id', '-a', required=True, help='API Gateway ID')
    parser.add_argument('--rate-limit', '-r', type=float, default=10, help='Rate limit (requests per second)')
    parser.add_argument('--burst-limit', '-b', type=int, default=20, help='Burst limit (requests)')
    parser.add_argument('--quota-limit', '-q', type=int, default=1000, help='Quota limit (requests)')
    parser.add_argument('--quota-period', '-p', choices=['DAY', 'WEEK', 'MONTH'], default='MONTH', help='Quota period')
    
    args = parser.parse_args()
    
    setup_rate_limiting(args.api_id, args.rate_limit, args.burst_limit, args.quota_limit, args.quota_period)

if __name__ == "__main__":
    main()