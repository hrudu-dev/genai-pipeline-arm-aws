#!/usr/bin/env python3
"""
Setup script for all GenAI Pipeline features
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

def setup_all(features=None):
    """Set up all GenAI Pipeline features"""
    if features is None:
        features = ['lambda', 'api', 'batch', 'monitoring', 'web']
    
    success = True
    
    if 'lambda' in features:
        print_header("Setting up Lambda function")
        success = success and run_command("python deploy_simple.py")
    
    if 'api' in features:
        print_header("Setting up API Gateway")
        print("Note: This requires API Gateway permissions. If it fails, run 'python attach_api_policy.py' first.")
        api_success = run_command("python api_gateway_setup.py")
        if not api_success:
            print("API Gateway setup failed. You may need additional permissions.")
            print("Run 'python attach_api_policy.py' to attach the necessary policy.")
        success = success and api_success
    
    if 'monitoring' in features:
        print_header("Setting up CloudWatch monitoring")
        monitoring_success = run_command("python setup_monitoring.py")
        if not monitoring_success:
            print("CloudWatch monitoring setup failed. You may need additional permissions.")
        success = success and monitoring_success
    
    if 'multi-region' in features:
        print_header("Setting up multi-region deployment")
        multi_region_success = run_command("python multi_region_deploy.py")
        if not multi_region_success:
            print("Multi-region deployment failed. You may need additional permissions.")
        success = success and multi_region_success
    
    if 'web' in features:
        print_header("Starting Web UI")
        print("Starting simple Web UI server...")
        web_success = run_command("start python simple_web_ui.py")
        if not web_success:
            print("Web UI server failed to start. Trying alternative method...")
            web_success = run_command("start python web_ui/server.py")
        success = success and web_success
    
    if success:
        print_header("Setup complete")
        print("All features have been set up successfully!")
    else:
        print_header("Setup incomplete")
        print("Some features were not set up successfully. See logs for details.")
        print("\nYou can still use the features that were set up successfully.")
        print("For example, you can test the Lambda function with:")
        print("curl -X POST \"https://cr7c7lxj5mt2lwvyi57s2o6arq0paars.lambda-url.us-east-1.on.aws/\" \")
        print("  -H \"Content-Type: application/json\" \")
        print("  -d '{\"prompt\": \"What is artificial intelligence?\"}'")
    
    return success

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Set up all GenAI Pipeline features')
    parser.add_argument('--features', '-f', nargs='+', choices=['lambda', 'api', 'batch', 'monitoring', 'multi-region', 'web', 'all'], 
                        default=['all'], help='Features to set up')
    
    args = parser.parse_args()
    
    features = args.features
    if 'all' in features:
        features = ['lambda', 'api', 'batch', 'monitoring', 'multi-region', 'web']
    
    setup_all(features)

if __name__ == "__main__":
    main()