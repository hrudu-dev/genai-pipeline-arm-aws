# Current Deployment Information

This document contains information about the current deployment of the GenAI Pipeline.

## Deployment Details

| Resource | Value |
|----------|-------|
| **Lambda Function Name** | GenAIPipelineTest2 |
| **Function URL** | https://btjml6cwvtetuz4mraonqwyqbq0aeotc.lambda-url.us-east-1.on.aws/ |
| **AWS Region** | us-east-1 |
| **IAM Role** | lambda-bedrock-role |
| **Architecture** | arm64 (AWS Graviton) |
| **Runtime** | Python 3.9 |
| **Memory** | 256 MB |
| **Timeout** | 30 seconds |
| **Model** | anthropic.claude-3-haiku-20240307-v1:0 |

## Testing the Deployment

### Using Python

```python
import requests

url = "https://btjml6cwvtetuz4mraonqwyqbq0aeotc.lambda-url.us-east-1.on.aws/"
headers = {"Content-Type": "application/json"}
data = {"prompt": "What is artificial intelligence?"}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

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

### Using the Provided Scripts

```bash
# Windows
py test_api.py "What is artificial intelligence?"
py run_interactive.py
py serve_ui.py

# Linux/Mac
python test_api.py "What is artificial intelligence?"
python run_interactive.py
python serve_ui.py
```

## Monitoring

You can monitor the Lambda function in the AWS Console:

1. Go to the AWS Lambda Console
2. Find the function "GenAIPipelineTest2"
3. Click on the "Monitor" tab to view CloudWatch metrics
4. Click on "View logs in CloudWatch" to see detailed logs

## Updating the Deployment

To update the Lambda function:

```bash
# Windows
py deploy_simple.py

# Linux/Mac
python deploy_simple.py
```

## Cleaning Up

To delete the Lambda function and associated resources:

```bash
# Windows
py cleanup_aws_resources.py

# Linux/Mac
python cleanup_aws_resources.py
```

## Notes

- The function URL is publicly accessible with no authentication
- The Lambda function uses the Claude 3 Haiku model from Anthropic via AWS Bedrock
- The function is optimized for ARM64/Graviton architecture for cost savings
- The function has CORS headers enabled for web access