@echo off
echo ========================================
echo   GenAI Pipeline - AWS CLI Setup
echo ========================================
echo.

REM Check if AWS CLI is installed
echo [1/5] Checking AWS CLI installation...
aws --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: AWS CLI not found!
    echo.
    echo Please install AWS CLI first:
    echo 1. Download from: https://aws.amazon.com/cli/
    echo 2. Or use: winget install Amazon.AWSCLI
    echo.
    pause
    exit /b 1
)
echo ✓ AWS CLI found

echo.
echo [2/5] AWS Access Keys Setup
echo.
echo You need AWS Access Keys. If you don't have them:
echo 1. Go to: https://console.aws.amazon.com
echo 2. Navigate to IAM ^> Users ^> Create user
echo 3. Attach policies: BedrockFullAccess, LambdaFullAccess, S3FullAccess, CloudFormationFullAccess
echo 4. Download the access keys
echo.
echo See docs\aws-setup-guide.md for detailed instructions
echo.
pause

REM Configure AWS CLI
echo [3/5] Configuring AWS CLI...
aws configure

REM Verify configuration
echo.
echo [4/5] Verifying AWS configuration...
aws sts get-caller-identity
if %errorlevel% neq 0 (
    echo ERROR: AWS configuration failed!
    echo Please check your access keys and try again.
    pause
    exit /b 1
)
echo ✓ AWS configuration verified

REM Create S3 bucket for artifacts
echo.
echo [5/5] Creating S3 bucket for deployment artifacts...
set BUCKET_NAME=genai-pipeline-artifacts-%RANDOM%
aws s3 mb s3://%BUCKET_NAME% --region us-east-1
if %errorlevel% neq 0 (
    echo ERROR: Failed to create S3 bucket!
    echo Please check your S3 permissions.
    pause
    exit /b 1
)

REM Save configuration
echo AWS_REGION=us-east-1 > .env
echo S3_BUCKET=%BUCKET_NAME% >> .env
echo PROJECT_NAME=GenAIPipeline >> .env
echo ENVIRONMENT=dev >> .env
echo STACK_NAME=GenAIPipelineStack >> .env

echo.
echo ========================================
echo   AWS Setup Completed Successfully!
echo ========================================
echo S3 Bucket: %BUCKET_NAME%
echo Configuration saved to: .env
echo.
echo Next step: Run 'scripts\deploy.bat' to deploy your pipeline
echo.
pause