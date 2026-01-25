#!/bin/bash
# Simple bot starter - Checks for existing instances

echo "🚀 Starting Anonymous Chat Bot..."
echo ""

# Check if bot is already running
PIDS=$(pgrep -f "python.*bot\.py")

if [ ! -z "$PIDS" ]; then
    echo "⚠️  Bot is already running!"
    echo ""
    echo "Running processes:"
    for PID in $PIDS; do
        echo "  - PID: $PID"
    done
    echo ""
    echo "To stop existing instances, run:"
    echo "  ./stop_bot.sh"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ -d "env" ]; then
    echo "Activating virtual environment..."
    source env/bin/activate
fi

# Start the bot
echo "Starting bot..."
echo ""
python bot.py
