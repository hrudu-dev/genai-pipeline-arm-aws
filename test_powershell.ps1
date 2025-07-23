# PowerShell script to test GenAI Pipeline API
# This demonstrates the correct way to call the API from Windows PowerShell

$apiUrl = "https://cr7c7lxj5mt2lwvyi57s2o6arq0paars.lambda-url.us-east-1.on.aws/"
$prompt = "What is artificial intelligence?"

Write-Host "Testing GenAI Pipeline API with PowerShell..." -ForegroundColor Green
Write-Host "Prompt: $prompt" -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method POST -ContentType "application/json" -Body "{`"prompt`":`"$prompt`"}"
    
    if ($response.inference_complete) {
        Write-Host "`nAPI Response:" -ForegroundColor Green
        Write-Host $response.result -ForegroundColor White
    } else {
        Write-Host "Error: $($response.error)" -ForegroundColor Red
    }
} catch {
    Write-Host "Failed to call API: $($_.Exception.Message)" -ForegroundColor Red
}
