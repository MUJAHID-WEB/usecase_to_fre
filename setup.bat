@echo off
echo Setting up Use Case to FR Converter on Windows...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install --upgrade pip
pip install flask==2.3.3 flask-cors==4.0.0 pillow==10.0.0

echo Installing lightweight OCR alternative...
pip install pytesseract==0.3.10

echo Installing NLP libraries...
pip install nltk==3.8.1

echo Setup completed!
echo.
echo IMPORTANT: You need to install Tesseract OCR separately:
echo 1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
echo 2. Install Tesseract OCR
echo 3. The system will work with sample data if Tesseract is not installed
echo.
echo To run the application:
echo 1. Start backend: run-backend.bat
echo 2. Open frontend/index.html in your browser
pause