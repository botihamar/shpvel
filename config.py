"""
Configuration file for Anonymous Chat Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file.
# Important: override=True ensures the .env value wins even if BOT_TOKEN was exported
# in the shell or injected by the IDE/launcher.
load_dotenv(override=True)

# Bot Token from BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Admin User IDs (comma-separated in .env, e.g., "123456789,987654321")
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]

# Required channels for subscription (comma-separated in .env, e.g., "@channel1,@channel2")
REQUIRED_CHANNELS = [ch.strip() for ch in os.getenv('REQUIRED_CHANNELS', '').split(',') if ch.strip()]

# VIP Price in Telegram Stars
VIP_PRICE_STARS = int(os.getenv('VIP_PRICE_STARS', '100'))

# Database path
DATABASE_PATH = os.getenv('DATABASE_PATH', 'chatbot.db')

# Bad words filter (optional - expand as needed)
BAD_WORDS = [
    'spam', 'scam', 'fraud'
    # Add more words as needed
]

# URL patterns for link detection
URL_PATTERNS = [
    r'http[s]?://',
    r'www\.',
    r't\.me',
    r'@\w+',
    r'[\w-]+\.(com|net|org|io|co|ru|me|uk|de|fr|it|es|cn|jp|in|br|au)'
]
