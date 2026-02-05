#!/bin/bash

# HacxGPT Web UI Installation Script
# Installs dependencies and sets up the web interface

echo "=============================================="
echo "🔥 HacxGPT Web UI - Installation Script"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install/upgrade pip
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements
echo ""
echo "📦 Installing dependencies..."
echo ""

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    echo "⚠️  requirements.txt not found. Installing core dependencies..."
    pip3 install openai rich python-dotenv pwinput pyperclip colorama prompt_toolkit gradio
fi

# Install package in development mode
echo ""
echo "📦 Installing HacxGPT package..."
pip3 install -e .

echo ""
echo "=============================================="
echo "✅ Installation Complete!"
echo "=============================================="
echo ""
echo "🚀 Quick Start:"
echo ""
echo "  Terminal UI:"
echo "    hacxgpt"
echo ""
echo "  Web UI:"
echo "    python hacxgpt_web.py"
echo "    # OR"
echo "    hacxgpt-web"
echo ""
echo "  Then open: http://127.0.0.1:7860"
echo ""
echo "📚 Documentation:"
echo "  - README.md - General information"
echo "  - WEB_UI_GUIDE.md - Web interface guide"
echo ""
echo "🧪 Test Installation:"
echo "  python test_web_ui.py"
echo ""
echo "=============================================="
