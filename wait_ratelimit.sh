#!/bin/bash
# Wait for Rate Limit - Shows countdown

echo "⏰ TELEGRAM RATE LIMIT DETECTED"
echo ""
echo "Your bot has been rate-limited by Telegram due to too many requests."
echo "This happens when you restart the bot many times in a short period."
echo ""
echo "⏳ You must wait approximately 8-10 minutes before starting the bot."
echo ""
echo "Countdown timer:"
echo ""

WAIT_TIME=500  # 500 seconds = ~8.3 minutes

for ((i=WAIT_TIME; i>0; i--)); do
    minutes=$((i / 60))
    seconds=$((i % 60))
    printf "\r⏰ Time remaining: %02d:%02d" $minutes $seconds
    sleep 1
done

echo ""
echo ""
echo "✅ Rate limit should be cleared now!"
echo "🚀 You can now start your bot with: ./start_bot.sh"
