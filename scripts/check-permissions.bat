@echo off
echo Checking AWS permissions for GenAI Pipeline...

echo Testing IAM permissions...
aws iam get-user >nul 2>&1
if %errorlevel% equ 0 (echo \u2713 IAM access) else (echo \u2717 IAM access - REQUIRED)

echo Testing S3 permissions...
aws s3 ls >nul 2>&1
if %errorlevel% equ 0 (echo \u2713 S3 access) else (echo \u2717 S3 access - REQUIRED)

echo Testing Lambda permissions...
aws lambda list-functions >nul 2>&1
if %errorlevel% equ 0 (echo \u2713 Lambda access) else (echo \u2717 Lambda access - REQUIRED)

echo Testing CloudFormation permissions...
aws cloudformation list-stacks >nul 2>&1
if %errorlevel% equ 0 (echo \u2713 CloudFormation access) else (echo \u2717 CloudFormation access - REQUIRED)

echo Testing Bedrock permissions...
aws bedrock list-foundation-models >nul 2>&1
if %errorlevel% equ 0 (echo \u2713 Bedrock access) else (echo \u2717 Bedrock access - REQUIRED)

echo.
echo If any permissions are missing, update your IAM user policies.