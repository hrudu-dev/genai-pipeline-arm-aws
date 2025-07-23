#!/usr/bin/env python3
"""
Deploy all features of GenAI Pipeline
"""

import os
import sys
import subprocess
import argparse
import json
import time

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

def deploy_all(features=None):
    """Deploy all features of GenAI Pipeline"""
    if features is None:
        features = ['lambda', 'cache', 'api', 'auth', 'monitoring', 'rate-limiting', 'multi-model']
    
    success = True
    
    # Deploy Lambda function
    if 'lambda' in features:
        print_header("Deploying Lambda function")
        success = success and run_command("python deploy_simple.py")
    
    # Set up cache
    if 'cache' in features and success:
        print_header("Setting up cache")
        success = success and run_command("python setup_cache.py")
        success = success and run_command("python deploy_simple.py --function lambda_function_cached.py")
    
    # Set up API Gateway
    if 'api' in features and success:
        print_header("Setting up API Gateway")
        api_id = input("Enter your API Gateway ID (leave blank to skip): ")
        if api_id:
            success = success and run_command(f"python api_gateway_setup.py --api-id {api_id}")
    
    # Set up authentication
    if 'auth' in features and success:
        print_header("Setting up authentication")
        api_id = input("Enter your API Gateway ID (leave blank to skip): ")
        if api_id:
            auth_type = input("Enter authentication type (api-key, cognito, both): ")
            success = success and run_command(f"python setup_auth.py --api-id {api_id} --auth-type {auth_type}")
    
    # Set up monitoring
    if 'monitoring' in features and success:
        print_header("Setting up monitoring")
        function_name = input("Enter your Lambda function name (leave blank to use default): ") or "GenAIPipelineTest2"
        success = success and run_command(f"python setup_monitoring.py --function {function_name}")
        success = success and run_command(f"python setup_cache_monitoring.py --function {function_name}")
    
    # Set up rate limiting
    if 'rate-limiting' in features and success:
        print_header("Setting up rate limiting")
        api_id = input("Enter your API Gateway ID (leave blank to skip): ")
        if api_id:
            rate_limit = input("Enter rate limit (requests per second, default: 10): ") or "10"
            quota_limit = input("Enter quota limit (requests per month, default: 1000): ") or "1000"
            success = success and run_command(f"python setup_rate_limiting.py --api-id {api_id} --rate-limit {rate_limit} --quota-limit {quota_limit}")
    
    # Set up multi-model support
    if 'multi-model' in features and success:
        print_header("Setting up multi-model support")
        success = success and run_command("python deploy_simple.py --function lambda_function_multi_model.py")
    
    # Optimize Lambda function
    if 'optimize' in features and success:
        print_header("Optimizing Lambda function")
        function_name = input("Enter your Lambda function name (leave blank to use default): ") or "GenAIPipelineTest2"
        memory = input("Enter memory size in MB (leave blank to skip): ")
        timeout = input("Enter timeout in seconds (leave blank to skip): ")
        
        command = f"python optimize_lambda.py --function {function_name}"
        if memory:
            command += f" --memory {memory}"
        if timeout:
            command += f" --timeout {timeout}"
        
        success = success and run_command(command)
    
    if success:
        print_header("Deployment complete")
        print("All features have been deployed successfully!")
        
        # Save deployment information
        deployment_info = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'features': features,
            'success': True
        }
        
        with open('deployment_info.json', 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        print("Deployment information saved to deployment_info.json")
    else:
        print_header("Deployment failed")
        print("One or more features failed to deploy. Please check the logs for details.")
    
    return success

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Deploy all features of GenAI Pipeline')
    parser.add_argument('--features', '-f', nargs='+', 
                        choices=['lambda', 'cache', 'api', 'auth', 'monitoring', 'rate-limiting', 'multi-model', 'optimize', 'all'], 
                        default=['all'], help='Features to deploy')
    
    args = parser.parse_args()
    
    features = args.features
    if 'all' in features:
        features = ['lambda', 'cache', 'api', 'auth', 'monitoring', 'rate-limiting', 'multi-model', 'optimize']
    
    deploy_all(features)

if __name__ == "__main__":
    main()