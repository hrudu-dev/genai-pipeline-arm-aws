# AWS CLI Setup Guide

## Step 1: Get AWS Access Keys

### Option A: IAM User (Recommended for Development)

1. **Login to AWS Console**: https://console.aws.amazon.com
2. **Go to IAM Service**: Search "IAM" in services
3. **Create User**:
   - Click "Users" → "Create user"
   - Username: `genai-pipeline-dev`
   - Select "Programmatic access"
4. **Attach Policies** (search for each one):
   - `AmazonBedrockFullAccess`
   - `AWSLambda_FullAccess` (or search "Lambda")
   - `AmazonS3FullAccess`
   - `CloudFormationFullAccess`
   - `IAMFullAccess`
   - `AmazonAPIGatewayAdministrator`
   
   **If policies don't show up:**
   - Use the search box in "Attach policies"
   - Type "Lambda" and select `AWSLambda_FullAccess`
   - Type "Bedrock" and select `AmazonBedrockFullAccess`
   - Type "S3" and select `AmazonS3FullAccess`
5. **Download Keys**: Save the CSV file with Access Key ID and Secret

### Option B: AWS CLI SSO (Recommended for Production)

1. **Setup AWS SSO** in your organization
2. **Use**: `aws configure sso`

## Step 2: Configure AWS CLI

Run the setup script:
```cmd
scripts\setup-aws.bat
```

Or manually:
```cmd
aws configure
```

Enter:
- **AWS Access Key ID**: [Your access key]
- **AWS Secret Access Key**: [Your secret key]
- **Default region**: us-east-1
- **Default output format**: json

## Step 3: Verify Setup

```cmd
aws sts get-caller-identity
```

Should return your account info.

## Required Permissions

Your IAM user needs these services:
- Amazon Bedrock (AI models)
- AWS Lambda (serverless functions)
- Amazon S3 (storage)
- CloudFormation (infrastructure)
- API Gateway (REST API)
- IAM (roles and policies)