# Quick Start Guide for GenAI Pipeline

This guide provides the essential steps to get the GenAI Pipeline up and running quickly.

## Prerequisites

- AWS Account with access to Amazon Bedrock
- AWS credentials with appropriate permissions
- Python 3.9 or higher

## Step 1: Install Dependencies

```bash
# Windows
pip install -r requirements.txt

# Linux/Mac
python -m pip install -r requirements.txt
```

## Step 2: Configure AWS Credentials

Create a `.env` file with your AWS credentials:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
PROJECT_NAME=GenAIPipeline
ENVIRONMENT=dev
LAMBDA_ROLE_ARN=arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-bedrock-role
```

## Step 3: Test Local Access

Test that your credentials can access Amazon Bedrock:

```bash
# Windows
py test_local.py

# Linux/Mac
python test_local.py
```

## Step 4: Deploy Lambda Function

Deploy the Lambda function to AWS:

```bash
# Windows
py deploy_simple.py

# Linux/Mac
python deploy_simple.py
```

## Step 5: Test Deployed API

Test the deployed API using the provided test script:

```bash
# Windows
py test_api.py "What is artificial intelligence?"

# Linux/Mac
python test_api.py "What is artificial intelligence?"
```

## Step 6: Use Interactive CLI

Use the interactive CLI for a better testing experience:

```bash
# Windows
py run_interactive.py

# Linux/Mac
python run_interactive.py
```

## Step 7: Use Web UI

Use the web UI for a graphical interface:

```bash
# Windows
py serve_ui.py

# Linux/Mac
python serve_ui.py
```

## Current Deployment

The project is currently deployed with the following resources:

- **Lambda Function**: GenAIPipelineTest2
- **Function URL**: https://btjml6cwvtetuz4mraonqwyqbq0aeotc.lambda-url.us-east-1.on.aws/
- **Region**: us-east-1

## Testing the API Directly

### Using PowerShell

```powershell
Invoke-RestMethod -Uri "https://btjml6cwvtetuz4mraonqwyqbq0aeotc.lambda-url.us-east-1.on.aws/" -Method POST -ContentType "application/json" -Body '{"prompt": "Hello, AI!"}'
```

### Using curl (Linux/Mac)

```bash
curl -X POST "https://btjml6cwvtetuz4mraonqwyqbq0aeotc.lambda-url.us-east-1.on.aws/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is artificial intelligence?"}'
```

## Next Steps

For more detailed information, see:

- [README.md](README.md) - Project overview
- [GETTING-STARTED.md](GETTING-STARTED.md) - Detailed setup instructions
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment options
- [TESTING.md](TESTING.md) - Testing instructions