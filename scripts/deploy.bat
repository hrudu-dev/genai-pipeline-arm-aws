@echo off
setlocal enabledelayedexpansion

echo Deploying GenAI Pipeline to AWS...

REM Load environment variables
if exist .env (
    for /f "tokens=1,2 delims==" %%a in (.env) do set %%a=%%b
)

REM Set defaults if not in .env
if not defined AWS_REGION set AWS_REGION=us-east-1
if not defined STACK_NAME set STACK_NAME=GenAIPipelineStack
if not defined PROJECT_NAME set PROJECT_NAME=GenAIPipeline

REM Build project first
call scripts\build.bat

REM Upload artifacts to S3
echo Uploading artifacts to S3...
aws s3 cp dist\genai-pipeline.zip s3://%S3_BUCKET%/artifacts/

REM Deploy infrastructure
echo Deploying infrastructure...
aws cloudformation deploy ^
    --template-file infra\cloudformation\pipeline.yaml ^
    --stack-name %STACK_NAME% ^
    --parameter-overrides ^
        ProjectName=%PROJECT_NAME% ^
        Environment=dev ^
        ArtifactsBucket=%S3_BUCKET% ^
    --capabilities CAPABILITY_IAM ^
    --region %AWS_REGION%

REM Deploy tagging resources
echo Deploying tagging resources...
aws cloudformation deploy ^
    --template-file infra\cloudformation\tagging-resources.yaml ^
    --stack-name %STACK_NAME%-Tagging ^
    --capabilities CAPABILITY_IAM ^
    --region %AWS_REGION%

REM Tag resources
echo Tagging resources...
call scripts\tag_resources.bat

echo Deployment completed successfully!
echo Stack: %STACK_NAME%
echo Region: %AWS_REGION%