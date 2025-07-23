#!/usr/bin/env python3
"""
Deploy advanced features for GenAI Pipeline
"""

import os
import sys
import subprocess
import argparse

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def run_command(command):
    """Run a command and print the output"""
    print(f"Running: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())
    
    return process.returncode == 0

def deploy_advanced_features(features=None):
    """Deploy advanced features for GenAI Pipeline"""
    if features is None:
        features = ['cache', 'auth', 'domain']
    
    success = True
    
    # Deploy Lambda function
    print_header("Deploying Lambda function")
    success = success and run_command("python deploy_simple.py")
    
    # Set up API Gateway
    print_header("Setting up API Gateway")
    api_id = input("Enter your API Gateway ID: ")
    
    # Set up cache
    if 'cache' in features:
        print_header("Setting up cache")
        success = success and run_command("python setup_cache.py")
        success = success and run_command("python deploy_simple.py --function lambda_function_cached.py")
    
    # Set up authentication
    if 'auth' in features:
        print_header("Setting up authentication")
        auth_type = input("Enter authentication type (api-key, cognito, both): ")
        success = success and run_command(f"python setup_auth.py --api-id {api_id} --auth-type {auth_type}")
    
    # Set up custom domain
    if 'domain' in features:
        print_header("Setting up custom domain")
        domain = input("Enter your custom domain name: ")
        cert_arn = input("Enter your SSL certificate ARN: ")
        success = success and run_command(f"python setup_custom_domain.py --domain {domain} --cert-arn {cert_arn} --api-id {api_id}")
    
    if success:
        print_header("Deployment complete")
        print("Advanced features have been deployed successfully!")
    else:
        print_header("Deployment failed")
        print("One or more features failed to deploy. Please check the logs for details.")
    
    return success

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Deploy advanced features for GenAI Pipeline')
    parser.add_argument('--features', '-f', nargs='+', choices=['cache', 'auth', 'domain', 'all'], 
                        default=['all'], help='Features to deploy')
    
    args = parser.parse_args()
    
    features = args.features
    if 'all' in features:
        features = ['cache', 'auth', 'domain']
    
    deploy_advanced_features(features)

if __name__ == "__main__":
    main()