"""
Test script for Anonymous Chat Bot
Tests various components and functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_database():
    """Test database operations"""
    print("Testing database...")
    
    try:
        from database import Database
        
        db = Database(':memory:')  # Use in-memory database for testing
        
        # Test user creation
        db.create_user(12345, 'male', 25)
        user = db.get_user(12345)
        assert user is not None
        assert user['gender'] == 'male'
        assert user['age'] == 25
        print("  ✅ User creation works")
        
        # Test VIP status
        db.set_vip_status(12345, True)
        user = db.get_user(12345)
        assert user['is_vip'] == True
        print("  ✅ VIP status works")
        
        # Test ratings
        db.create_user(67890, 'female', 30)
        db.add_rating(12345, 67890, 'good')
        ratings = db.get_user_ratings(67890)
        assert ratings['good'] == 1
        print("  ✅ Rating system works")
        
        # Test ban
        db.ban_user(67890)
        user = db.get_user(67890)
        assert user['is_banned'] == True
        print("  ✅ Ban system works")
        
        print("✅ Database tests passed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}\n")
        return False


def test_utils():
    """Test utility functions"""
    print("Testing utilities...")
    
    try:
        from utils import MessageFilter, ValidationHelper, TextFormatter
        
        # Test URL detection
        assert MessageFilter.contains_url("Check out http://example.com")
        assert MessageFilter.contains_url("Visit www.google.com")
        assert MessageFilter.contains_url("Join @mychannel")
        assert not MessageFilter.contains_url("Hello world!")
        print("  ✅ URL detection works")
        
        # Test age validation
        valid, age, error = ValidationHelper.validate_age("25")
        assert valid and age == 25
        valid, age, error = ValidationHelper.validate_age("15")
        assert not valid
        print("  ✅ Age validation works")
        
        # Test text formatting
        user_data = {'gender': 'male', 'age': 25, 'is_vip': True}
        profile_text = TextFormatter.format_profile(user_data)
        assert '👑' in profile_text
        print("  ✅ Text formatting works")
        
        print("✅ Utility tests passed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Utility test failed: {e}\n")
        return False


def test_config():
    """Test configuration"""
    print("Testing configuration...")
    
    try:
        from config import BOT_TOKEN, ADMIN_IDS, VIP_PRICE_STARS
        
        if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE' or not BOT_TOKEN:
            print("  ⚠️  BOT_TOKEN not configured")
        else:
            print("  ✅ BOT_TOKEN found")
        
        if not ADMIN_IDS:
            print("  ⚠️  ADMIN_IDS not configured")
        else:
            print(f"  ✅ {len(ADMIN_IDS)} admin(s) configured")
        
        print(f"  ℹ️  VIP price: {VIP_PRICE_STARS} Stars")
        
        print("✅ Configuration loaded!\n")
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}\n")
        return False


def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    
    all_good = True
    
    # Test telegram
    try:
        import telegram
        print("  ✅ python-telegram-bot installed")
    except ImportError:
        print("  ❌ python-telegram-bot NOT installed")
        print("     Run: pip install python-telegram-bot")
        all_good = False
    
    # Test dotenv
    try:
        import dotenv
        print("  ✅ python-dotenv installed")
    except ImportError:
        print("  ❌ python-dotenv NOT installed")
        print("     Run: pip install python-dotenv")
        all_good = False
    
    # Test sqlite3 (should be built-in)
    try:
        import sqlite3
        print("  ✅ sqlite3 available")
    except ImportError:
        print("  ❌ sqlite3 NOT available")
        all_good = False
    
    if all_good:
        print("✅ All packages installed!\n")
    else:
        print("❌ Some packages missing. Install with: pip install -r requirements.txt\n")
    
    return all_good


def test_files():
    """Test if all required files exist"""
    print("Testing project files...")
    
    required_files = [
        'bot.py',
        'database.py',
        'config.py',
        'utils.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} missing")
            all_exist = False
    
    if os.path.exists('.env'):
        print(f"  ✅ .env (configured)")
    else:
        print(f"  ⚠️  .env (not found - run setup.py)")
    
    if all_exist:
        print("✅ All required files present!\n")
    else:
        print("❌ Some files missing!\n")
    
    return all_exist


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Anonymous Chat Bot - Test Suite")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("Files", test_files()))
    results.append(("Imports", test_imports()))
    results.append(("Config", test_config()))
    results.append(("Database", test_database()))
    results.append(("Utils", test_utils()))
    
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:.<30} {status}")
    
    print()
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("🎉 All tests passed! Your bot is ready to run.")
        print()
        print("Next steps:")
        print("1. Make sure .env is configured (run setup.py if needed)")
        print("2. Start the bot: python bot.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
    
    print("=" * 60)
    
    return all_passed


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
