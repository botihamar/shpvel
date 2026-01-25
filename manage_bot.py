#!/usr/bin/env python3
"""
Bot Manager - Utility to manage the Anonymous Chat Bot
Prevents multiple instances from running simultaneously
"""

import os
import sys
import signal
import psutil
import subprocess
from pathlib import Path

def get_bot_processes():
    """Find all running bot processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'python' in proc.info['name'].lower():
                if any('bot.py' in str(arg) for arg in cmdline):
                    processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes

def stop_all_bots():
    """Stop all running bot instances"""
    processes = get_bot_processes()
    
    if not processes:
        print("✅ No bot instances running")
        return True
    
    print(f"Found {len(processes)} bot instance(s) running:")
    for proc in processes:
        try:
            print(f"  - PID {proc.pid}: {' '.join(proc.cmdline())}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    print("\nStopping all instances...")
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=5)
            print(f"✅ Stopped PID {proc.pid}")
        except psutil.TimeoutExpired:
            print(f"⚠️  Force killing PID {proc.pid}")
            proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"❌ Could not stop PID {proc.pid}: {e}")
    
    return True

def check_bot_running():
    """Check if bot is already running"""
    processes = get_bot_processes()
    if processes:
        print("⚠️  Bot is already running!")
        print(f"   Found {len(processes)} instance(s):")
        for proc in processes:
            try:
                print(f"   - PID {proc.pid}")
            except:
                pass
        return True
    return False

def start_bot():
    """Start the bot (ensuring no other instance is running)"""
    if check_bot_running():
        print("\n❌ Cannot start bot: another instance is already running")
        print("   Use 'python manage_bot.py stop' to stop existing instances")
        return False
    
    print("🚀 Starting bot...")
    try:
        # Start bot in current terminal
        subprocess.run([sys.executable, 'bot.py'])
    except KeyboardInterrupt:
        print("\n\n✅ Bot stopped by user")
    
    return True

def restart_bot():
    """Restart the bot"""
    print("🔄 Restarting bot...\n")
    stop_all_bots()
    print()
    return start_bot()

def show_status():
    """Show bot status"""
    processes = get_bot_processes()
    
    print("=" * 50)
    print("  Anonymous Chat Bot - Status")
    print("=" * 50)
    
    if not processes:
        print("\n❌ Bot is NOT running")
    else:
        print(f"\n✅ Bot is RUNNING ({len(processes)} instance(s))")
        for proc in processes:
            try:
                print(f"\n   PID: {proc.pid}")
                print(f"   Status: {proc.status()}")
                print(f"   CPU: {proc.cpu_percent()}%")
                print(f"   Memory: {proc.memory_info().rss / 1024 / 1024:.1f} MB")
                
                # Show runtime
                import datetime
                create_time = datetime.datetime.fromtimestamp(proc.create_time())
                uptime = datetime.datetime.now() - create_time
                print(f"   Uptime: {uptime}")
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    
    print("\n" + "=" * 50)

def show_help():
    """Show help message"""
    print("""
Anonymous Chat Bot Manager

Usage: python manage_bot.py [command]

Commands:
  start    - Start the bot (if not already running)
  stop     - Stop all running bot instances
  restart  - Restart the bot
  status   - Show bot status
  help     - Show this help message

Examples:
  python manage_bot.py start
  python manage_bot.py stop
  python manage_bot.py status
  python manage_bot.py restart

Note: This script prevents multiple bot instances from running,
which causes the "Conflict: terminated by other getUpdates" error.
""")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        start_bot()
    elif command == 'stop':
        stop_all_bots()
    elif command == 'restart':
        restart_bot()
    elif command == 'status':
        show_status()
    elif command in ['help', '-h', '--help']:
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        print("   Use 'python manage_bot.py help' for usage")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
