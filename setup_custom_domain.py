#!/usr/bin/env python3
"""
Set up custom domain name for API Gateway
"""

import boto3
import json
import argparse
import time

# AWS credentials
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

def setup_custom_domain(domain_name, certificate_arn, api_id):
    """Set up custom domain name for API Gateway"""
    print(f"Setting up custom domain name: {domain_name}")
    
    # Create API Gateway client
    apigateway = boto3.client('apigateway',
                            region_name=AWS_DEFAULT_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Create custom domain name
    try:
        response = apigateway.create_domain_name(
            domainName=domain_name,
            certificateArn=certificate_arn,
            endpointConfiguration={
                'types': ['REGIONAL']
            },
            securityPolicy='TLS_1_2'
        )
        
        print(f"Created custom domain name: {domain_name}")
        print(f"Distribution domain name: {response['distributionDomainName']}")
        
        # Create base path mapping
        apigateway.create_base_path_mapping(
            domainName=domain_name,
            restApiId=api_id,
            stage='prod'
        )
        
        print(f"Created base path mapping for API: {api_id}")
        print("\nTo use your custom domain name:")
        print(f"1. Create a CNAME record in your DNS provider pointing {domain_name} to {response['distributionDomainName']}")
        print("2. Wait for DNS propagation (may take up to 24 hours)")
        print(f"3. Access your API at https://{domain_name}/")
        
        return response['distributionDomainName']
    except Exception as e:
        print(f"Error creating custom domain name: {str(e)}")
        return None

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Set up custom domain name for API Gateway')
    parser.add_argument('--domain', '-d', required=True, help='Custom domain name (e.g., api.example.com)')
    parser.add_argument('--cert-arn', '-c', required=True, help='ACM certificate ARN')
    parser.add_argument('--api-id', '-a', required=True, help='API Gateway ID')
    
    args = parser.parse_args()
    
    setup_custom_domain(args.domain, args.cert_arn, args.api_id)

if __name__ == "__main__":
    main()