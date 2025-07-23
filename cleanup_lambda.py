#!/usr/bin/env python3
"""
Simple script to delete Lambda functions created by the GenAI Pipeline project.
"""

import boto3
import sys

def cleanup_lambda():
    """Delete Lambda functions"""
    print("Cleaning up Lambda functions...")
    lambda_client = boto3.client('lambda')
    
    # List of function names that might exist
    functions = [
        "GenAIPipeline-Inference",
        "GenAIPipelineTest2", 
        "GenAIPipelineMultiRegion",
        "GenAIPipeline",
        "GenAIPipelineCached"
    ]
    
    for function in functions:
        try:
            lambda_client.delete_function(FunctionName=function)
            print(f"✅ Deleted Lambda function: {function}")
        except lambda_client.exceptions.ResourceNotFoundException:
            print(f"⚠️ Lambda function not found: {function}")
        except Exception as e:
            print(f"❌ Error deleting Lambda function {function}: {e}")

if __name__ == "__main__":
    print("GenAI Pipeline Lambda Cleanup")
    print("=============================")
    
    confirm = input("Delete all GenAI Pipeline Lambda functions? (y/n): ")
    if confirm.lower() != 'y':
        print("Cleanup cancelled.")
        sys.exit(0)
    
    cleanup_lambda()
    print("\nLambda cleanup complete!")