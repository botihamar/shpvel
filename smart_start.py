#!/usr/bin/env python3
"""
Smart Bot Starter - Waits for Telegram API to be ready before starting
"""
import asyncio
import sys
from telegram import Bot
from telegram.error import Conflict
from config import BOT_TOKEN

async def wait_for_api_ready():
    """Wait until Telegram API is ready to accept getUpdates"""
    print("🔍 Checking if Telegram API is ready...")
    
    bot = Bot(token=BOT_TOKEN)
    max_attempts = 30  # 30 attempts = 60 seconds max
    
    try:
        for attempt in range(1, max_attempts + 1):
            try:
                # Try to get updates with a very short timeout
                print(f"⏳ Attempt {attempt}/{max_attempts}...", end=" ")
                await bot.get_updates(timeout=1, limit=1)
                print("✅ API is ready!")
                return True
            except Conflict:
                print("❌ Still locked")
                if attempt < max_attempts:
                    await asyncio.sleep(2)  # Wait 2 seconds between attempts
                else:
                    print("\n❌ ERROR: Telegram API still reports conflict after 60 seconds")
                    print("\n🔍 Possible causes:")
                    print("1. Another bot instance is running in a different terminal/IDE")
                    print("2. Bot is running in Telegram Bot Father's test mode")
                    print("3. Another computer/server is running this bot")
                    print("\n💡 Solutions:")
                    print("• Check all terminals with: ps aux | grep bot.py")
                    print("• Close PyCharm/VSCode/other IDEs that might be running the bot")
                    print("• Wait 5-10 minutes for Telegram's API to fully clear")
                    print("• Revoke and regenerate your bot token in @BotFather")
                    return False
            except Exception as e:
                print(f"❌ Error: {e}")
                return False
        
        return False
        
    finally:
        await bot.close()

async def main():
    ready = await wait_for_api_ready()
    
    if ready:
        print("\n✅ Ready to start bot!")
        print("🚀 Starting in 2 seconds...")
        await asyncio.sleep(2)
        
        # Import and start the actual bot
        import subprocess
        subprocess.Popen(
            ["python", "bot.py"],
            stdout=sys.stdout,
            stderr=sys.stderr
        )
    else:
        print("\n❌ Cannot start bot - API not ready")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
