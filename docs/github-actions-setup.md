# Setting Up GitHub Actions Secrets

This document explains how to set up the necessary secrets for GitHub Actions to deploy the GenAI Pipeline.

## Required Secrets

The GitHub Actions workflows require the following secrets:

1. **AWS_ACCESS_KEY_ID**: Your AWS access key ID
2. **AWS_SECRET_ACCESS_KEY**: Your AWS secret access key
3. **AWS_DEFAULT_REGION**: (Optional) The AWS region to deploy to (defaults to us-east-1)
4. **LAMBDA_ROLE_ARN**: The ARN of the IAM role for the Lambda function

## Setting Up Secrets

1. Go to your GitHub repository
2. Click on **Settings**
3. In the left sidebar, click on **Secrets and variables** → **Actions**
4. Click on **New repository secret**
5. Add each of the required secrets:

### AWS_ACCESS_KEY_ID

1. Name: `AWS_ACCESS_KEY_ID`
2. Value: Your AWS access key ID
3. Click **Add secret**

### AWS_SECRET_ACCESS_KEY

1. Name: `AWS_SECRET_ACCESS_KEY`
2. Value: Your AWS secret access key
3. Click **Add secret**

### AWS_DEFAULT_REGION

1. Name: `AWS_DEFAULT_REGION`
2. Value: The AWS region to deploy to (e.g., `us-east-1`)
3. Click **Add secret**

### LAMBDA_ROLE_ARN

1. Name: `LAMBDA_ROLE_ARN`
2. Value: The ARN of the IAM role for the Lambda function (e.g., `arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-bedrock-role`)
3. Click **Add secret**

## Creating AWS Credentials

If you don't have AWS credentials yet:

1. Go to the AWS Management Console
2. Navigate to IAM (Identity and Access Management)
3. Click on **Users** in the left sidebar
4. Click **Add users**
5. Enter a username (e.g., `github-actions`)
6. Select **Access key - Programmatic access**
7. Click **Next: Permissions**
8. Click **Attach existing policies directly**
9. Search for and select the following policies:
   - `AWSLambdaFullAccess`
   - `IAMFullAccess`
   - `AmazonBedrockFullAccess`
10. Click **Next: Tags** (add tags if desired)
11. Click **Next: Review**
12. Click **Create user**
13. Copy the **Access key ID** and **Secret access key**
14. Add these as secrets in your GitHub repository

## IAM Role for Lambda

Make sure you have created the IAM role for the Lambda function:

1. Go to the AWS Management Console
2. Navigate to IAM (Identity and Access Management)
3. Click on **Roles** in the left sidebar
4. Click **Create role**
5. Select **AWS service** and **Lambda**
6. Click **Next: Permissions**
7. Attach the **AWSLambdaBasicExecutionRole** policy
8. Click **Next: Tags** (add tags if desired)
9. Click **Next: Review**
10. Name the role **lambda-bedrock-role**
11. Click **Create role**
12. Go to the role and add an inline policy for Bedrock access:

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

13. Name the policy **bedrock-access** and click **Create policy**
14. Copy the role ARN and add it as the `LAMBDA_ROLE_ARN` secret in your GitHub repository

## Troubleshooting

If the GitHub Actions workflow fails:

1. Check that all required secrets are set
2. Verify that the AWS credentials have the necessary permissions
3. Ensure that the Lambda role ARN is correct
4. Check the workflow logs for detailed error messages