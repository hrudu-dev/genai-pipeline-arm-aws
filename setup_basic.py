#!/usr/bin/env python3
"""
Setup script for basic GenAI Pipeline features (no additional permissions required)
"""

import os
import sys
import subprocess
import webbrowser

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

def setup_basic():
    """Set up basic GenAI Pipeline features"""
    print_header("Setting up Lambda function")
    success = run_command("python deploy_simple.py")
    
    if success:
        print_header("Starting Web UI")
        run_command("start python simple_web_ui.py")
        
        print_header("Setup complete")
        print("Basic features have been set up successfully!")
        print("\nYou can now:")
        print("1. Use the Web UI to interact with the API")
        print("2. Test the API directly with curl:")
        print('   curl -X POST "https://cr7c7lxj5mt2lwvyi57s2o6arq0paars.lambda-url.us-east-1.on.aws/" -H "Content-Type: application/json" -d \'{"prompt": "What is artificial intelligence?"}\'')
        print("3. Process batch prompts:")
        print("   python batch_processing.py sample_prompts.txt")
    else:
        print_header("Setup failed")
        print("Failed to set up Lambda function. Please check the logs for details.")
    
    return success

if __name__ == "__main__":
    setup_basic()