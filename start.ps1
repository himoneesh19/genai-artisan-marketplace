# GenAI Artisan Marketplace Startup Script
# This script sets up the environment and starts the Flask application

Write-Host "=== GenAI Artisan Marketplace Startup ===" -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& venv\Scripts\Activate.ps1

# Install/update dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Set Google Cloud credentials
$credentialsPath = "C:\secure\genAI\credentials\my-project-genai-471504-228dc08e66b2.json"
if (Test-Path $credentialsPath) {
    Write-Host "Setting Google Cloud credentials..." -ForegroundColor Yellow
    $env:GOOGLE_APPLICATION_CREDENTIALS = $credentialsPath
    $env:GOOGLE_CLOUD_PROJECT = "my-project-genai-471504"
    Write-Host "Credentials configured successfully!" -ForegroundColor Green
} else {
    Write-Warning "Service account JSON file not found at $credentialsPath"
    Write-Warning "Please ensure your credentials are located at the correct path."
    Write-Warning "You can update the path in this script if needed."
    Read-Host "Press Enter to continue anyway"
}

Write-Host ""
Write-Host "Starting Flask application..." -ForegroundColor Green
Write-Host "Application will be available at: http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

# Start the application
python app.py
