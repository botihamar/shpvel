#!/bin/bash

# Anonymous Chat Bot - Quick Setup Script
# This script helps you quickly set up and run the bot

set -e  # Exit on error

echo "=========================================="
echo "  Anonymous Chat Bot - Quick Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo "✅ Python $PYTHON_VERSION found"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version | awk '{print $2}')
    echo "✅ Python $PYTHON_VERSION found"
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

echo ""

# Install dependencies
echo "Installing dependencies..."
if $PYTHON_CMD -m pip install -r requirements.txt; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found"
    echo ""
    echo "Would you like to run the setup wizard? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        $PYTHON_CMD setup.py
    else
        echo ""
        echo "Please create a .env file manually using .env.example as a template"
        echo "Then run: $PYTHON_CMD bot.py"
        exit 0
    fi
else
    echo "✅ .env file found"
fi

echo ""

# Run tests
echo "Running tests..."
if $PYTHON_CMD test.py; then
    echo ""
    echo "=========================================="
    echo "  ✅ Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Your bot is ready to run!"
    echo ""
    echo "To start the bot, run:"
    echo "  $PYTHON_CMD bot.py"
    echo ""
    echo "Or run this script with 'start' argument:"
    echo "  ./quicksetup.sh start"
    echo ""
else
    echo ""
    echo "⚠️  Some tests failed. Please check the output above."
    echo ""
    echo "You can still try to run the bot with:"
    echo "  $PYTHON_CMD bot.py"
    echo ""
fi

# Check if start argument is passed
if [ "$1" = "start" ]; then
    echo "Starting the bot..."
    echo ""
    $PYTHON_CMD bot.py
fi
