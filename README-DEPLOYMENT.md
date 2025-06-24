# GenAI Pipeline - Deployment Guide

## Quick Start

### 1. Setup AWS CLI
```cmd
scripts\setup-aws.bat
```
This will:
- Check AWS CLI installation
- Configure your AWS credentials
- Create S3 bucket for artifacts
- Verify your setup

### 2. Build and Deploy
```cmd
scripts\deploy.bat
```
This will:
- Install dependencies
- Run tests
- Package the application
- Deploy infrastructure to AWS
- Set up resource tagging

### 3. Test the API
```cmd
scripts\test-api.bat
```

## Manual Steps

### Build Only
```cmd
scripts\build.bat
```

### Deploy Infrastructure Only
```cmd
aws cloudformation deploy --template-file infra\cloudformation\pipeline.yaml --stack-name GenAIPipelineStack --capabilities CAPABILITY_IAM
```

### Clean Up Resources
```cmd
scripts\cleanup.bat
```

## Environment Configuration

Copy `.env.example` to `.env` and customize:
```
AWS_PROFILE=default
AWS_REGION=us-east-1
PROJECT_NAME=GenAIPipeline
ENVIRONMENT=dev
```

## Architecture Deployed

- **Lambda Functions**: Data processing and inference on Graviton
- **API Gateway**: REST API for inference requests
- **S3 Buckets**: Data storage and artifacts
- **IAM Roles**: Secure access to AWS services
- **Resource Groups**: Organized resource management
- **CloudWatch**: Monitoring and logging

## API Usage

POST to the deployed endpoint:
```json
{
  "prompt": "What is artificial intelligence?"
}
```

Response:
```json
{
  "inference_complete": true,
  "result": "AI response here...",
  "data": {...}
}
```