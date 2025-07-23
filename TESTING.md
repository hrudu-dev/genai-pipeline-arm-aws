# Testing Guide for GenAI Pipeline

This guide provides detailed instructions for testing the GenAI Pipeline locally and in production.

## Testing Options

The GenAI Pipeline can be tested in several ways:

1. **Local Testing** - Test the Bedrock integration locally
2. **API Testing** - Test the deployed Lambda function API
3. **Interactive CLI** - Test using an interactive command-line interface
4. **Web UI** - Test using a simple web interface
5. **Batch Testing** - Test with multiple prompts in parallel

## Prerequisites

- AWS Account with access to Amazon Bedrock
- AWS credentials configured in `.env` file
- Python 3.9 or higher with required packages installed

## Local Testing

Local testing allows you to verify that your AWS credentials have access to Amazon Bedrock without deploying any infrastructure.

### Step 1: Configure Environment

Ensure your `.env` file is configured with the necessary values:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

### Step 2: Run Local Test

```bash
# Windows
py test_local.py

# Linux/Mac
python test_local.py
```

This script will:
1. Load your AWS credentials from the `.env` file
2. Create a Bedrock client
3. Send a test prompt to the Claude AI model
4. Display the response

If successful, you should see a response from the Claude AI model.

## API Testing

After deploying the Lambda function, you can test the API using various methods.

### Using Python Script

```bash
# Windows
py test_api.py "What is artificial intelligence?"

# Linux/Mac
python test_api.py "What is artificial intelligence?"
```

You can customize the prompt by passing it as an argument.

### Using PowerShell

```powershell
Invoke-RestMethod -Uri "https://YOUR_LAMBDA_URL.lambda-url.us-east-1.on.aws/" -Method POST -ContentType "application/json" -Body '{"prompt": "Hello, AI!"}'
```

Replace `YOUR_LAMBDA_URL` with your actual Lambda function URL.

### Using curl (Linux/Mac)

```bash
curl -X POST "https://YOUR_LAMBDA_URL.lambda-url.us-east-1.on.aws/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is artificial intelligence?"}'
```

Replace `YOUR_LAMBDA_URL` with your actual Lambda function URL.

## Interactive CLI

The interactive CLI provides a command-line interface for interacting with the API.

```bash
# Windows
py run_interactive.py

# Linux/Mac
python run_interactive.py
```

This will start an interactive session where you can enter prompts and see responses from the API.

## Web UI

The web UI provides a simple web interface for interacting with the API.

```bash
# Windows
py serve_ui.py

# Linux/Mac
python serve_ui.py
```

This will start a local web server and open a browser with a simple UI for interacting with the API.

## Batch Testing

For testing with multiple prompts in parallel:

```bash
# Windows
py batch_processing.py sample_prompts.txt --workers 5

# Linux/Mac
python batch_processing.py sample_prompts.txt --workers 5
```

This will process all prompts in the specified file in parallel using the specified number of workers.

## Unit Testing

For running unit tests:

```bash
# Windows
py -m pytest tests/ -v

# Linux/Mac
python -m pytest tests/ -v
```

## Performance Testing

For performance testing:

```bash
# Windows
py scripts/performance-test.bat

# Linux/Mac
./scripts/performance-test.sh
```

This will run a series of tests to measure the performance of the API.

## Troubleshooting Tests

### Local Testing Fails

If local testing fails:
- Check that your AWS credentials are correct
- Verify that you have access to Amazon Bedrock
- Ensure that the Claude AI model is available in your region

### API Testing Fails

If API testing fails:
- Check that your Lambda function is deployed correctly
- Verify that the function URL is correct
- Ensure that your Lambda function has permission to invoke Bedrock models

### CORS Issues with Web UI

If you encounter CORS issues when using the web UI:
- Use the interactive CLI instead
- Use the command-line test scripts
- Add CORS headers to your Lambda function URL configuration

## Test Scenarios

Here are some test scenarios to try:

1. **Basic Prompt**: "What is artificial intelligence?"
2. **Complex Prompt**: "Explain the benefits of ARM64 architecture for AI workloads"
3. **Code Generation**: "Write a Python function to calculate the Fibonacci sequence"
4. **Error Handling**: Test with an empty prompt or invalid JSON
5. **Performance**: Test with large prompts or multiple requests in parallel

## Monitoring Test Results

After running tests, you can monitor your Lambda function in the AWS Console:

1. Go to the AWS Lambda Console
2. Find your function (e.g., GenAIPipelineTest2)
3. Click on the "Monitor" tab to view CloudWatch metrics
4. Click on "View logs in CloudWatch" to see detailed logs

## Next Steps

After successful testing, consider:

1. Setting up automated testing with CI/CD
2. Implementing more comprehensive unit tests
3. Setting up performance benchmarks
4. Testing with different AI models
5. Testing with different prompt formats

For more information on these advanced features, see the [README.md](README.md) file.