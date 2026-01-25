#!/bin/bash
# Simple bot status checker - No dependencies required

echo "=================================================="
echo "  Anonymous Chat Bot - Status"
echo "=================================================="
echo ""

# Find all Python processes running bot.py
PIDS=$(pgrep -f "python.*bot\.py")

if [ -z "$PIDS" ]; then
    echo "❌ Bot is NOT running"
    echo ""
else
    COUNT=$(echo "$PIDS" | wc -l | tr -d ' ')
    echo "✅ Bot is RUNNING ($COUNT instance(s))"
    echo ""
    
    for PID in $PIDS; do
        echo "   PID: $PID"
        
        # Get process info (macOS specific)
        if command -v ps &> /dev/null; then
            # CPU and Memory
            STATS=$(ps -p $PID -o %cpu,%mem | tail -1)
            echo "   CPU/Memory: $STATS"
            
            # Command line
            CMD=$(ps -p $PID -o command | tail -1)
            echo "   Command: $CMD"
        fi
        
        echo ""
    done
fi

echo "=================================================="
echo ""
echo "Commands:"
echo "  ./start_bot.sh  - Start the bot"
echo "  ./stop_bot.sh   - Stop the bot"
echo "  ./status_bot.sh - Check status (this script)"
echo ""
