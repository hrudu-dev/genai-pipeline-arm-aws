# Advanced Features Guide

This guide provides detailed instructions for using the advanced features of the GenAI Pipeline.

## Table of Contents

1. [API Gateway Integration](#api-gateway-integration)
2. [Batch Processing](#batch-processing)
3. [CloudWatch Monitoring](#cloudwatch-monitoring)
4. [Multi-Region Deployment](#multi-region-deployment)
5. [Web UI](#web-ui)

## API Gateway Integration

API Gateway provides enhanced API management capabilities, including authentication, rate limiting, and custom domains.

### Setup

```bash
python api_gateway_setup.py
```

This script will:
- Create a new REST API in API Gateway
- Create a resource and method for the API
- Integrate the API with your Lambda function
- Deploy the API to a "prod" stage
- Configure CORS for the API

### Benefits

- **Authentication**: Add API keys or OAuth authentication
- **Rate Limiting**: Control the number of requests per second
- **Custom Domain**: Use your own domain name for the API
- **Usage Plans**: Create usage plans for different users
- **API Documentation**: Generate API documentation

### Customization

You can customize the API Gateway setup by modifying the `api_gateway_setup.py` script:

- Change the API name
- Add more resources and methods
- Configure different authentication methods
- Add request/response mapping templates

## Batch Processing

The batch processing feature allows you to process multiple prompts in parallel, improving throughput and efficiency.

### Usage

```bash
python batch_processing.py sample_prompts.txt --output results.json --workers 5
```

Parameters:
- `file`: File containing prompts (one per line)
- `--output`, `-o`: Output file for results (default: input_file.results.json)
- `--workers`, `-w`: Maximum number of concurrent workers (default: 5)

### Sample Prompts File

Create a text file with one prompt per line:

```
What is artificial intelligence?
Explain quantum computing in simple terms.
What are the benefits of ARM64 architecture?
```

### Results

The results are saved as a JSON file with the following structure:

```json
[
  {
    "prompt": "What is artificial intelligence?",
    "result": "Artificial intelligence (AI) refers to...",
    "success": true
  },
  {
    "prompt": "Explain quantum computing in simple terms.",
    "result": "Quantum computing is a type of computing...",
    "success": true
  }
]
```

## CloudWatch Monitoring

CloudWatch monitoring provides insights into the performance and usage of your GenAI Pipeline.

### Setup

```bash
python setup_monitoring.py
```

This script will:
- Create a CloudWatch dashboard for your Lambda function
- Add widgets for invocations, duration, errors, and concurrent executions
- Create alarms for errors and high duration

### Dashboard

The dashboard includes the following metrics:
- **Lambda Invocations**: Number of function invocations
- **Lambda Duration**: Average and maximum function duration
- **Lambda Errors**: Number of function errors
- **Lambda Concurrent Executions**: Number of concurrent executions

### Alarms

The script creates the following alarms:
- **Error Alarm**: Triggers when the function has errors
- **Duration Alarm**: Triggers when the function duration exceeds 5 seconds

## Multi-Region Deployment

Multi-region deployment improves redundancy and reduces latency for users in different geographic locations.

### Setup

```bash
python multi_region_deploy.py
```

This script will:
- Deploy your Lambda function to multiple AWS regions
- Create function URLs in each region
- Save the deployment information to a JSON file

### Regions

By default, the script deploys to the following regions:
- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- eu-west-1 (Ireland)

You can customize the regions by modifying the `REGIONS` list in the script.

### Results

The deployment information is saved to `multi_region_deployment.json`:

```json
[
  {
    "region": "us-east-1",
    "function_arn": "arn:aws:lambda:us-east-1:123456789012:function:GenAIPipelineMultiRegion",
    "function_url": "https://abcdefg.lambda-url.us-east-1.on.aws/"
  },
  {
    "region": "us-west-2",
    "function_arn": "arn:aws:lambda:us-west-2:123456789012:function:GenAIPipelineMultiRegion",
    "function_url": "https://hijklmn.lambda-url.us-west-2.on.aws/"
  }
]
```

## Web UI

The Web UI provides a simple interface for interacting with the GenAI Pipeline API.

### Setup

```bash
python web_ui/server.py
```

This will start a local HTTP server and open the Web UI in your default browser.

### Features

- **Simple Interface**: Easy-to-use interface for entering prompts
- **Real-time Responses**: See responses as they are generated
- **Token Estimation**: Approximate token count for prompts and responses
- **Response Time**: Track how long each request takes

### Customization

You can customize the Web UI by modifying the `web_ui/index.html` file:
- Change the styling
- Add more features
- Integrate with other APIs

### Deployment

To deploy the Web UI to a production environment, you can:
- Host it on Amazon S3
- Deploy it to a web server
- Use a static site hosting service

Example S3 deployment:

```bash
aws s3 sync web_ui/ s3://your-bucket-name/ --acl public-read
```