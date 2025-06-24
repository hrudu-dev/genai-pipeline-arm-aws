@echo off
echo Testing GenAI Pipeline API...

REM Get API endpoint from CloudFormation stack
for /f %%i in ('aws cloudformation describe-stacks --stack-name GenAIPipelineStack --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text') do set API_ENDPOINT=%%i

echo API Endpoint: %API_ENDPOINT%

REM Test the API
echo Testing inference endpoint...
curl -X POST %API_ENDPOINT% ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\": \"What is artificial intelligence?\"}"

echo.
echo API test completed!