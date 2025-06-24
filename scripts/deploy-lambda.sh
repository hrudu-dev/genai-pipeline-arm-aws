#!/bin/bash
# Deploy Lambda function with minimal dependencies

set -e

echo "🚀 Deploying minimal Lambda package..."

# Create minimal build
mkdir -p build/minimal
cp src/inference.py build/minimal/
cp src/data_processing.py build/minimal/
cp src/utils.py build/minimal/

# Install only essential dependencies
pip install boto3 -t build/minimal/ --no-deps

# Create minimal package
cd build/minimal
zip -r ../../genai-pipeline-minimal.zip .
cd ../..

echo "📦 Minimal package created: genai-pipeline-minimal.zip"

# Deploy to Lambda
export AWS_ACCESS_KEY_ID=AKIAQCJFIBGQIDQPFLSB
export AWS_SECRET_ACCESS_KEY=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
export AWS_DEFAULT_REGION=us-east-1

echo "🔄 Updating Lambda function..."
/home/codespace/.local/lib/python3.12/site-packages/bin/aws lambda update-function-code \
  --function-name GenAIPipeline-Inference \
  --zip-file fileb://genai-pipeline-minimal.zip

echo "⚙️ Updating to ARM64 architecture..."
/home/codespace/.local/lib/python3.12/site-packages/bin/aws lambda update-function-configuration \
  --function-name GenAIPipeline-Inference \
  --architectures arm64 \
  --runtime python3.11

echo "✅ Lambda deployment complete!"