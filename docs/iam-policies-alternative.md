# Alternative IAM Policy Setup

If you can't find the exact policy names, use these alternatives:

## Method 1: Search for Policies
In IAM → Users → Attach Policies, search for:

- **Lambda**: Search "Lambda" → Select `AWSLambda_FullAccess`
- **Bedrock**: Search "Bedrock" → Select `AmazonBedrockFullAccess`  
- **S3**: Search "S3" → Select `AmazonS3FullAccess`
- **CloudFormation**: Search "CloudFormation" → Select `CloudFormationFullAccess`
- **API Gateway**: Search "API" → Select `AmazonAPIGatewayAdministrator`
- **IAM**: Search "IAM" → Select `IAMFullAccess`

## Method 2: Create Custom Policy
If policies are missing, create a custom policy with this JSON:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:*",
                "bedrock:*",
                "s3:*",
                "cloudformation:*",
                "apigateway:*",
                "iam:*",
                "logs:*"
            ],
            "Resource": "*"
        }
    ]
}
```

## Method 3: Use PowerUser Policy
Attach `PowerUserAccess` policy (gives most permissions except IAM)

## Minimum Required Actions
Your user needs these specific permissions:
- `lambda:CreateFunction`
- `lambda:UpdateFunctionCode`
- `bedrock:InvokeModel`
- `s3:CreateBucket`
- `s3:PutObject`
- `cloudformation:CreateStack`
- `cloudformation:UpdateStack`