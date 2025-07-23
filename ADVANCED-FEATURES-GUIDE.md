# Advanced Features Guide

This guide provides detailed instructions for using the advanced features of the GenAI Pipeline.

## Table of Contents

1. [Custom Domain Name](#custom-domain-name)
2. [Request Caching](#request-caching)
3. [Authentication and Authorization](#authentication-and-authorization)

## Custom Domain Name

Adding a custom domain name to your API Gateway makes it more professional and easier to remember.

### Prerequisites

1. A registered domain name
2. An SSL certificate in AWS Certificate Manager (ACM)

### Setup

```bash
python setup_custom_domain.py --domain api.example.com --cert-arn YOUR_CERT_ARN --api-id YOUR_API_ID
```

Parameters:
- `--domain`, `-d`: Your custom domain name (e.g., api.example.com)
- `--cert-arn`, `-c`: ARN of your SSL certificate in ACM
- `--api-id`, `-a`: ID of your API Gateway API

### DNS Configuration

After setting up the custom domain name, you need to create a CNAME record in your DNS provider:

1. Go to your DNS provider's website
2. Create a CNAME record pointing your domain to the distribution domain name provided by the script
3. Wait for DNS propagation (may take up to 24 hours)

### Testing

Once DNS propagation is complete, you can test your API using the custom domain name:

```bash
curl -X POST "https://api.example.com/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is artificial intelligence?"}'
```

## Request Caching

Implementing caching for common requests can improve performance and reduce costs.

### Setup

1. Create the DynamoDB cache table:

```bash
python setup_cache.py
```

2. Deploy the Lambda function with caching:

```bash
python deploy_simple.py --function lambda_function_cached.py
```

### Configuration

You can configure the caching behavior using environment variables:

- `ENABLE_CACHE`: Set to "true" to enable caching (default: "true")
- `CACHE_TTL`: Cache time-to-live in seconds (default: 3600)
- `CACHE_TABLE_NAME`: Name of the DynamoDB cache table (default: "GenAIPipelineCache")

### Monitoring

You can monitor the cache performance using CloudWatch metrics:

- Cache hits and misses are logged to CloudWatch Logs
- You can create CloudWatch Dashboards to visualize cache performance

## Authentication and Authorization

Adding authentication and authorization to your API improves security and allows you to control access.

### API Key Authentication

1. Set up API key authentication:

```bash
python setup_auth.py --api-id YOUR_API_ID --auth-type api-key
```

2. Test the API with API key authentication:

```bash
python test_auth_api.py --api-url YOUR_API_URL --auth-type api-key --api-key YOUR_API_KEY
```

### Cognito Authentication

1. Set up Cognito authentication:

```bash
python setup_auth.py --api-id YOUR_API_ID --auth-type cognito
```

2. Create a user in the Cognito user pool:

```bash
aws cognito-idp admin-create-user \
  --user-pool-id YOUR_USER_POOL_ID \
  --username user@example.com \
  --temporary-password Temp123! \
  --user-attributes Name=email,Value=user@example.com
```

3. Test the API with Cognito authentication:

```bash
python test_auth_api.py \
  --api-url YOUR_API_URL \
  --auth-type cognito \
  --user-pool-id YOUR_USER_POOL_ID \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET \
  --username user@example.com \
  --password YOUR_PASSWORD
```

### Usage Plans and Quotas

API Gateway usage plans allow you to control access to your API:

- Rate limiting: Limit the number of requests per second
- Quotas: Limit the total number of requests per day, week, or month

The `setup_auth.py` script creates a usage plan with the following defaults:
- Rate limit: 10 requests per second
- Burst limit: 20 requests
- Quota: 1000 requests per month

You can modify these values in the script to suit your needs.