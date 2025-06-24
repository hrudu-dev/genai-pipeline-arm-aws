@echo off
echo Cleaning up GenAI Pipeline resources...

REM Load environment variables
if exist .env (
    for /f "tokens=1,2 delims==" %%a in (.env) do set %%a=%%b
)

REM Delete CloudFormation stacks
echo Deleting CloudFormation stacks...
aws cloudformation delete-stack --stack-name GenAIPipelineStack
aws cloudformation delete-stack --stack-name GenAIPipelineStack-Tagging

REM Wait for stack deletion
echo Waiting for stack deletion...
aws cloudformation wait stack-delete-complete --stack-name GenAIPipelineStack

REM Delete S3 bucket contents and bucket
if defined S3_BUCKET (
    echo Emptying S3 bucket: %S3_BUCKET%
    aws s3 rm s3://%S3_BUCKET% --recursive
    aws s3 rb s3://%S3_BUCKET%
)

echo Cleanup completed!