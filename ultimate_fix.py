#!/usr/bin/env python3
"""
ULTIMATE FIX - Forces complete disconnect and waits properly
"""
import asyncio
import sys
from telegram import Bot
from config import BOT_TOKEN

async def ultimate_fix():
    """Ultimate fix - logout, wait, verify"""
    print("🔥 ULTIMATE FIX - Complete Reset")
    print("=" * 50)
    
    bot = Bot(token=BOT_TOKEN)
    
    try:
        # Step 1: Logout
        print("\n🚪 Step 1: Logging out (terminates all sessions)...")
        try:
            await bot.log_out()
            print("✅ Logged out successfully")
        except Exception as e:
            print(f"⚠️  Logout returned: {e}")
            print("(This is usually fine)")
        
        await asyncio.sleep(2)
        
        # Step 2: Delete webhook
        print("\n🔌 Step 2: Clearing webhook...")
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            print("✅ Webhook cleared")
        except Exception as e:
            print(f"⚠️  {e}")
        
        await asyncio.sleep(2)
        
        # Step 3: Wait for API to clear
        print("\n⏳ Step 3: Waiting 30 seconds for Telegram API to fully clear...")
        print("(Telegram can take up to 30-60 seconds to release getUpdates lock)")
        
        for i in range(30, 0, -1):
            print(f"⏰ {i} seconds remaining...", end="\r")
            await asyncio.sleep(1)
        
        print("\n")
        
        # Step 4: Test connection
        print("🔍 Step 4: Testing connection...")
        try:
            me = await bot.get_me()
            print(f"✅ Bot verified: @{me.username}")
            print(f"✅ Bot ID: {me.id}")
            print(f"✅ Name: {me.first_name}")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n⚠️  WARNING: Bot may still be locked")
            print("Wait another 5 minutes before trying to start")
            sys.exit(1)
        
        # Step 5: Try getUpdates
        print("\n🎯 Step 5: Testing getUpdates...")
        try:
            await bot.get_updates(timeout=1, limit=1)
            print("✅ getUpdates works! Bot is ready!")
        except Exception as e:
            print(f"❌ getUpdates still blocked: {e}")
            print("\n💡 SOLUTION:")
            print("There IS another bot instance running somewhere!")
            print("\nCheck:")
            print("  1. Other terminal windows")
            print("  2. PyCharm/IDEs running the bot")
            print("  3. Another computer/server")
            print("  4. Telegram Bot Father test mode")
            print("\n Or wait 5-10 more minutes for Telegram to clear")
            sys.exit(1)
        
        print("\n" + "=" * 50)
        print("✅ ALL CHECKS PASSED!")
        print("=" * 50)
        print("\n🚀 Ready to start bot!")
        print("Run: ./safe_start.sh")
        
    finally:
        try:
            await bot.close()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(ultimate_fix())
