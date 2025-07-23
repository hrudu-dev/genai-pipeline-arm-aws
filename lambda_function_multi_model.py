import json
import os
import boto3
from cached_inference import run_cached_inference
from src.multi_model import run_inference_with_model

def lambda_handler(event, context):
    """AWS Lambda handler for model inference."""
    try:
        # Handle both API Gateway and Function URL formats
        if 'body' in event:
            data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            data = event
        
        # Check if caching is enabled
        if os.environ.get('ENABLE_CACHE', 'true').lower() == 'true':
            # Run inference with caching
            result = run_cached_inference(data, run_inference_with_model)
        else:
            # Run inference without caching
            result = run_inference_with_model(data)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }