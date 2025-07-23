# Deploying the GenAI Pipeline

This guide provides step-by-step instructions for deploying the GenAI Pipeline to AWS.

## Prerequisites

1. AWS account with access to:
   - AWS Lambda
   - Amazon Bedrock (Claude 3 Haiku model)
   - IAM permissions to create roles and policies

2. AWS CLI installed and configured with appropriate credentials

## Option 1: Automated Setup (Recommended)

The easiest way to deploy the GenAI Pipeline is using our setup script:

```bash
python setup.py
```

This script will:
1. Configure your AWS credentials
2. Check your access to Amazon Bedrock
3. Deploy the Lambda function
4. Update test scripts with your function URL

## Option 2: One-Click CloudFormation Deployment

For a complete infrastructure deployment:

1. Open the AWS CloudFormation console
2. Click "Create stack" > "With new resources"
3. Upload the template file: `deploy/one-click-deploy.yaml`
4. Follow the prompts to complete the deployment
5. Once deployed, note the function URL from the Outputs tab

## Option 3: Manual Deployment

### Step 1: Configure AWS Credentials

Create or update your `.env` file with AWS credentials:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

### Step 2: Create IAM Role for Lambda

1. Create a file named `trust-policy.json`:
   ```json
   {
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
   }
   ```

2. Create the role:
   ```bash
   aws iam create-role --role-name lambda-bedrock-role --assume-role-policy-document file://trust-policy.json
   ```

3. Attach policies:
   ```bash
   aws iam attach-role-policy --role-name lambda-bedrock-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
   ```

4. Create Bedrock access policy:
   ```bash
   aws iam put-role-policy --role-name lambda-bedrock-role --policy-name bedrock-access --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"bedrock:InvokeModel","Resource":"*"}]}'
   ```

### Step 3: Deploy Lambda Function

1. Build the package:
   ```bash
   mkdir -p build
   cp -r src/* build/
   pip install -r requirements.txt -t build/
   cd build && zip -r ../function.zip . && cd ..
   ```

2. Create the Lambda function:
   ```bash
   aws lambda create-function \
     --function-name GenAIPipeline \
     --runtime python3.9 \
     --architectures arm64 \
     --handler main.lambda_handler \
     --role arn:aws:iam::ACCOUNT_ID:role/lambda-bedrock-role \
     --zip-file fileb://function.zip
   ```

3. Create function URL:
   ```bash
   aws lambda create-function-url-config \
     --function-name GenAIPipeline \
     --auth-type NONE
   ```

## Testing Your Deployment

After deployment, test your function:

```bash
curl -X POST "YOUR_FUNCTION_URL" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is artificial intelligence?"}'
```

Or use the provided test script:

```bash
python run_test.py
```