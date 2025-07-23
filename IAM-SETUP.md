# IAM Setup Guide for GenAI Pipeline

This guide provides detailed instructions for setting up the necessary IAM roles and policies for the GenAI Pipeline.

## Required IAM Resources

The GenAI Pipeline requires the following IAM resources:

1. **Lambda Execution Role** - A role that Lambda can assume to execute the function
2. **Bedrock Access Policy** - A policy that grants permission to invoke Bedrock models

## Manual Setup (Recommended)

### Step 1: Create Lambda Execution Role

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

### Step 2: Add Bedrock Access Policy

1. Find and click on the newly created "lambda-bedrock-role" in the roles list
2. Click on the "Permissions" tab
3. Click "Add permissions" and select "Create inline policy"
4. Click on the "JSON" tab
5. Paste the following policy:

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

6. Click "Review policy"
7. Name the policy "bedrock-access"
8. Click "Create policy"

### Step 3: Get the Role ARN

1. Go back to the "lambda-bedrock-role" summary page
2. Copy the Role ARN (it will look like `arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-bedrock-role`)
3. Add this ARN to your .env file as `LAMBDA_ROLE_ARN`

## Using AWS CLI

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

## Using the setup-iam.py Script

The project includes a script to set up IAM resources:

```bash
# Windows
py iam/setup-iam.py

# Linux/Mac
python iam/setup-iam.py
```

This script will:
1. Create the Lambda execution role
2. Attach the necessary policies
3. Create a test user (optional)

## Minimum Required Permissions

If you want to create a custom policy with minimal permissions, include:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
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

## Troubleshooting

### Permission Denied Errors

If you encounter "Permission Denied" errors when creating IAM resources:

1. Check that your AWS user has the necessary permissions
2. Consider using the AWS Console to create the resources manually
3. Ask your AWS administrator to create the resources for you

### Role Already Exists

If the role already exists:

1. Use the existing role
2. Get the ARN of the existing role
3. Add the ARN to your .env file as `LAMBDA_ROLE_ARN`

### Missing Permissions

If the Lambda function fails with permission errors:

1. Check that the role has the AWSLambdaBasicExecutionRole policy
2. Check that the role has the bedrock-access inline policy
3. Verify that the trust relationship allows Lambda to assume the role

## Current Role ARN

The current deployment uses the following role:

```
arn:aws:iam::004909959584:role/lambda-bedrock-role
```

Add this to your .env file as:

```
LAMBDA_ROLE_ARN=arn:aws:iam::004909959584:role/lambda-bedrock-role
```