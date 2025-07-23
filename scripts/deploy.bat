@echo off
echo Deploying GenAI Pipeline Lambda function...

REM Check if AWS CLI is installed
where aws >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo AWS CLI not found. Please install AWS CLI.
    exit /b 1
)

REM Load environment variables from .env file
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if not "%%a"=="" if not "%%a:~0,1%"=="#" (
        set "%%a=%%b"
    )
)

echo Building Lambda package...
mkdir -p build
xcopy /s /y src build\
copy requirements.txt build\

echo Creating Lambda function...
aws lambda create-function ^
    --function-name %PROJECT_NAME% ^
    --runtime python3.9 ^
    --architectures arm64 ^
    --handler main.lambda_handler ^
    --role arn:aws:iam::%AWS_ACCOUNT_ID%:role/lambda-bedrock-role ^
    --zip-file fileb://build/function.zip ^
    --region %AWS_DEFAULT_REGION%

echo Creating function URL...
aws lambda create-function-url-config ^
    --function-name %PROJECT_NAME% ^
    --auth-type NONE ^
    --region %AWS_DEFAULT_REGION%

echo Deployment complete!
echo Function URL: https://{function-id}.lambda-url.%AWS_DEFAULT_REGION%.on.aws/