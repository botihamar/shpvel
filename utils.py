"""
Utility functions for Anonymous Chat Bot
"""

import re
from datetime import datetime
from typing import List, Optional

class MessageFilter:
    """Filter and validate messages"""
    
    @staticmethod
    def contains_url(text: str) -> bool:
        """Check if text contains any URLs or links"""
        patterns = [
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            r'www\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,}',
            r't\.me/[a-zA-Z0-9_]+',
            r'@[a-zA-Z0-9_]+',
            r'[a-zA-Z0-9-]+\.(com|net|org|io|co|ru|me|uk|de|fr|it|es|cn|jp|in|br|au|tv|xyz)',
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def contains_phone(text: str) -> bool:
        """Check if text contains phone numbers"""
        patterns = [
            r'\+?[1-9]\d{1,14}',  # International format
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
            r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',  # (123) 456-7890
        ]
        
        for pattern in patterns:
            if re.search(pattern, text):
                return True
        return False
    
    @staticmethod
    def contains_bad_words(text: str, bad_words: List[str]) -> bool:
        """Check if text contains bad words"""
        text_lower = text.lower()
        return any(word.lower() in text_lower for word in bad_words)
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Remove potentially harmful content from text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove invisible characters
        text = ''.join(char for char in text if char.isprintable() or char.isspace())
        
        return text.strip()


class RateLimiter:
    """Simple rate limiter for preventing spam"""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}  # {user_id: [timestamp1, timestamp2, ...]}
    
    def is_allowed(self, user_id: int) -> bool:
        """Check if user is allowed to make a request"""
        now = datetime.now().timestamp()
        
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Remove old requests outside time window
        self.requests[user_id] = [
            ts for ts in self.requests[user_id]
            if now - ts < self.time_window
        ]
        
        # Check if under limit
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True
        
        return False
    
    def get_remaining_time(self, user_id: int) -> Optional[int]:
        """Get remaining time until user can make request again"""
        if user_id not in self.requests or len(self.requests[user_id]) < self.max_requests:
            return 0
        
        now = datetime.now().timestamp()
        oldest = self.requests[user_id][0]
        remaining = self.time_window - (now - oldest)
        
        return max(0, int(remaining))


class TextFormatter:
    """Format text for better display"""
    
    @staticmethod
    def format_profile(user_data: dict) -> str:
        """Format user profile data"""
        gender_emoji = {
            'male': '♂️',
            'female': '♀️',
            'other': '⚧️'
        }.get(user_data.get('gender'), '❓')
        
        vip_status = '👑 VIP Member' if user_data.get('is_vip') else 'Regular User'
        
        text = (
            f"👤 Profile\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{gender_emoji} Gender: {user_data.get('gender', 'Unknown').capitalize()}\n"
            f"🎂 Age: {user_data.get('age', 'N/A')}\n"
            f"✨ Status: {vip_status}\n"
        )
        
        return text
    
    @staticmethod
    def format_stats(stats: dict) -> str:
        """Format bot statistics"""
        text = (
            f"📊 Bot Statistics\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👥 Total Users: {stats.get('total_users', 0):,}\n"
            f"👑 VIP Users: {stats.get('vip_users', 0):,}\n"
            f"🚫 Banned Users: {stats.get('banned_users', 0):,}\n"
            f"⭐ Total Ratings: {stats.get('total_ratings', 0):,}\n"
            f"⛔ Total Reports: {stats.get('total_reports', 0):,}\n"
        )
        
        return text
    
    @staticmethod
    def format_ratings(ratings: dict) -> str:
        """Format user ratings"""
        total = ratings.get('good', 0) + ratings.get('bad', 0) + ratings.get('scam', 0)
        
        if total == 0:
            return "No ratings yet"
        
        good_pct = (ratings.get('good', 0) / total) * 100 if total > 0 else 0
        
        text = (
            f"📊 Ratings ({total} total)\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👍 Good: {ratings.get('good', 0)} ({good_pct:.1f}%)\n"
            f"👎 Bad: {ratings.get('bad', 0)}\n"
            f"⛔ Reports: {ratings.get('scam', 0)}\n"
        )
        
        return text


class ValidationHelper:
    """Validate user inputs"""
    
    @staticmethod
    def validate_age(age: str) -> tuple[bool, Optional[int], Optional[str]]:
        """Validate age input
        
        Returns:
            (is_valid, age_value, error_message)
        """
        try:
            age_int = int(age)
            
            if age_int < 18:
                return False, None, "You must be at least 18 years old to use this bot."
            
            if age_int > 100:
                return False, None, "Please enter a realistic age."
            
            return True, age_int, None
            
        except ValueError:
            return False, None, "Please enter a valid number for your age."
    
    @staticmethod
    def validate_gender(gender: str) -> bool:
        """Validate gender input"""
        valid_genders = ['male', 'female', 'other']
        return gender.lower() in valid_genders
    
    @staticmethod
    def validate_user_id(user_id_str: str) -> tuple[bool, Optional[int], Optional[str]]:
        """Validate user ID input
        
        Returns:
            (is_valid, user_id, error_message)
        """
        try:
            user_id = int(user_id_str)
            
            if user_id <= 0:
                return False, None, "User ID must be positive."
            
            return True, user_id, None
            
        except ValueError:
            return False, None, "Invalid user ID format."


class TimeFormatter:
    """Format time and dates"""
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Format duration in seconds to human-readable format"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}m"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours}h"
        else:
            days = seconds // 86400
            return f"{days}d"
    
    @staticmethod
    def format_timestamp(timestamp: datetime) -> str:
        """Format timestamp to readable format"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days == 0:
            return "Today at " + timestamp.strftime("%H:%M")
        elif diff.days == 1:
            return "Yesterday at " + timestamp.strftime("%H:%M")
        elif diff.days < 7:
            return timestamp.strftime("%A at %H:%M")
        else:
            return timestamp.strftime("%d %b %Y at %H:%M")


class Logger:
    """Simple logging helper"""
    
    @staticmethod
    def log_chat_start(user1_id: int, user2_id: int):
        """Log when a chat starts"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Chat started: {user1_id} <-> {user2_id}")
    
    @staticmethod
    def log_chat_end(user1_id: int, user2_id: int, duration: int):
        """Log when a chat ends"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration_str = TimeFormatter.format_duration(duration)
        print(f"[{timestamp}] Chat ended: {user1_id} <-> {user2_id} (Duration: {duration_str})")
    
    @staticmethod
    def log_report(reporter_id: int, target_id: int, reason: str):
        """Log when a user is reported"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Report: User {target_id} reported by {reporter_id} ({reason})")
    
    @staticmethod
    def log_ban(user_id: int, reason: str = "Multiple reports"):
        """Log when a user is banned"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Ban: User {user_id} banned ({reason})")


def escape_markdown(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def is_admin(user_id: int, admin_ids: List[int]) -> bool:
    """Check if user is an admin"""
    return user_id in admin_ids
