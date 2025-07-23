#!/usr/bin/env python3
"""
Test the authenticated API
"""

import requests
import json
import argparse
import boto3
import base64
import os
import time

def test_api_key_auth(api_url, api_key, prompt):
    """Test API with API key authentication"""
    print(f"Testing API with API key authentication...")
    
    # Prepare request
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    data = {
        "prompt": prompt
    }
    
    # Send request
    print("Sending request...")
    response = requests.post(api_url, headers=headers, json=data)
    
    # Print response
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("inference_complete"):
            print("\nResponse:")
            print("-" * 80)
            print(response_json["result"])
            print("-" * 80)
        else:
            print(f"Error: {response_json.get('error', 'Unknown error')}")
    else:
        print(f"Error: {response.text}")

def test_cognito_auth(api_url, user_pool_id, client_id, client_secret, username, password, prompt):
    """Test API with Cognito authentication"""
    print(f"Testing API with Cognito authentication...")
    
    # Create Cognito client
    cognito = boto3.client('cognito-idp',
                         region_name=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1'),
                         aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    
    # Authenticate with Cognito
    try:
        auth_response = cognito.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': base64.b64encode(
                    hmac.new(
                        client_secret.encode('utf-8'),
                        (username + client_id).encode('utf-8'),
                        digestmod=hashlib.sha256
                    ).digest()
                ).decode('utf-8')
            }
        )
        
        id_token = auth_response['AuthenticationResult']['IdToken']
        
        print(f"Authenticated with Cognito")
        
        # Prepare request
        headers = {
            "Content-Type": "application/json",
            "Authorization": id_token
        }
        data = {
            "prompt": prompt
        }
        
        # Send request
        print("Sending request...")
        response = requests.post(api_url, headers=headers, json=data)
        
        # Print response
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("inference_complete"):
                print("\nResponse:")
                print("-" * 80)
                print(response_json["result"])
                print("-" * 80)
            else:
                print(f"Error: {response_json.get('error', 'Unknown error')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error authenticating with Cognito: {str(e)}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Test the authenticated API')
    parser.add_argument('--api-url', '-u', required=True, help='API URL')
    parser.add_argument('--auth-type', '-t', choices=['api-key', 'cognito'], default='api-key', help='Authentication type')
    parser.add_argument('--api-key', '-k', help='API key')
    parser.add_argument('--user-pool-id', '-p', help='Cognito user pool ID')
    parser.add_argument('--client-id', '-c', help='Cognito client ID')
    parser.add_argument('--client-secret', '-s', help='Cognito client secret')
    parser.add_argument('--username', '-n', help='Cognito username')
    parser.add_argument('--password', '-w', help='Cognito password')
    parser.add_argument('--prompt', '-m', default='What is artificial intelligence?', help='Prompt to send to the API')
    
    args = parser.parse_args()
    
    if args.auth_type == 'api-key':
        if not args.api_key:
            print("Error: API key is required for API key authentication")
            return
        test_api_key_auth(args.api_url, args.api_key, args.prompt)
    elif args.auth_type == 'cognito':
        if not all([args.user_pool_id, args.client_id, args.client_secret, args.username, args.password]):
            print("Error: User pool ID, client ID, client secret, username, and password are required for Cognito authentication")
            return
        test_cognito_auth(args.api_url, args.user_pool_id, args.client_id, args.client_secret, args.username, args.password, args.prompt)

if __name__ == "__main__":
    main()