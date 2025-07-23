@echo off
echo Setting up IAM for GenAI Pipeline Testing...

REM Check if AWS CLI is installed
where aws >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo AWS CLI not found. Please install AWS CLI.
    exit /b 1
)

echo.
echo === Creating Lambda Execution Role ===
echo.

REM Create the Lambda execution role
aws iam create-role --role-name lambda-bedrock-role --assume-role-policy-document file://iam/lambda-trust-policy.json
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create Lambda role.
    exit /b 1
)

REM Attach the execution policy to the role
aws iam put-role-policy --role-name lambda-bedrock-role --policy-name lambda-bedrock-execution --policy-document file://iam/lambda-execution-role-policy.json
if %ERRORLEVEL% NEQ 0 (
    echo Failed to attach policy to Lambda role.
    exit /b 1
)

echo.
echo === Creating Test Policy ===
echo.

REM Create the test policy
aws iam create-policy --policy-name GenAIPipelineTestPolicy --policy-document file://iam/genai-pipeline-test-policy.json
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create test policy.
    exit /b 1
)

REM Get the account ID
for /f "tokens=2 delims=: " %%a in ('aws sts get-caller-identity --query "Account" --output text') do set ACCOUNT_ID=%%a

echo.
echo === Creating Test User ===
echo.

REM Create the user
aws iam create-user --user-name genai-pipeline-tester
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create test user.
    exit /b 1
)

REM Attach the test policy to the user
aws iam attach-user-policy --user-name genai-pipeline-tester --policy-arn arn:aws:iam::%ACCOUNT_ID%:policy/GenAIPipelineTestPolicy
if %ERRORLEVEL% NEQ 0 (
    echo Failed to attach policy to test user.
    exit /b 1
)

REM Create access keys for the user
aws iam create-access-key --user-name genai-pipeline-tester > access_keys.json
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create access keys.
    exit /b 1
)

echo.
echo === IAM Setup Complete ===
echo.
echo Your access keys have been saved to access_keys.json
echo Please update your .env file with these credentials.
echo.
echo Next steps:
echo 1. Make sure your AWS account has access to Amazon Bedrock
echo 2. Run local tests: python test_local.py
echo 3. Deploy Lambda: python setup.py