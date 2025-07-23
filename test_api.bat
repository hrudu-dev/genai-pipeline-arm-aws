@echo off
echo Testing GenAI Pipeline API...
echo.

curl -X POST "https://2fu2iveexbqvfe74qqehldjeky0urivd.lambda-url.us-east-1.on.aws/" ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\": \"What is artificial intelligence?\"}"

echo.
echo Test complete!