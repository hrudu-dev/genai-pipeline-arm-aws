# Advanced Features Guide - Part 2

This guide provides detailed instructions for using the additional advanced features of the GenAI Pipeline.

## Table of Contents

1. [CI/CD Pipeline](#cicd-pipeline)
2. [Cost Optimization](#cost-optimization)
3. [Cache Monitoring](#cache-monitoring)
4. [Rate Limiting](#rate-limiting)
5. [Multi-Model Support](#multi-model-support)

## CI/CD Pipeline

The CI/CD pipeline automates the testing and deployment of the GenAI Pipeline using GitHub Actions.

### Setup

1. Create a GitHub repository for your project:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/genai-pipeline.git
git push -u origin main
```

2. Add GitHub repository secrets:
   - Go to your GitHub repository
   - Navigate to Settings > Secrets and variables > Actions
   - Add the following secrets:
     - `AWS_ACCESS_KEY_ID`: Your AWS access key
     - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

3. The workflow will automatically run when you push to the main branch.

### Workflow

The CI/CD pipeline includes the following jobs:

1. **Test**: Run unit tests to ensure the code is working correctly
2. **Deploy Lambda**: Deploy the Lambda function to AWS
3. **Deploy Cache**: Set up the DynamoDB cache table and deploy the cached Lambda function
4. **Deploy Multi-Region**: Deploy the Lambda function to multiple regions (manual trigger only)

### Manual Trigger

You can manually trigger the workflow:

1. Go to your GitHub repository
2. Navigate to Actions
3. Select the "Deploy GenAI Pipeline" workflow
4. Click "Run workflow"

## Cost Optimization

The cost optimization tools help you optimize your Lambda function for cost and performance.

### Lambda Optimization

```bash
python optimize_lambda.py --function YOUR_FUNCTION_NAME --memory 256 --timeout 30
```

Parameters:
- `--function`, `-f`: Lambda function name
- `--memory`, `-m`: Memory size in MB (128-10240)
- `--timeout`, `-t`: Timeout in seconds (1-900)
- `--provisioned-concurrency`, `-p`: Provisioned concurrency

### Cost Estimates

The script provides cost estimates for your Lambda function:

- Cost per invocation
- Cost per 1M invocations
- Provisioned concurrency cost per hour
- Provisioned concurrency cost per month

### Memory Optimization

Finding the optimal memory size for your Lambda function is crucial for cost optimization:

1. Start with a low memory size (e.g., 128 MB)
2. Gradually increase the memory size and measure the performance
3. Find the sweet spot where the cost-performance ratio is optimal

## Cache Monitoring

The cache monitoring tools help you monitor the performance of your DynamoDB cache.

### Setup

```bash
python setup_cache_monitoring.py --function YOUR_FUNCTION_NAME
```

Parameters:
- `--function`, `-f`: Lambda function name
- `--table`, `-t`: DynamoDB table name

### Dashboard

The CloudWatch dashboard includes the following metrics:

- Lambda Invocations
- Lambda Duration
- DynamoDB Consumed Capacity
- DynamoDB Latency
- Cache Hit/Miss Ratio

### Metric Filters

The script creates a metric filter for cache hits and misses, allowing you to track the cache performance over time.

## Rate Limiting

The rate limiting tools help you control access to your API and prevent abuse.

### Setup

```bash
python setup_rate_limiting.py --api-id YOUR_API_ID --rate-limit 10 --quota-limit 1000
```

Parameters:
- `--api-id`, `-a`: API Gateway ID
- `--rate-limit`, `-r`: Rate limit (requests per second)
- `--burst-limit`, `-b`: Burst limit (requests)
- `--quota-limit`, `-q`: Quota limit (requests)
- `--quota-period`, `-p`: Quota period (DAY, WEEK, MONTH)

### Usage Plans

The script creates a usage plan with the following settings:

- Rate limit: Maximum number of requests per second
- Burst limit: Maximum number of concurrent requests
- Quota limit: Maximum number of requests per period
- Quota period: Time period for the quota (day, week, month)

### API Keys

The script creates an API key and adds it to the usage plan, allowing you to control access to your API.

## Multi-Model Support

The multi-model support allows you to use multiple AI models for inference.

### Available Models

The following models are available:

- `claude-haiku`: Anthropic Claude 3 Haiku
- `claude-sonnet`: Anthropic Claude 3 Sonnet
- `claude-opus`: Anthropic Claude 3 Opus
- `titan-text`: Amazon Titan Text
- `llama3`: Meta Llama 3

### Usage

To use a specific model, include the `model` parameter in your request:

```json
{
  "prompt": "What is artificial intelligence?",
  "model": "claude-haiku"
}
```

### Model Comparison

You can compare multiple models using the `test_multi_model.py` script:

```bash
python test_multi_model.py --compare
```

Parameters:
- `--prompt`, `-p`: Prompt to send to the API
- `--model`, `-m`: Model to test (omit to compare all models)
- `--compare`, `-c`: Compare multiple models

### Custom Models

You can add custom models by updating the `MODELS` dictionary in the `multi_model.py` file:

```python
MODELS = {
    'custom-model': {
        'id': 'provider.model-id',
        'provider': 'bedrock',
        'max_tokens': 500,
        'temperature': 0.7,
        'top_p': 0.9
    },
    # ...
}
```