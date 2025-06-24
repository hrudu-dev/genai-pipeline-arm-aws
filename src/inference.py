import json
import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# FastAPI app for EC2 deployment
app = FastAPI(title="GenAI Pipeline", description="ARM64/Graviton optimized GenAI Pipeline")

class InferenceRequest(BaseModel):
    prompt: str

class InferenceResponse(BaseModel):
    inference_complete: bool
    result: str = None
    error: str = None
    data: dict = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "architecture": "ARM64", "service": "GenAI Pipeline"}

@app.post("/", response_model=InferenceResponse)
async def inference_endpoint(request: InferenceRequest):
    try:
        result = run_inference({"prompt": request.prompt})
        return InferenceResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_inference(data):
    """Run GenAI model inference on processed data."""
    try:
        bedrock = boto3.client('bedrock-runtime')
        
        # Prepare prompt
        prompt = data.get('prompt', 'Hello, how can I help you?')
        
        # Call Bedrock model
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
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

def lambda_handler(event, context):
    """AWS Lambda handler for model inference."""
    try:
        # Handle both API Gateway and Function URL formats
        if 'body' in event:
            data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            data = event
        
        # Run inference
        result = run_inference(data)
        
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