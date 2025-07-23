# Testing the GenAI Pipeline

This document provides instructions for testing the GenAI Pipeline locally and in production.

## Prerequisites

1. Python 3.8+ installed
2. AWS CLI configured with appropriate credentials
3. Access to AWS Bedrock and Claude 3 Haiku model

## Quick Test

Run the comprehensive test script:

```bash
python run_test.py
```

This script will:
1. Check your environment setup
2. Test local inference functionality
3. Test the deployed API endpoint (if available)

## Manual Testing Steps

### 1. Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials (if not already done)
# Edit .env with your AWS credentials

# Run local test
python test_local.py
```

### 2. API Testing

For Windows:
```bash
test_api.bat
```

For Unix/Linux:
```bash
curl -X POST "https://2fu2iveexbqvfe74qqehldjeky0urivd.lambda-url.us-east-1.on.aws/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is artificial intelligence?"}'
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Ensure AWS credentials are correctly configured
   - Check that your AWS account has access to Bedrock

2. **Model Access Issues**:
   - Verify that your AWS account has access to Claude 3 Haiku model
   - Check that you're using a region where Bedrock is available

3. **Dependency Issues**:
   - Make sure all dependencies are installed: `pip install -r requirements.txt`

4. **API Endpoint Not Responding**:
   - Verify that the Lambda function is deployed
   - Check if the function URL is correct

## Running Unit Tests

```bash
python -m pytest tests/ -v
```