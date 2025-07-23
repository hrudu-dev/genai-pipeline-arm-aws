#!/usr/bin/env python3
"""
Optimize Lambda function for cost and performance
"""

import boto3
import json
import argparse
import time

# AWS credentials
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

def optimize_lambda(function_name, memory=None, timeout=None, provisioned_concurrency=None):
    """Optimize Lambda function configuration"""
    print(f"Optimizing Lambda function: {function_name}")
    
    # Create Lambda client
    lambda_client = boto3.client('lambda',
                               region_name=AWS_DEFAULT_REGION,
                               aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Get current configuration
    try:
        response = lambda_client.get_function_configuration(FunctionName=function_name)
        current_memory = response['MemorySize']
        current_timeout = response['Timeout']
        
        print(f"Current configuration:")
        print(f"- Memory: {current_memory} MB")
        print(f"- Timeout: {current_timeout} seconds")
        
        # Update configuration if needed
        update_config = {}
        
        if memory is not None and memory != current_memory:
            update_config['MemorySize'] = memory
        
        if timeout is not None and timeout != current_timeout:
            update_config['Timeout'] = timeout
        
        if update_config:
            print(f"Updating configuration:")
            if 'MemorySize' in update_config:
                print(f"- Memory: {update_config['MemorySize']} MB")
            if 'Timeout' in update_config:
                print(f"- Timeout: {update_config['Timeout']} seconds")
            
            lambda_client.update_function_configuration(
                FunctionName=function_name,
                **update_config
            )
            
            print("Configuration updated successfully")
        else:
            print("No configuration changes needed")
        
        # Set up provisioned concurrency if specified
        if provisioned_concurrency is not None:
            print(f"Setting up provisioned concurrency: {provisioned_concurrency}")
            
            # Get function version
            version_response = lambda_client.publish_version(
                FunctionName=function_name,
                Description=f"Optimized version with provisioned concurrency {provisioned_concurrency}"
            )
            
            version = version_response['Version']
            
            # Set up provisioned concurrency
            lambda_client.put_provisioned_concurrency_config(
                FunctionName=function_name,
                Qualifier=version,
                ProvisionedConcurrentExecutions=provisioned_concurrency
            )
            
            print(f"Provisioned concurrency set up for version {version}")
        
        # Calculate cost estimates
        memory_price_per_ms = 0.0000000167  # $0.0000000167 per GB-ms for ARM64
        
        # Convert memory to GB
        memory_gb = (memory or current_memory) / 1024
        
        # Estimate cost per invocation (assuming average execution time of 1 second)
        avg_execution_time_ms = 1000
        cost_per_invocation = memory_gb * avg_execution_time_ms * memory_price_per_ms
        
        print("\nCost estimates:")
        print(f"- Cost per invocation: ${cost_per_invocation:.8f}")
        print(f"- Cost per 1M invocations: ${cost_per_invocation * 1000000:.2f}")
        
        if provisioned_concurrency is not None:
            # Provisioned concurrency cost: $0.000004 per GB-second for ARM64
            pc_cost_per_hour = provisioned_concurrency * memory_gb * 3600 * 0.000004
            pc_cost_per_month = pc_cost_per_hour * 24 * 30
            
            print(f"- Provisioned concurrency cost per hour: ${pc_cost_per_hour:.2f}")
            print(f"- Provisioned concurrency cost per month: ${pc_cost_per_month:.2f}")
        
        return True
    except Exception as e:
        print(f"Error optimizing Lambda function: {str(e)}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Optimize Lambda function for cost and performance')
    parser.add_argument('--function', '-f', default='GenAIPipelineTest2', help='Lambda function name')
    parser.add_argument('--memory', '-m', type=int, help='Memory size in MB (128-10240)')
    parser.add_argument('--timeout', '-t', type=int, help='Timeout in seconds (1-900)')
    parser.add_argument('--provisioned-concurrency', '-p', type=int, help='Provisioned concurrency')
    
    args = parser.parse_args()
    
    optimize_lambda(args.function, args.memory, args.timeout, args.provisioned_concurrency)

if __name__ == "__main__":
    main()