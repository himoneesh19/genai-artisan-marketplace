@echo off
REM GenAI Artisan Marketplace Startup Script
REM This script sets up the environment and starts the Flask application

echo === GenAI Artisan Marketplace Startup ===
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Set Google Cloud credentials
set CREDENTIALS_PATH=C:\secure\genAI\credentials\my-project-genai-471504-228dc08e66b2.json
if exist "%CREDENTIALS_PATH%" (
    echo Setting Google Cloud credentials...
    set GOOGLE_APPLICATION_CREDENTIALS=%CREDENTIALS_PATH%
    set GOOGLE_CLOUD_PROJECT=my-project-genai-471504
    echo Credentials configured successfully!
) else (
    echo WARNING: Service account JSON file not found at %CREDENTIALS_PATH%
    echo Attempting to use gcloud application default credentials...
    set GOOGLE_APPLICATION_CREDENTIALS=%APPDATA%\gcloud\application_default_credentials.json
    set GOOGLE_CLOUD_PROJECT=my-project-genai-471504
    if exist "%GOOGLE_APPLICATION_CREDENTIALS%" (
        echo Using gcloud application default credentials.
    ) else (
        echo ERROR: No credentials found. Please set up Google Cloud credentials.
        pause
        exit /b 1
    )
)

echo.
echo Starting Flask application...
echo Application will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the application
echo.

REM Start the application
python app.py
