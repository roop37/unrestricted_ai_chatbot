@echo off
REM HacxGPT Web UI Installation Script for Windows
REM Installs dependencies and sets up the web interface

echo ==============================================
echo 🔥 HacxGPT Web UI - Installation Script
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python found
python --version
echo.

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo 📦 Installing dependencies...
echo.

if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo ⚠️  requirements.txt not found. Installing core dependencies...
    pip install openai rich python-dotenv pwinput pyperclip colorama prompt_toolkit gradio
)

REM Install package in development mode
echo.
echo 📦 Installing HacxGPT package...
pip install -e .

echo.
echo ==============================================
echo ✅ Installation Complete!
echo ==============================================
echo.
echo 🚀 Quick Start:
echo.
echo   Terminal UI:
echo     hacxgpt
echo.
echo   Web UI:
echo     python hacxgpt_web.py
echo     # OR
echo     hacxgpt-web
echo.
echo   Then open: http://127.0.0.1:7860
echo.
echo 📚 Documentation:
echo   - README.md - General information
echo   - WEB_UI_GUIDE.md - Web interface guide
echo.
echo 🧪 Test Installation:
echo   python test_web_ui.py
echo.
echo ==============================================
pause
