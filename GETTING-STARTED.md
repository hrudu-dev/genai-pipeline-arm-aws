# Getting Started with GenAI Pipeline

This guide provides detailed instructions for setting up and deploying the GenAI Pipeline project.

## Prerequisites

- AWS Account with access to Amazon Bedrock
- AWS CLI installed and configured
- Python 3.9 or higher
- Basic knowledge of AWS services (Lambda, IAM)

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/genai-pipeline-arm-aws.git
cd genai-pipeline-arm-aws
```

## Step 2: Install Dependencies

```bash
# Windows
pip install -r requirements.txt

# Linux/Mac
python -m pip install -r requirements.txt
```

## Step 3: Configure AWS Credentials

1. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your AWS credentials:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
PROJECT_NAME=GenAIPipeline
ENVIRONMENT=dev
```

## Step 4: Create IAM Role for Lambda

### Option 1: Manual Setup (Recommended)

1. Go to the AWS Management Console
2. Navigate to IAM (Identity and Access Management)
3. In the left navigation pane, click on "Roles"
4. Click the "Create role" button
5. Select "AWS service" as the trusted entity type
6. Under "Use case", select "Lambda"
7. Click "Next: Permissions"
8. Search for and select "AWSLambdaBasicExecutionRole"
9. Click "Next: Tags" (add tags if desired)
10. Click "Next: Review"
11. Name the role "lambda-bedrock-role"
12. Add a description like "Role for Lambda function to access Bedrock"
13. Click "Create role"
14. Find and click on the newly created "lambda-bedrock-role" in the roles list
15. Click on the "Permissions" tab
16. Click "Add permissions" and select "Create inline policy"
17. Click on the "JSON" tab
18. Paste the following policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "*"
        }
    ]
}
```

19. Click "Review policy"
20. Name the policy "bedrock-access"
21. Click "Create policy"
22. Copy the Role ARN from the role summary page

### Option 2: Using AWS CLI

If you have sufficient permissions, you can create the role using AWS CLI:

```bash
# Create trust policy file
echo '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}' > trust-policy.json

# Create the role
aws iam create-role --role-name lambda-bedrock-role --assume-role-policy-document file://trust-policy.json

# Attach Lambda basic execution policy
aws iam attach-role-policy --role-name lambda-bedrock-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Create Bedrock policy
echo '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "*"
        }
    ]
}' > bedrock-policy.json

# Attach Bedrock policy
aws iam put-role-policy --role-name lambda-bedrock-role --policy-name bedrock-access --policy-document file://bedrock-policy.json

# Get the role ARN
aws iam get-role --role-name lambda-bedrock-role --query Role.Arn --output text
```

## Step 5: Update .env File with Role ARN

Add the role ARN to your `.env` file:

```
LAMBDA_ROLE_ARN=arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-bedrock-role
```

## Step 6: Test Local Access to Bedrock

```bash
# Windows
py test_local.py

# Linux/Mac
python test_local.py
```

If successful, you should see a response from the Claude AI model.

## Step 7: Deploy Lambda Function

```bash
# Windows
py deploy_simple.py

# Linux/Mac
python deploy_simple.py
```

This will:
1. Create a zip package with the Lambda function code
2. Create or update the Lambda function using the role you created
3. Create a function URL for accessing the Lambda
4. Output the function URL for testing

## Step 8: Test Deployed API

### Using Python Script

```bash
# Windows
py test_api.py "What is artificial intelligence?"

# Linux/Mac
python test_api.py "What is artificial intelligence?"
```

### Using PowerShell

```powershell
Invoke-RestMethod -Uri "https://YOUR_LAMBDA_URL.lambda-url.us-east-1.on.aws/" -Method POST -ContentType "application/json" -Body '{"prompt": "Hello, AI!"}'
```

### Using curl (Linux/Mac)

```bash
curl -X POST "https://YOUR_LAMBDA_URL.lambda-url.us-east-1.on.aws/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is artificial intelligence?"}'
```

## Step 9: Use Interactive CLI

```bash
# Windows
py run_interactive.py

# Linux/Mac
python run_interactive.py
```

This provides a command-line interface for interacting with the API.

## Step 10: Use Web UI

```bash
# Windows
py serve_ui.py

# Linux/Mac
python serve_ui.py
```

This starts a local web server and opens a browser with a simple UI for interacting with the API.

## Troubleshooting

### CORS Issues with Web UI

If you encounter CORS issues when using the web UI, you can:

1. Use the interactive CLI instead
2. Use the command-line test scripts
3. Add CORS headers to your Lambda function URL configuration

### Permission Issues

If you encounter permission issues:

1. Check that your IAM role has the correct policies attached
2. Verify that your AWS credentials have permission to create and invoke Lambda functions
3. Ensure that you have access to Amazon Bedrock

### Lambda Deployment Issues

If Lambda deployment fails:

1. Check that your AWS credentials are correct
2. Verify that the role ARN in your .env file is correct
3. Ensure that you have permission to create Lambda functions

## Next Steps

- Explore advanced features like API Gateway integration, batch processing, and multi-region deployment
- Optimize Lambda function for cost and performance
- Add authentication and authorization to your API
- Set up monitoring and alerting

For more information, see the [README.md](README.md) file.