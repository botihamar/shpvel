"""
Database module for Anonymous Chat Bot
Handles all database operations using SQLite
"""

import sqlite3
from datetime import datetime
import threading

class Database:
    def __init__(self, db_path='chatbot.db'):
        self.db_path = db_path
        self.local = threading.local()
        self.init_database()
    
    def get_connection(self):
        """Get thread-local database connection"""
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.local.conn.row_factory = sqlite3.Row
        return self.local.conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                gender TEXT NOT NULL,
                age INTEGER NOT NULL,
                is_vip BOOLEAN DEFAULT 0,
                is_banned BOOLEAN DEFAULT 0,
                subscribed BOOLEAN DEFAULT 0,
                language TEXT DEFAULT 'en',
                vip_expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # If upgrading an old DB, add `username` column if missing.
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
        except sqlite3.OperationalError:
            # Already exists
            pass
        
        # Add language column if missing
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
        except sqlite3.OperationalError:
            # Already exists
            pass
        
        # Add vip_expires_at column if missing
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN vip_expires_at TIMESTAMP")
        except sqlite3.OperationalError:
            # Already exists
            pass
        
        # Ratings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rater_id INTEGER NOT NULL,
                target_id INTEGER NOT NULL,
                rating_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rater_id) REFERENCES users(user_id),
                FOREIGN KEY (target_id) REFERENCES users(user_id)
            )
        ''')
        
        # Chat history table (optional, for logging)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER NOT NULL,
                user2_id INTEGER NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                FOREIGN KEY (user1_id) REFERENCES users(user_id),
                FOREIGN KEY (user2_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
    
    def create_user(self, user_id, gender, age, username=None, language='en'):
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, gender, age, subscribed, language)
            VALUES (?, ?, ?, ?, 1, ?)
        ''', (user_id, username, gender, age, language))
        
        conn.commit()
    
    def get_user_language(self, user_id):
        """Get user's preferred language."""
        user = self.get_user(user_id)
        if user and user.get('language'):
            return user['language']
        return 'en'
    
    def set_user_language(self, user_id, language):
        """Set user's preferred language."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
        conn.commit()

    def set_username(self, user_id, username):
        """Persist Telegram username (without @) for user_id."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))
        conn.commit()

    def get_user_by_username(self, username):
        """Get user by Telegram username (with or without leading @)."""
        if not username:
            return None
        normalized = username.strip()
        if normalized.startswith('@'):
            normalized = normalized[1:]
        normalized = normalized.lower()

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE LOWER(username) = ?', (normalized,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def get_user(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def update_user_subscription(self, user_id, subscribed):
        """Update user subscription status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET subscribed = ? WHERE user_id = ?
        ''', (subscribed, user_id))
        
        conn.commit()
    
    def set_vip_status(self, user_id, is_vip, days=30):
        """Set VIP status for user with expiration date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if is_vip:
            # Calculate expiration date (30 days from now by default)
            from datetime import timedelta
            expiration_date = datetime.now() + timedelta(days=days)
            cursor.execute('''
                UPDATE users SET is_vip = ?, vip_expires_at = ? WHERE user_id = ?
            ''', (is_vip, expiration_date, user_id))
        else:
            # Removing VIP status
            cursor.execute('''
                UPDATE users SET is_vip = ?, vip_expires_at = NULL WHERE user_id = ?
            ''', (is_vip, user_id))
        
        conn.commit()

    def update_gender(self, user_id, gender):
        """Update user's gender."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET gender = ? WHERE user_id = ?', (gender, user_id))
        conn.commit()

    def update_age(self, user_id, age):
        """Update user's age."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET age = ? WHERE user_id = ?', (age, user_id))
        conn.commit()
    
    def get_vip_expiration(self, user_id):
        """Get VIP expiration date for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT vip_expires_at FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row and row['vip_expires_at']:
            return datetime.fromisoformat(row['vip_expires_at'])
        return None
    
    def get_vip_days_remaining(self, user_id):
        """Get number of days remaining for VIP subscription"""
        expiration = self.get_vip_expiration(user_id)
        if not expiration:
            return None
        
        remaining = expiration - datetime.now()
        return max(0, remaining.days)
    
    def check_and_expire_vips(self):
        """Check and expire VIP subscriptions that have passed their expiration date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now()
        cursor.execute('''
            UPDATE users 
            SET is_vip = 0 
            WHERE is_vip = 1 
            AND vip_expires_at IS NOT NULL 
            AND vip_expires_at < ?
        ''', (now,))
        
        expired_count = cursor.rowcount
        conn.commit()
        return expired_count
    
    def ban_user(self, user_id):
        """Ban a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET is_banned = 1 WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
    
    def unban_user(self, user_id):
        """Unban a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET is_banned = 0 WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()

    def unban_all_users(self) -> int:
        """Unban all users.

        Returns:
            int: number of users updated
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_banned = 0 WHERE is_banned = 1')
        changed = cursor.rowcount
        conn.commit()
        return changed
    
    def add_rating(self, rater_id, target_id, rating_type):
        """Add a rating"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ratings (rater_id, target_id, rating_type)
            VALUES (?, ?, ?)
        ''', (rater_id, target_id, rating_type))
        
        conn.commit()
    
    def get_user_ratings(self, user_id):
        """Get ratings for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN rating_type = 'good' THEN 1 END) as good,
                COUNT(CASE WHEN rating_type = 'bad' THEN 1 END) as bad,
                COUNT(CASE WHEN rating_type = 'scam' THEN 1 END) as scam
            FROM ratings
            WHERE target_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        return {
            'good': row['good'],
            'bad': row['bad'],
            'scam': row['scam']
        }
    
    def get_scam_count(self, user_id):
        """Get number of scam reports for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM ratings
            WHERE target_id = ? AND rating_type = 'scam'
        ''', (user_id,))
        
        return cursor.fetchone()['count']
    
    def get_stats(self):
        """Get bot statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total users
        cursor.execute('SELECT COUNT(*) as count FROM users')
        total_users = cursor.fetchone()['count']
        
        # VIP users
        cursor.execute('SELECT COUNT(*) as count FROM users WHERE is_vip = 1')
        vip_users = cursor.fetchone()['count']
        
        # Banned users
        cursor.execute('SELECT COUNT(*) as count FROM users WHERE is_banned = 1')
        banned_users = cursor.fetchone()['count']
        
        # Total ratings
        cursor.execute('SELECT COUNT(*) as count FROM ratings')
        total_ratings = cursor.fetchone()['count']
        
        # Total reports
        cursor.execute("SELECT COUNT(*) as count FROM ratings WHERE rating_type = 'scam'")
        total_reports = cursor.fetchone()['count']
        
        return {
            'total_users': total_users,
            'vip_users': vip_users,
            'banned_users': banned_users,
            'total_ratings': total_ratings,
            'total_reports': total_reports
        }
    
    def get_recent_reports(self, limit=20):
        """Get recent scam reports"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT target_id, COUNT(*) as count
            FROM ratings
            WHERE rating_type = 'scam'
            GROUP BY target_id
            ORDER BY count DESC
            LIMIT ?
        ''', (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_users(self):
        """Get all users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id FROM users WHERE is_banned = 0')
        return [dict(row) for row in cursor.fetchall()]
    
    def log_chat_start(self, user1_id, user2_id):
        """Log chat start"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_history (user1_id, user2_id)
            VALUES (?, ?)
        ''', (user1_id, user2_id))
        
        conn.commit()
        return cursor.lastrowid
    
    def log_chat_end(self, chat_id):
        """Log chat end"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE chat_history
            SET ended_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (chat_id,))
        
        conn.commit()
