@echo off
echo Tagging AWS resources for GenAI Pipeline Project...

REM Tag Lambda functions
echo Tagging Lambda functions...
for /f %%i in ('aws lambda list-functions --query "Functions[?contains(FunctionName, 'genai')].FunctionName" --output text') do (
    for /f %%j in ('aws lambda get-function --function-name %%i --query "Configuration.FunctionArn" --output text') do (
        aws lambda tag-resource --resource %%j --tags Project=GenAIPipeline,Environment=dev,Component=ModelInference,Service=Bedrock
    )
)

REM Tag S3 buckets
echo Tagging S3 buckets...
for /f %%i in ('aws s3api list-buckets --query "Buckets[?contains(Name, 'genai')].Name" --output text') do (
    aws s3api put-bucket-tagging --bucket %%i --tagging "TagSet=[{Key=Project,Value=GenAIPipeline},{Key=Environment,Value=dev},{Key=Component,Value=DataProcessing}]"
)

echo Resource tagging completed!