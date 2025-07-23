#!/usr/bin/env python3
"""
Set up API Gateway integration for GenAI Pipeline
"""

import boto3
import json

# Hardcoded credentials - only for testing
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

# Lambda function name
LAMBDA_FUNCTION_NAME = "GenAIPipelineTest2"

def create_api_gateway():
    """Create API Gateway for Lambda function"""
    print("Creating API Gateway...")
    
    # Create API Gateway client
    apigateway = boto3.client('apigateway',
                            region_name=AWS_DEFAULT_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Create Lambda client
    lambda_client = boto3.client('lambda',
                               region_name=AWS_DEFAULT_REGION,
                               aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Get Lambda function ARN
    lambda_response = lambda_client.get_function(FunctionName=LAMBDA_FUNCTION_NAME)
    lambda_arn = lambda_response['Configuration']['FunctionArn']
    
    # Create REST API
    api_response = apigateway.create_rest_api(
        name='GenAIPipelineAPI',
        description='API for GenAI Pipeline',
        endpointConfiguration={
            'types': ['REGIONAL']
        }
    )
    
    api_id = api_response['id']
    print(f"Created API Gateway: {api_id}")
    
    # Get root resource ID
    resources = apigateway.get_resources(restApiId=api_id)
    root_id = [resource for resource in resources['items'] if resource['path'] == '/'][0]['id']
    
    # Create resource
    resource_response = apigateway.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='inference'
    )
    resource_id = resource_response['id']
    
    # Create POST method
    apigateway.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        authorizationType='NONE',
        apiKeyRequired=False
    )
    
    # Create integration with Lambda
    apigateway.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{AWS_DEFAULT_REGION}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
    )
    
    # Create method response
    apigateway.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        statusCode='200',
        responseModels={
            'application/json': 'Empty'
        }
    )
    
    # Create integration response
    apigateway.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        statusCode='200',
        responseTemplates={
            'application/json': ''
        }
    )
    
    # Add OPTIONS method for CORS
    apigateway.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )
    
    # Add integration for OPTIONS
    apigateway.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        type='MOCK',
        requestTemplates={
            'application/json': '{"statusCode": 200}'
        }
    )
    
    # Add method response for OPTIONS
    apigateway.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': True,
            'method.response.header.Access-Control-Allow-Methods': True,
            'method.response.header.Access-Control-Allow-Origin': True
        },
        responseModels={
            'application/json': 'Empty'
        }
    )
    
    # Add integration response for OPTIONS
    apigateway.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
            'method.response.header.Access-Control-Allow-Methods': "'GET,POST,OPTIONS'",
            'method.response.header.Access-Control-Allow-Origin': "'*'"
        },
        responseTemplates={
            'application/json': ''
        }
    )
    
    # Deploy API
    deployment = apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )
    
    # Add Lambda permission
    try:
        lambda_client.add_permission(
            FunctionName=LAMBDA_FUNCTION_NAME,
            StatementId=f'apigateway-prod-{api_id}',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:{AWS_DEFAULT_REGION}:{lambda_response["Configuration"]["FunctionArn"].split(":")[4]}:{api_id}/*/*/inference'
        )
    except lambda_client.exceptions.ResourceConflictException:
        print("Lambda permission already exists")
    
    # Get API URL
    api_url = f'https://{api_id}.execute-api.{AWS_DEFAULT_REGION}.amazonaws.com/prod/inference'
    print(f"API Gateway URL: {api_url}")
    
    return api_url

if __name__ == "__main__":
    create_api_gateway()