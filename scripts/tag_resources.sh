#!/bin/bash

echo "Tagging AWS resources for GenAI Pipeline Project..."

# Tag EC2 instances
echo "Tagging EC2 instances..."
for instance in $(aws ec2 describe-instances --query 'Reservations[*].Instances[*].InstanceId' --output text)
do
  aws ec2 create-tags --resources $instance --tags \
    Key=Project,Value=GenAIPipeline \
    Key=Environment,Value=dev \
    Key=Component,Value=ModelInference \
    Key=Service,Value=Graviton
done

# Tag S3 buckets
echo "Tagging S3 buckets..."
for bucket in $(aws s3api list-buckets --query 'Buckets[?contains(Name, `genai`)].Name' --output text)
do
  aws s3api put-bucket-tagging --bucket $bucket --tagging 'TagSet=[
    {Key=Project,Value=GenAIPipeline},
    {Key=Environment,Value=dev},
    {Key=Component,Value=DataProcessing}
  ]'
done

# Tag Lambda functions
echo "Tagging Lambda functions..."
for function in $(aws lambda list-functions --query 'Functions[?contains(FunctionName, `genai`)].FunctionName' --output text)
do
  aws lambda tag-resource --resource $(aws lambda get-function --function-name $function --query 'Configuration.FunctionArn' --output text) --tags \
    Project=GenAIPipeline,Environment=dev,Component=ModelInference,Service=Bedrock
done

echo "Resource tagging completed!"