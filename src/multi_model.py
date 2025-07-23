"""
Multi-model support for GenAI Pipeline
"""

import json
import os
import boto3

# Model configurations
MODELS = {
    'claude-haiku': {
        'id': 'anthropic.claude-3-haiku-20240307-v1:0',
        'provider': 'bedrock',
        'max_tokens': 500,
        'temperature': 0.7,
        'top_p': 0.9
    },
    'claude-sonnet': {
        'id': 'anthropic.claude-3-sonnet-20240229-v1:0',
        'provider': 'bedrock',
        'max_tokens': 1000,
        'temperature': 0.7,
        'top_p': 0.9
    },
    'claude-opus': {
        'id': 'anthropic.claude-3-opus-20240229-v1:0',
        'provider': 'bedrock',
        'max_tokens': 1500,
        'temperature': 0.7,
        'top_p': 0.9
    },
    'titan-text': {
        'id': 'amazon.titan-text-express-v1',
        'provider': 'bedrock',
        'max_tokens': 500,
        'temperature': 0.7,
        'top_p': 0.9
    },
    'llama3': {
        'id': 'meta.llama3-70b-instruct-v1',
        'provider': 'bedrock',
        'max_tokens': 500,
        'temperature': 0.7,
        'top_p': 0.9
    }
}

def get_model_config(model_name):
    """Get model configuration"""
    if model_name in MODELS:
        return MODELS[model_name]
    else:
        # Default to Claude Haiku
        return MODELS['claude-haiku']

def run_inference_with_model(data, model_name=None):
    """Run inference with specified model"""
    try:
        # Get model name from data or use default
        if model_name is None:
            model_name = data.get('model', 'claude-haiku')
        
        # Get model configuration
        model_config = get_model_config(model_name)
        
        # Get credentials from environment variables if available
        aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        
        # Create Bedrock client
        bedrock = boto3.client('bedrock-runtime', region_name=aws_region)
        
        # Prepare prompt
        prompt = data.get('prompt', 'Hello, how can I help you?')
        
        # Call model based on provider
        if model_config['provider'] == 'bedrock':
            # Handle different model providers
            if 'anthropic' in model_config['id']:
                # Anthropic models (Claude)
                response = bedrock.invoke_model(
                    modelId=model_config['id'],
                    contentType='application/json',
                    accept='application/json',
                    body=json.dumps({
                        'anthropic_version': 'bedrock-2023-05-31',
                        'max_tokens': model_config['max_tokens'],
                        'temperature': model_config['temperature'],
                        'top_p': model_config['top_p'],
                        'messages': [{'role': 'user', 'content': prompt}]
                    })
                )
                
                response_body = json.loads(response.get('body').read())
                result = response_body['content'][0]['text']
            
            elif 'amazon' in model_config['id']:
                # Amazon models (Titan)
                response = bedrock.invoke_model(
                    modelId=model_config['id'],
                    contentType='application/json',
                    accept='application/json',
                    body=json.dumps({
                        'inputText': prompt,
                        'textGenerationConfig': {
                            'maxTokenCount': model_config['max_tokens'],
                            'temperature': model_config['temperature'],
                            'topP': model_config['top_p']
                        }
                    })
                )
                
                response_body = json.loads(response.get('body').read())
                result = response_body['results'][0]['outputText']
            
            elif 'meta' in model_config['id']:
                # Meta models (Llama)
                response = bedrock.invoke_model(
                    modelId=model_config['id'],
                    contentType='application/json',
                    accept='application/json',
                    body=json.dumps({
                        'prompt': prompt,
                        'max_gen_len': model_config['max_tokens'],
                        'temperature': model_config['temperature'],
                        'top_p': model_config['top_p']
                    })
                )
                
                response_body = json.loads(response.get('body').read())
                result = response_body['generation']
            
            else:
                # Generic handling for other models
                raise ValueError(f"Unsupported model: {model_config['id']}")
        
        else:
            # Handle other providers if needed
            raise ValueError(f"Unsupported provider: {model_config['provider']}")
        
        return {
            'inference_complete': True,
            'result': result,
            'model': model_name,
            'model_id': model_config['id'],
            'data': data
        }
    except Exception as e:
        return {
            'inference_complete': False,
            'error': str(e),
            'model': model_name,
            'data': data
        }