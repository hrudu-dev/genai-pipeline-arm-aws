import json
import os
import boto3

def lambda_handler(event, context):
    """AWS Lambda handler for model inference."""
    try:
        # Handle CORS preflight requests
        http_method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method', 'POST')
        
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Accept, Authorization',
                    'Access-Control-Max-Age': '86400'
                }
            }
        
        # Handle both API Gateway and Function URL formats
        if 'body' in event:
            body = event['body']
            if isinstance(body, str):
                data = json.loads(body) if body else {}
            else:
                data = body or {}
        else:
            data = event
        
        # Validate request
        if not data.get('prompt'):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing prompt in request'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        
        # Run inference
        result = run_inference(data)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Accept, Authorization'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'inference_complete': False,
                'error': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

def run_inference(data):
    """Run GenAI model inference on processed data."""
    try:
        # Use the Lambda execution role's permissions
        aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        bedrock = boto3.client('bedrock-runtime', region_name=aws_region)
        
        # Prepare prompt
        prompt = data.get('prompt', 'Hello, how can I help you?')
        
        # Call Bedrock model with correct model ID
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',  # Updated model ID
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 500,
                'messages': [{'role': 'user', 'content': prompt}]
            })
        )
        
        response_body = json.loads(response.get('body').read())
        return {
            'inference_complete': True,
            'result': response_body['content'][0]['text'],
            'data': data
        }
    except Exception as e:
        return {
            'inference_complete': False,
            'error': str(e),
            'data': data
        }