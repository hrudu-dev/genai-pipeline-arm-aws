#!/usr/bin/env python3
"""
Set up authentication for API Gateway
"""

import boto3
import json
import argparse
import time
import uuid
import base64
import os

# AWS credentials
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

def setup_api_key(api_id, key_name=None):
    """Set up API key for API Gateway"""
    print("Setting up API key...")
    
    # Create API Gateway client
    apigateway = boto3.client('apigateway',
                            region_name=AWS_DEFAULT_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Generate key name if not provided
    if key_name is None:
        key_name = f"GenAIPipeline-Key-{uuid.uuid4()}"
    
    # Create API key
    try:
        response = apigateway.create_api_key(
            name=key_name,
            enabled=True,
            generateDistinctId=True
        )
        
        api_key_id = response['id']
        api_key_value = response['value']
        
        print(f"Created API key: {key_name}")
        print(f"API key value: {api_key_value}")
        
        # Create usage plan
        usage_plan_response = apigateway.create_usage_plan(
            name=f"GenAIPipeline-UsagePlan-{uuid.uuid4()}",
            description='Usage plan for GenAI Pipeline API',
            apiStages=[
                {
                    'apiId': api_id,
                    'stage': 'prod'
                }
            ],
            throttle={
                'rateLimit': 10,
                'burstLimit': 20
            },
            quota={
                'limit': 1000,
                'period': 'MONTH'
            }
        )
        
        usage_plan_id = usage_plan_response['id']
        
        print(f"Created usage plan: {usage_plan_id}")
        
        # Add API key to usage plan
        apigateway.create_usage_plan_key(
            usagePlanId=usage_plan_id,
            keyId=api_key_id,
            keyType='API_KEY'
        )
        
        print(f"Added API key to usage plan")
        
        # Save API key to file
        with open('api_key.txt', 'w') as f:
            f.write(f"API Key: {api_key_value}\n")
            f.write(f"Usage Plan ID: {usage_plan_id}\n")
        
        print("API key saved to api_key.txt")
        
        return api_key_value
    except Exception as e:
        print(f"Error setting up API key: {str(e)}")
        return None

def setup_cognito_auth(api_id, user_pool_name=None):
    """Set up Cognito authentication for API Gateway"""
    print("Setting up Cognito authentication...")
    
    # Create Cognito client
    cognito = boto3.client('cognito-idp',
                         region_name=AWS_DEFAULT_REGION,
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Generate user pool name if not provided
    if user_pool_name is None:
        user_pool_name = f"GenAIPipeline-UserPool-{uuid.uuid4()}"
    
    # Create user pool
    try:
        response = cognito.create_user_pool(
            PoolName=user_pool_name,
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True,
                    'RequireSymbols': False
                }
            },
            AutoVerifiedAttributes=['email'],
            UsernameAttributes=['email'],
            MfaConfiguration='OFF'
        )
        
        user_pool_id = response['UserPool']['Id']
        
        print(f"Created user pool: {user_pool_id}")
        
        # Create user pool client
        client_response = cognito.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName=f"GenAIPipeline-Client-{uuid.uuid4()}",
            GenerateSecret=True,
            ExplicitAuthFlows=['ALLOW_USER_PASSWORD_AUTH', 'ALLOW_REFRESH_TOKEN_AUTH'],
            SupportedIdentityProviders=['COGNITO']
        )
        
        client_id = client_response['UserPoolClient']['ClientId']
        client_secret = client_response['UserPoolClient']['ClientSecret']
        
        print(f"Created user pool client: {client_id}")
        
        # Create API Gateway client
        apigateway = boto3.client('apigateway',
                                region_name=AWS_DEFAULT_REGION,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        
        # Create authorizer
        authorizer_response = apigateway.create_authorizer(
            restApiId=api_id,
            name=f"GenAIPipeline-Authorizer-{uuid.uuid4()}",
            type='COGNITO_USER_POOLS',
            providerARNs=[f"arn:aws:cognito-idp:{AWS_DEFAULT_REGION}:{boto3.client('sts').get_caller_identity()['Account']}:userpool/{user_pool_id}"],
            identitySource='method.request.header.Authorization'
        )
        
        authorizer_id = authorizer_response['id']
        
        print(f"Created authorizer: {authorizer_id}")
        
        # Save Cognito details to file
        with open('cognito_auth.txt', 'w') as f:
            f.write(f"User Pool ID: {user_pool_id}\n")
            f.write(f"Client ID: {client_id}\n")
            f.write(f"Client Secret: {client_secret}\n")
            f.write(f"Authorizer ID: {authorizer_id}\n")
        
        print("Cognito details saved to cognito_auth.txt")
        
        return {
            'user_pool_id': user_pool_id,
            'client_id': client_id,
            'client_secret': client_secret,
            'authorizer_id': authorizer_id
        }
    except Exception as e:
        print(f"Error setting up Cognito authentication: {str(e)}")
        return None

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Set up authentication for API Gateway')
    parser.add_argument('--api-id', '-a', required=True, help='API Gateway ID')
    parser.add_argument('--auth-type', '-t', choices=['api-key', 'cognito', 'both'], default='api-key', help='Authentication type')
    parser.add_argument('--key-name', '-k', help='API key name')
    parser.add_argument('--user-pool-name', '-u', help='Cognito user pool name')
    
    args = parser.parse_args()
    
    if args.auth_type in ['api-key', 'both']:
        setup_api_key(args.api_id, args.key_name)
    
    if args.auth_type in ['cognito', 'both']:
        setup_cognito_auth(args.api_id, args.user_pool_name)

if __name__ == "__main__":
    main()