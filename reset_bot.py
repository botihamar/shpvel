#!/usr/bin/env python3
"""
Reset Bot - Clears Telegram API locks
This script forcefully resets the bot's connection by calling dropPendingUpdates
"""
import asyncio
import sys
from telegram import Bot
from config import BOT_TOKEN

async def reset_bot():
    """Reset the bot by dropping all pending updates"""
    print("🔄 Resetting bot connection...")
    
    bot = Bot(token=BOT_TOKEN)
    
    try:
        # Delete webhook (if any)
        print("📡 Deleting webhook...")
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook deleted")
        
        # Wait a bit
        await asyncio.sleep(2)
        
        # Get bot info to verify connection
        me = await bot.get_me()
        print(f"✅ Bot verified: @{me.username}")
        
        print("\n🎉 Bot reset complete!")
        print("⏳ Wait 5-10 seconds, then run: ./start_bot.sh")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        # Close bot session
        await bot.close()

if __name__ == "__main__":
    asyncio.run(reset_bot())
