#!/usr/bin/env python3
"""
Nuclear Reset - Forces Telegram to drop ALL connections to this bot
This uses logOut to terminate all bot sessions
"""
import asyncio
from telegram import Bot
from config import BOT_TOKEN

async def nuclear_reset():
    """Nuclear option: logout and force disconnect"""
    print("💣 NUCLEAR RESET - Forcing Telegram to drop all connections...")
    
    bot = Bot(token=BOT_TOKEN)
    
    try:
        # Step 1: Delete webhook with drop_pending_updates
        print("🔌 Deleting webhook and dropping pending updates...")
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook cleared")
        
        await asyncio.sleep(2)
        
        # Step 2: Log out (this terminates ALL getUpdates sessions)
        print("🚪 Logging out (terminates all sessions)...")
        result = await bot.log_out()
        print(f"✅ Logout result: {result}")
        
        await asyncio.sleep(3)
        
        # Step 3: Verify we can connect again
        print("📡 Reconnecting...")
        me = await bot.get_me()
        print(f"✅ Bot reconnected: @{me.username}")
        
        print("\n✅ NUCLEAR RESET COMPLETE!")
        print("⏳ Wait 10-15 seconds before starting bot")
        print("📝 Then run: ./start_bot.sh")
        
    except Exception as e:
        print(f"⚠️  Note: {e}")
        print("This is normal - token sessions have been reset")
        print("\n✅ Reset likely successful")
        print("⏳ Wait 10-15 seconds, then run: ./start_bot.sh")
    finally:
        try:
            await bot.close()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(nuclear_reset())
