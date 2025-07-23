# Getting Started with GenAI Pipeline

This guide will help you get started with the GenAI Pipeline quickly and easily.

## Quick Start

### 1. Basic Setup (No Additional Permissions Required)

Run the basic setup script to deploy the Lambda function and start the Web UI:

```bash
python setup_basic.py
```

This will:
- Deploy the Lambda function with ARM64/Graviton optimization
- Start the Web UI for interacting with the API

### 2. Testing the API

You can test the API using the provided test script:

```bash
python test_api.py "What are the benefits of ARM64 architecture?"
```

Or using curl:

```bash
curl -X POST "https://cr7c7lxj5mt2lwvyi57s2o6arq0paars.lambda-url.us-east-1.on.aws/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is artificial intelligence?"}'
```

Or use the Web UI at http://localhost:8000

### 3. Batch Processing

Process multiple prompts in parallel:

```bash
python batch_processing.py sample_prompts.txt
```

## Advanced Features

Some advanced features require additional IAM permissions:

### 1. API Gateway Integration

To set up API Gateway, you need to attach the API Gateway policy to your IAM user:

```bash
python attach_api_policy.py
python api_gateway_setup.py
```

### 2. CloudWatch Monitoring

To set up CloudWatch monitoring, you need CloudWatch permissions:

```bash
python setup_monitoring.py
```

### 3. Multi-Region Deployment

To deploy to multiple regions, you need permissions in those regions:

```bash
python multi_region_deploy.py
```

## Complete Setup

To set up all features at once (requires all permissions):

```bash
python setup_all.py
```

## Troubleshooting

### Permission Issues

If you encounter permission errors, you may need to attach additional policies to your IAM user:

```bash
python attach_api_policy.py
```

### Web UI Issues

If the Web UI doesn't start automatically, you can start it manually:

```bash
python web_ui/server.py
```

Or use the simplified version:

```bash
python simple_web_ui.py
```

### Lambda Deployment Issues

If Lambda deployment fails, check your IAM permissions and AWS credentials in the `.env` file.

## Next Steps

1. Explore the advanced features in the `ADVANCED-FEATURES.md` guide
2. Check the project status in the README
3. Contribute to the project by adding new features or improving existing ones