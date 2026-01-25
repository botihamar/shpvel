#!/bin/bash
# Safe bot starter - Always ensures clean start

echo "🚀 Safe Bot Starter"
echo "===================="
echo ""

# Step 1: Kill any existing instances
echo "🔍 Step 1: Checking for existing bot instances..."
if pgrep -f "python.*bot\.py" > /dev/null; then
    echo "⚠️  Found running bot(s). Stopping them..."
    pkill -9 -f "python.*bot\.py"
    sleep 2
    
    # Double-check they're gone
    if pgrep -f "python.*bot\.py" > /dev/null; then
        echo "❌ ERROR: Failed to stop existing bot!"
        echo "Please manually run: pkill -9 -f bot.py"
        exit 1
    fi
    echo "✅ Stopped existing instances"
else
    echo "✅ No existing instances found"
fi

echo ""

# Step 2: Wait for Telegram API
echo "⏳ Step 2: Waiting 3 seconds for Telegram API to clear..."
sleep 3

echo ""

# Step 2.5: Preflight conflict check (fail fast if Telegram is locked by another poller)
echo "🧪 Step 2.5: Preflight check (Telegram polling lock)..."

# Activate venv if exists (needed for python-telegram-bot)
if [ -d "env" ]; then
    source env/bin/activate
fi

python preflight_check.py
PREFLIGHT_RC=$?

if [ $PREFLIGHT_RC -eq 3 ]; then
    echo ""
    echo "❌ Telegram 409 Conflict detected: another bot instance is polling right now."
    echo "   This is NOT fixed by restarting locally if another machine/server is running it."
    echo ""
    echo "Next actions:" 
    echo "  1) Make sure the bot isn't running anywhere else (VPS, Railway, Render, Heroku, Termux, another laptop)."
    echo "  2) If you can't find it, revoke the token in BotFather and update your .env (see TOKEN_FIX_URGENT.md)."
    exit 3
elif [ $PREFLIGHT_RC -ne 0 ]; then
    echo ""
    echo "❌ Preflight failed (code $PREFLIGHT_RC). Fix the issue above before starting."
    exit $PREFLIGHT_RC
fi

echo "✅ Preflight passed"

echo ""

# Step 3: Start bot
echo "🚀 Step 3: Starting bot..."

echo ""
echo "════════════════════════════════════════"
echo "   BOT IS STARTING"
echo "   Press Ctrl+C to stop"
echo "════════════════════════════════════════"
echo ""

# Start bot in foreground
python bot.py
