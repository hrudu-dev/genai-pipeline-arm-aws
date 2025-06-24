#!/bin/bash
# Setup IAM policies for GenAI Pipeline

set -e

export AWS_ACCESS_KEY_ID=AKIAQCJFIBGQIDQPFLSB
export AWS_SECRET_ACCESS_KEY=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
export AWS_DEFAULT_REGION=us-east-1

AWS_CLI="/home/codespace/.local/lib/python3.12/site-packages/bin/aws"

echo "🔐 Setting up IAM policies for GenAI Pipeline..."

# Create Lambda execution policy
echo "📋 Creating Lambda execution policy..."
$AWS_CLI iam create-policy \
  --policy-name GenAIPipeline-Lambda-Policy \
  --policy-document file://lambda-policy.json \
  --description "Policy for GenAI Pipeline Lambda execution" || echo "Policy may already exist"

# Create user policy  
echo "👤 Creating user access policy..."
$AWS_CLI iam create-policy \
  --policy-name GenAIPipeline-User-Policy \
  --policy-document file://user-policy.json \
  --description "Policy for GenAI Pipeline user access" || echo "Policy may already exist"

# Add permission for function URL
echo "🌐 Adding function URL permission..."
$AWS_CLI lambda add-permission \
  --function-name GenAIPipeline-Inference \
  --statement-id FunctionURLAllowPublicAccess \
  --action lambda:InvokeFunctionUrl \
  --principal '*' || echo "Permission may already exist"

echo "✅ Permissions setup complete!"
echo "📝 To assign to user, run:"
echo "aws iam attach-user-policy --user-name YOUR_USERNAME --policy-arn arn:aws:iam::004909959584:policy/GenAIPipeline-User-Policy"