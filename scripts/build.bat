@echo off
echo Building GenAI Pipeline Project...

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Run tests
echo Running tests...
python -m pytest tests/ -v

REM Package Lambda functions
echo Packaging Lambda functions...
if not exist "dist" mkdir dist

REM Create deployment package
echo Creating deployment package...
powershell Compress-Archive -Path src\* -DestinationPath dist\genai-pipeline.zip -Force

echo Build completed successfully!