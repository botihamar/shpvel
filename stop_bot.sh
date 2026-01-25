#!/bin/bash
# Simple bot stopper - No dependencies required

echo "🛑 Stopping Anonymous Chat Bot..."
echo ""

# Find all Python processes running bot.py
PIDS=$(pgrep -f "python.*bot\.py")

if [ -z "$PIDS" ]; then
    echo "✅ No bot processes found running"
    exit 0
fi

echo "Found bot process(es):"
for PID in $PIDS; do
    echo "  - PID: $PID"
done

echo ""
echo "Stopping processes..."

# Try graceful termination first
for PID in $PIDS; do
    if kill $PID 2>/dev/null; then
        echo "  ✅ Sent SIGTERM to PID $PID"
        sleep 1
        
        # Check if still running
        if kill -0 $PID 2>/dev/null; then
            echo "  ⚠️  Process still running, force killing..."
            kill -9 $PID 2>/dev/null
            echo "  ✅ Force killed PID $PID"
        else
            echo "  ✅ Process $PID stopped gracefully"
        fi
    else
        echo "  ⚠️  Could not stop PID $PID (may already be stopped)"
    fi
done

echo ""
echo "🎉 All bot processes stopped!"
