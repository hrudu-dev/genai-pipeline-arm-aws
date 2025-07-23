# Testing the GenAI Pipeline with IAM Setup

This guide will help you test the GenAI Pipeline after setting up the necessary IAM resources.

## Step 1: Set Up IAM Resources

First, create the necessary IAM resources:

```bash
# Windows
iam\setup-iam.bat

# Python (cross-platform)
python iam/setup-iam.py
```

This will create:
- A Lambda execution role (`lambda-bedrock-role`)
- A test policy (`GenAIPipelineTestPolicy`)
- A test user (`genai-pipeline-tester`) with access keys

## Step 2: Configure AWS Credentials

Update your `.env` file with the access keys generated in Step 1:

```
AWS_ACCESS_KEY_ID=your_generated_access_key
AWS_SECRET_ACCESS_KEY=your_generated_secret_key
AWS_DEFAULT_REGION=us-east-1
```

## Step 3: Test Locally

Run the local test to verify that your credentials work:

```bash
python test_local.py
```

If successful, you should see a response from the Claude AI model.

## Step 4: Deploy Lambda Function

Deploy the Lambda function to AWS:

```bash
# Windows
scripts\deploy.bat

# Python (cross-platform)
python setup.py
```

## Step 5: Test API Endpoint

Test the deployed API endpoint:

```bash
python run_test.py
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify that your access keys are correctly set in the `.env` file
   - Check that the IAM user has the necessary permissions

2. **Bedrock Access Issues**:
   - Ensure your AWS account has access to Amazon Bedrock
   - Request access to the Claude 3 Haiku model if needed

3. **Lambda Deployment Issues**:
   - Check that the Lambda execution role exists
   - Verify that the IAM user has permission to create Lambda functions

### Requesting Bedrock Access

If you don't have access to Amazon Bedrock:

1. Go to the AWS Console
2. Navigate to Amazon Bedrock
3. Click on "Model access"
4. Request access to "Claude 3 Haiku"

### Verifying IAM Permissions

To verify that your IAM user has the necessary permissions:

```bash
# List attached policies
aws iam list-attached-user-policies --user-name genai-pipeline-tester

# Verify Lambda role
aws iam get-role --role-name lambda-bedrock-role
```