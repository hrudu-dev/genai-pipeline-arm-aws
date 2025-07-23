# Deployment Guide for GenAI Pipeline

This guide provides detailed instructions for deploying the GenAI Pipeline to AWS.

## Deployment Options

The GenAI Pipeline can be deployed in several ways:

1. **Simple Lambda Deployment** - Quick deployment using the `deploy_simple.py` script
2. **Advanced Lambda Deployment** - More configuration options using the `deploy_advanced.py` script
3. **CloudFormation Deployment** - Infrastructure as Code deployment using CloudFormation
4. **Terraform Deployment** - Infrastructure as Code deployment using Terraform
5. **EC2 Deployment** - Deployment to EC2 instances for dedicated compute

This guide focuses on the Simple Lambda Deployment option, which is the quickest way to get started.

## Prerequisites

- AWS Account with access to Amazon Bedrock
- IAM Role for Lambda with Bedrock access
- AWS credentials configured in `.env` file

## Simple Lambda Deployment

### Step 1: Prepare Environment

Ensure your `.env` file is configured with the necessary values:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
PROJECT_NAME=GenAIPipeline
ENVIRONMENT=dev
LAMBDA_ROLE_ARN=arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-bedrock-role
```

### Step 2: Deploy Lambda Function

```bash
# Windows
py deploy_simple.py

# Linux/Mac
python deploy_simple.py
```

This script will:
1. Create a zip package with the Lambda function code
2. Create or update the Lambda function using the role you specified
3. Create a function URL for accessing the Lambda
4. Output the function URL for testing

### Step 3: Test Deployment

Use the function URL provided in the deployment output to test the API:

```bash
# Windows
py test_api.py "What is artificial intelligence?"

# Linux/Mac
python test_api.py "What is artificial intelligence?"
```

## Advanced Lambda Deployment

For more configuration options, use the `deploy_advanced.py` script:

```bash
# Windows
py deploy_advanced.py --memory 512 --timeout 60 --name CustomGenAIPipeline

# Linux/Mac
python deploy_advanced.py --memory 512 --timeout 60 --name CustomGenAIPipeline
```

Options:
- `--memory`: Memory allocation in MB (default: 256)
- `--timeout`: Function timeout in seconds (default: 30)
- `--name`: Function name (default: GenAIPipeline)
- `--region`: AWS region (default: from .env file)
- `--role`: IAM role ARN (default: from .env file)

## CloudFormation Deployment

For a more comprehensive deployment using CloudFormation:

```bash
# Windows
py deploy_cloudformation.py

# Linux/Mac
python deploy_cloudformation.py
```

This will deploy the entire stack including:
- Lambda function
- IAM role and policies
- CloudWatch logs
- Function URL

You can also deploy directly using the AWS CLI:

```bash
aws cloudformation deploy \
  --template-file deploy/one-click-deploy.yaml \
  --stack-name GenAIPipelineStack \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides ProjectName=GenAIPipeline Environment=dev
```

## Terraform Deployment

For deployment using Terraform:

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

## EC2 Deployment

For deployment to EC2 instances:

```bash
# Launch ARM64/Graviton EC2 instance
./scripts/launch-ec2-arm64.sh -k YOUR_KEY_PAIR_NAME -t t4g.medium

# Deploy to existing instance
./scripts/deploy-to-ec2.sh -i PUBLIC_IP -k KEY_PAIR_NAME
```

See [README-EC2.md](README-EC2.md) for more details on EC2 deployment.

## Updating Deployed Function

To update an existing Lambda function:

```bash
# Windows
py deploy_simple.py

# Linux/Mac
python deploy_simple.py
```

The script will detect that the function already exists and update it instead of creating a new one.

## Deleting Deployed Resources

To clean up deployed resources:

```bash
# Windows
py cleanup_aws_resources.py

# Linux/Mac
python cleanup_aws_resources.py
```

This will delete:
- Lambda function
- Function URL configuration
- CloudWatch log group

## Monitoring Deployment

After deployment, you can monitor your Lambda function in the AWS Console:

1. Go to the AWS Lambda Console
2. Find your function (e.g., GenAIPipelineTest2)
3. Click on the "Monitor" tab to view CloudWatch metrics
4. Click on "View logs in CloudWatch" to see detailed logs

## Troubleshooting Deployment

### Lambda Creation Fails

If Lambda creation fails:
- Check that your IAM role has the correct permissions
- Verify that your AWS credentials have permission to create Lambda functions
- Ensure that the role ARN in your .env file is correct

### Function URL Creation Fails

If function URL creation fails:
- Check that your IAM role has permission to create function URLs
- Verify that your AWS credentials have permission to create function URLs

### Invocation Fails

If function invocation fails:
- Check that your IAM role has permission to invoke Bedrock models
- Verify that you have access to Amazon Bedrock
- Check the CloudWatch logs for detailed error messages

## Next Steps

After successful deployment, consider:

1. Setting up API Gateway for more advanced API features
2. Implementing authentication and authorization
3. Setting up CloudWatch alarms for monitoring
4. Implementing request caching for improved performance
5. Deploying to multiple regions for redundancy and lower latency

For more information on these advanced features, see the [README.md](README.md) file.