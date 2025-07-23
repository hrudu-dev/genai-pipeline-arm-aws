# Setting Up IAM for GenAI Pipeline Testing

This guide will help you create an IAM user and the necessary policies for testing the GenAI Pipeline.

## Step 1: Create the Lambda Execution Role

First, create the role that the Lambda function will use:

```bash
# Create the Lambda execution role
aws iam create-role \
    --role-name lambda-bedrock-role \
    --assume-role-policy-document file://iam/lambda-trust-policy.json

# Attach the execution policy to the role
aws iam put-role-policy \
    --role-name lambda-bedrock-role \
    --policy-name lambda-bedrock-execution \
    --policy-document file://iam/lambda-execution-role-policy.json
```

## Step 2: Create a Policy for Testing

Create a policy that grants permissions for testing the GenAI Pipeline:

```bash
# Create the test policy
aws iam create-policy \
    --policy-name GenAIPipelineTestPolicy \
    --policy-document file://iam/genai-pipeline-test-policy.json
```

Note the ARN of the created policy, which will look like:
`arn:aws:iam::123456789012:policy/GenAIPipelineTestPolicy`

## Step 3: Create an IAM User for Testing

Create a dedicated IAM user for testing:

```bash
# Create the user
aws iam create-user --user-name genai-pipeline-tester

# Attach the test policy to the user
aws iam attach-user-policy \
    --user-name genai-pipeline-tester \
    --policy-arn arn:aws:iam::ACCOUNT_ID:policy/GenAIPipelineTestPolicy

# Create access keys for the user
aws iam create-access-key --user-name genai-pipeline-tester
```

Make sure to save the `AccessKeyId` and `SecretAccessKey` from the output.

## Step 4: Configure AWS Credentials

Update your `.env` file with the new credentials:

```
AWS_ACCESS_KEY_ID=your_new_access_key
AWS_SECRET_ACCESS_KEY=your_new_secret_key
AWS_DEFAULT_REGION=us-east-1
```

## Step 5: Verify Bedrock Access

Ensure your AWS account has access to Amazon Bedrock and the Claude 3 Haiku model:

1. Go to the AWS Console
2. Navigate to Amazon Bedrock
3. Click on "Model access"
4. Request access to "Claude 3 Haiku" if not already granted

## Using the AWS Console Instead of CLI

If you prefer using the AWS Console:

### Create the Lambda Execution Role

1. Go to IAM > Roles > Create role
2. Select "AWS service" and "Lambda"
3. Click "Next: Permissions"
4. Create a new policy using the JSON in `lambda-execution-role-policy.json`
5. Name the role "lambda-bedrock-role"

### Create the Test Policy

1. Go to IAM > Policies > Create policy
2. Switch to the JSON editor
3. Paste the contents of `genai-pipeline-test-policy.json`
4. Name the policy "GenAIPipelineTestPolicy"

### Create the Test User

1. Go to IAM > Users > Add users
2. Name the user "genai-pipeline-tester"
3. Enable "Access key - Programmatic access"
4. Attach the "GenAIPipelineTestPolicy" directly
5. Complete the user creation
6. Download or copy the access key and secret key