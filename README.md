# GenAI Pipeline

A scalable and modular GenAI pipeline on AWS with Bedrock integration.

## Features
- ✅ **Bedrock Integration**: Claude AI model inference
- ✅ **Lambda Functions**: Serverless data processing and inference
- ✅ **Local Testing**: Test pipeline components locally
- ✅ **AWS Deployment**: Automated deployment scripts
- ✅ **Resource Management**: Automated tagging and resource groups

## Quick Start

### 1. Setup AWS CLI
```cmd
scripts\setup-aws.bat
```

### 2. Test Locally
```cmd
pip install -r requirements.txt
python src\main.py
python -m pytest tests\
```

### 3. Deploy to AWS
```cmd
scripts\deploy.bat
```

### 4. Test API
**Function URL**: `https://2fu2iveexbqvfe74qqehldjeky0urivd.lambda-url.us-east-1.on.aws/`

```powershell
$body = @{prompt = "What is AI?"} | ConvertTo-Json
Invoke-RestMethod -Uri "https://2fu2iveexbqvfe74qqehldjeky0urivd.lambda-url.us-east-1.on.aws/" -Method POST -Body $body -ContentType "application/json"
```

## Architecture
- **AWS Lambda**: Serverless inference with Bedrock
- **Amazon Bedrock**: Claude AI model
- **S3**: Data and artifact storage
- **IAM**: Secure access management
- **Resource Groups**: Organized resource management

## Project Structure
- `src/` – Python source code
- `infra/` – CloudFormation templates
- `scripts/` – Deployment and testing scripts
- `tests/` – Unit tests
- `docs/` – Documentation

## Status
✅ **Working**: Local testing, Bedrock integration, Lambda deployment  
🔧 **In Progress**: CloudFormation stack deployment  
📋 **Next**: API Gateway integration