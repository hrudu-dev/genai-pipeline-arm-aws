#!/bin/bash

echo "Deploying GenAI Pipeline Tagging Stack..."

# Deploy CloudFormation stack for resource groups
aws cloudformation create-stack \
  --stack-name GenAIPipelineTaggingStack \
  --template-body file://../infra/cloudformation/tagging-resources.yaml \
  --capabilities CAPABILITY_IAM

echo "Waiting for stack creation to complete..."
aws cloudformation wait stack-create-complete --stack-name GenAIPipelineTaggingStack

echo "Stack deployed successfully!"
echo "Stack outputs:"
aws cloudformation describe-stacks --stack-name GenAIPipelineTaggingStack --query 'Stacks[0].Outputs' --output table