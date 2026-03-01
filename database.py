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
        
        # Users table with state machine
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                state TEXT DEFAULT 'IDLE' CHECK(state IN ('IDLE', 'SEARCHING', 'RESERVED', 'CHATTING', 'RATING')),
                search_target_gender TEXT CHECK(search_target_gender IN ('male', 'female', 'any') OR search_target_gender IS NULL),
                current_chat_id INTEGER,
                reserved_at TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        
        # Add state machine columns if missing
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN state TEXT DEFAULT 'IDLE' CHECK(state IN ('IDLE', 'SEARCHING', 'RESERVED', 'CHATTING', 'RATING'))")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN search_target_gender TEXT CHECK(search_target_gender IN ('male', 'female', 'any') OR search_target_gender IS NULL)")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN current_chat_id INTEGER")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN reserved_at TIMESTAMP")
        except sqlite3.OperationalError:
            pass
        
        # Add updated_at column (SQLite doesn't support DEFAULT CURRENT_TIMESTAMP in ALTER TABLE)
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN updated_at TIMESTAMP")
            # Populate with current timestamp for all existing rows
            cursor.execute("UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")
        except sqlite3.OperationalError:
            # Column already exists
            pass
        
        # Create search queue table for atomic operations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_queue (
                user_id INTEGER PRIMARY KEY,
                target_gender TEXT NOT NULL CHECK(target_gender IN ('male', 'female', 'any')),
                is_vip BOOLEAN DEFAULT 0,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Create chat sessions table for atomic matching
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER NOT NULL,
                user2_id INTEGER NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                user1_rated BOOLEAN DEFAULT 0,
                user2_rated BOOLEAN DEFAULT 0,
                FOREIGN KEY (user1_id) REFERENCES users(user_id),
                FOREIGN KEY (user2_id) REFERENCES users(user_id),
                CHECK (user1_id != user2_id)
            )
        ''')

        # Migration: older DBs had uniqueness constraints that block valid future chats.
        # - UNIQUE on user1_id/user2_id individually prevents a user from ever chatting again.
        # - UNIQUE(user1_id, user2_id) prevents the same pair from chatting again later.
        # We rebuild table without these UNIQUE constraints and rely on state machine + ended_at checks.
        try:
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='chat_sessions'")
            row = cursor.fetchone()
            create_sql = (row['sql'] if row else '') or ''
            if (
                'user1_id INTEGER NOT NULL UNIQUE' in create_sql
                or 'user2_id INTEGER NOT NULL UNIQUE' in create_sql
                or 'UNIQUE(user1_id, user2_id)' in create_sql
            ):
                cursor.execute('ALTER TABLE chat_sessions RENAME TO chat_sessions_old')
                cursor.execute('''
                    CREATE TABLE chat_sessions (
                        chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user1_id INTEGER NOT NULL,
                        user2_id INTEGER NOT NULL,
                        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ended_at TIMESTAMP,
                        user1_rated BOOLEAN DEFAULT 0,
                        user2_rated BOOLEAN DEFAULT 0,
                        FOREIGN KEY (user1_id) REFERENCES users(user_id),
                        FOREIGN KEY (user2_id) REFERENCES users(user_id),
                        CHECK (user1_id != user2_id)
                    )
                ''')
                cursor.execute('''
                    INSERT INTO chat_sessions (chat_id, user1_id, user2_id, started_at, ended_at, user1_rated, user2_rated)
                    SELECT chat_id, user1_id, user2_id, started_at, ended_at, user1_rated, user2_rated
                    FROM chat_sessions_old
                ''')
                cursor.execute('DROP TABLE chat_sessions_old')
        except Exception:
            # Don't block startup on migration edge-cases
            pass

        # Helpful indexes for lookups of active chats by either side
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_sessions_user1 ON chat_sessions(user1_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_sessions_user2 ON chat_sessions(user2_id)')
        
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
        
        # Active chats
        cursor.execute('''
            SELECT COUNT(*) as count 
            FROM users 
            WHERE state = 'CHATTING' AND current_chat_id IS NOT NULL
        ''')
        active_chats = cursor.fetchone()['count'] // 2  # Divide by 2 since both users are counted
        
        # Users in queue
        cursor.execute('SELECT COUNT(*) as count FROM search_queue')
        in_queue = cursor.fetchone()['count']
        
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
            'active_chats': active_chats,
            'in_queue': in_queue,
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

    # ==================== ATOMIC MATCHMAKING METHODS ====================
    
    def get_user_state(self, user_id):
        """Get user's current state"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT state, current_chat_id FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            return {'state': row['state'], 'chat_id': row['current_chat_id']}
        return None
    
    def atomic_join_queue(self, user_id, target_gender='any'):
        """
        Atomically join search queue.
        Returns (success: bool, message: str)
        Enforces: user must be in IDLE state, no duplicate queue entries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Start transaction
            conn.execute('BEGIN IMMEDIATE')
            
            # Check user state
            cursor.execute('SELECT state, is_banned FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if not row:
                conn.rollback()
                return (False, "User not registered")
            
            if row['is_banned']:
                conn.rollback()
                return (False, "User is banned")
            
            if row['state'] != 'IDLE':
                conn.rollback()
                return (False, f"Already {row['state'].lower()}")
            
            # Insert into queue (UNIQUE constraint prevents duplicates)
            cursor.execute('''
                INSERT INTO search_queue (user_id, target_gender, is_vip)
                SELECT ?, ?, is_vip FROM users WHERE user_id = ?
            ''', (user_id, target_gender, user_id))
            
            # Update user state to SEARCHING
            cursor.execute('''
                UPDATE users 
                SET state = 'SEARCHING', search_target_gender = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (target_gender, user_id))
            
            conn.commit()
            return (True, "Joined queue")
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            return (False, f"Already in queue: {str(e)}")
        except Exception as e:
            conn.rollback()
            return (False, f"Error: {str(e)}")
    
    def atomic_match(self, searcher_id, target_gender='any'):
        """
        Atomically find and match with a partner.
        Uses proper locking to prevent race conditions.
        
        Returns:
            (success: bool, partner_id: int | None, message: str)
        
        Algorithm:
        1. Find compatible candidate in queue (not self, matching gender filter)
        2. Lock candidate's row (prevents other matchers from taking same person)
        3. Create chat session
        4. Update both users to CHATTING state
        5. Remove both from queue
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            conn.execute('BEGIN IMMEDIATE')
            
            # Get searcher info
            cursor.execute('SELECT gender, is_vip FROM users WHERE user_id = ?', (searcher_id,))
            searcher_row = cursor.fetchone()
            if not searcher_row:
                conn.rollback()
                return (False, None, "Searcher not found")
            
            searcher_is_vip = searcher_row['is_vip']
            
            # Build filter query.
            # We must respect BOTH sides:
            # - searcher constraint: candidate.gender must match searcher target_gender (if specified)
            # - candidate constraint: searcher.gender must match candidate target_gender (if specified)
            # This guarantees that if user asked for `female` and there is no suitable female,
            # we simply return "No matching candidates" and the caller keeps/joins SEARCHING.
            gender_filter = ""
            mutual_filter = ""
            params = [searcher_id]

            if target_gender in ('male', 'female'):
                gender_filter = " AND u.gender = ?"
                params.append(target_gender)

            # Candidate's preference must accept the searcher's gender.
            # Allow q.target_gender='any'. Otherwise require exact match.
            mutual_filter = " AND (q.target_gender = 'any' OR q.target_gender = ?)"
            params.append(searcher_row['gender'])
            
            # Find candidate with row-level locking
            # Note: SQLite doesn't have SELECT FOR UPDATE, but BEGIN IMMEDIATE
            # gives us exclusive write lock on the entire database
            cursor.execute(f'''
                SELECT q.user_id, u.gender, u.age, u.is_vip
                FROM search_queue q
                JOIN users u ON q.user_id = u.user_id
                WHERE q.user_id != ?
                  AND u.state = 'SEARCHING'
                  AND u.is_banned = 0
                  {gender_filter}
                  {mutual_filter}
                ORDER BY q.is_vip DESC, q.joined_at ASC
                LIMIT 1
            ''', params)
            
            candidate_row = cursor.fetchone()
            if not candidate_row:
                conn.rollback()
                return (False, None, "No matching candidates")
            
            partner_id = candidate_row['user_id']
            
            # CRITICAL: Double-check partner is still SEARCHING (not already matched)
            cursor.execute('SELECT state FROM users WHERE user_id = ?', (partner_id,))
            check_row = cursor.fetchone()
            if not check_row or check_row['state'] != 'SEARCHING':
                conn.rollback()
                return (False, None, "Candidate no longer available")
            
            # Create chat session
            # Guard: ensure neither side currently has an active chat session.
            cursor.execute('''
                SELECT chat_id FROM chat_sessions
                WHERE ended_at IS NULL AND (user1_id = ? OR user2_id = ? OR user1_id = ? OR user2_id = ?)
                LIMIT 1
            ''', (searcher_id, searcher_id, partner_id, partner_id))
            if cursor.fetchone():
                conn.rollback()
                return (False, None, 'Candidate no longer available')

            cursor.execute('''
                INSERT INTO chat_sessions (user1_id, user2_id, started_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (searcher_id, partner_id))
            
            chat_id = cursor.lastrowid
            
            # Update both users to CHATTING
            cursor.execute('''
                UPDATE users
                SET state = 'CHATTING', current_chat_id = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id IN (?, ?)
            ''', (chat_id, searcher_id, partner_id))
            
            # Remove both from queue
            cursor.execute('DELETE FROM search_queue WHERE user_id IN (?, ?)', (searcher_id, partner_id))
            
            # Log to chat history
            cursor.execute('''
                INSERT INTO chat_history (user1_id, user2_id, started_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (searcher_id, partner_id))
            
            conn.commit()
            return (True, partner_id, f"Matched! Chat ID: {chat_id}")
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            return (False, None, f"Match conflict: {str(e)}")
        except Exception as e:
            conn.rollback()
            return (False, None, f"Error: {str(e)}")
    
    def atomic_leave_queue(self, user_id):
        """
        Atomically leave search queue.
        Returns (success: bool, message: str)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            conn.execute('BEGIN IMMEDIATE')
            
            # Remove from queue
            cursor.execute('DELETE FROM search_queue WHERE user_id = ?', (user_id,))
            
            # Update state to IDLE
            cursor.execute('''
                UPDATE users
                SET state = 'IDLE', search_target_gender = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ? AND state = 'SEARCHING'
            ''', (user_id,))
            
            conn.commit()
            return (True, "Left queue")
            
        except Exception as e:
            conn.rollback()
            return (False, f"Error: {str(e)}")
    
    def atomic_end_chat(self, user_id):
        """
        Atomically end current chat session.
        Idempotent: safe to call multiple times.
        Returns (success: bool, partner_id: int | None, message: str)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            conn.execute('BEGIN IMMEDIATE')
            
            # Get current chat info
            cursor.execute('SELECT state, current_chat_id FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if not row or row['state'] not in ('CHATTING', 'RATING'):
                conn.rollback()
                return (False, None, "Not in active chat")
            
            chat_id = row['current_chat_id']
            if not chat_id:
                conn.rollback()
                return (False, None, "No chat ID found")
            
            # Get partner from chat session
            cursor.execute('''
                SELECT user1_id, user2_id FROM chat_sessions WHERE chat_id = ?
            ''', (chat_id,))
            chat_row = cursor.fetchone()
            if not chat_row:
                conn.rollback()
                return (False, None, "Chat session not found")
            
            partner_id = chat_row['user2_id'] if chat_row['user1_id'] == user_id else chat_row['user1_id']
            
            # End chat session
            cursor.execute('''
                UPDATE chat_sessions
                SET ended_at = CURRENT_TIMESTAMP
                WHERE chat_id = ?
            ''', (chat_id,))
            
            # Update both users to IDLE
            cursor.execute('''
                UPDATE users
                SET state = 'IDLE', current_chat_id = NULL, search_target_gender = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE user_id IN (?, ?)
            ''', (user_id, partner_id))
            
            # Clean up any stale queue entries
            cursor.execute('DELETE FROM search_queue WHERE user_id IN (?, ?)', (user_id, partner_id))
            
            conn.commit()
            return (True, partner_id, "Chat ended")
            
        except Exception as e:
            conn.rollback()
            return (False, None, f"Error: {str(e)}")
    
    def atomic_next_partner(self, user_id, target_gender='any'):
        """
        Atomic /next operation: end current chat + start new search.
        This is the "super-operation" that prevents /next race conditions.
        
        Returns (success: bool, action: str, data: dict)
        action can be: 'matched', 'searching', 'error'
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            conn.execute('BEGIN IMMEDIATE')
            
            # Step 1: End current chat if exists
            # Important: don't trust `state` alone. If `current_chat_id` points to an active
            # session (ended_at IS NULL), we must close it, otherwise user can get stuck in
            # CHATTING forever and search will appear "broken".
            cursor.execute('SELECT state, current_chat_id FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if not row:
                conn.rollback()
                return (False, 'error', {'message': 'User not found'})
            
            # Clean up any existing state
            if row['current_chat_id']:
                chat_id = row['current_chat_id']

                # Only close if it's actually active.
                cursor.execute('''
                    SELECT user1_id, user2_id
                    FROM chat_sessions
                    WHERE chat_id = ? AND ended_at IS NULL
                ''', (chat_id,))
                chat_row = cursor.fetchone()
                if chat_row:
                    partner_id = chat_row['user2_id'] if chat_row['user1_id'] == user_id else chat_row['user1_id']

                    cursor.execute('''
                        UPDATE chat_sessions
                        SET ended_at = CURRENT_TIMESTAMP
                        WHERE chat_id = ? AND ended_at IS NULL
                    ''', (chat_id,))

                    # Update partner to IDLE (idempotent)
                    cursor.execute('''
                        UPDATE users
                        SET state = 'IDLE', current_chat_id = NULL, search_target_gender = NULL, updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    ''', (partner_id,))

            # Defensive cleanup: if there are any other active sessions that still reference this user, end them.
            cursor.execute('''
                UPDATE chat_sessions
                SET ended_at = CURRENT_TIMESTAMP
                WHERE ended_at IS NULL AND (user1_id = ? OR user2_id = ?)
            ''', (user_id, user_id))
            
            # Remove from queue if somehow stuck there
            cursor.execute('DELETE FROM search_queue WHERE user_id = ?', (user_id,))
            
            # Update user to IDLE first
            cursor.execute('''
                UPDATE users
                SET state = 'IDLE', current_chat_id = NULL, search_target_gender = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (user_id,))
            
            # Step 2: Try to match immediately
            cursor.execute('SELECT gender, is_vip FROM users WHERE user_id = ?', (user_id,))
            searcher_row = cursor.fetchone()
            
            gender_filter = ""
            mutual_filter = ""
            params = [user_id]
            if target_gender in ('male', 'female'):
                gender_filter = " AND u.gender = ?"
                params.append(target_gender)

            # Candidate's preference must accept the searcher's gender.
            mutual_filter = " AND (q.target_gender = 'any' OR q.target_gender = ?)"
            params.append(searcher_row['gender'])
            
            cursor.execute(f'''
                SELECT q.user_id, u.gender, u.age, u.is_vip
                FROM search_queue q
                JOIN users u ON q.user_id = u.user_id
                WHERE q.user_id != ?
                  AND u.state = 'SEARCHING'
                  AND u.is_banned = 0
                  {gender_filter}
                  {mutual_filter}
                ORDER BY q.is_vip DESC, q.joined_at ASC
                LIMIT 1
            ''', params)
            
            candidate_row = cursor.fetchone()
            
            if candidate_row:
                # Found match!
                partner_id = candidate_row['user_id']

                # Guard: partner might already be in an active chat (stale queue/state). If so, treat as no match.
                cursor.execute('''
                    SELECT chat_id FROM chat_sessions
                    WHERE ended_at IS NULL AND (user1_id = ? OR user2_id = ?)
                    LIMIT 1
                ''', (partner_id, partner_id))
                if cursor.fetchone():
                    candidate_row = None

            if candidate_row:
                partner_id = candidate_row['user_id']
                
                # Create chat session
                cursor.execute('''
                    INSERT INTO chat_sessions (user1_id, user2_id, started_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (user_id, partner_id))
                
                chat_id = cursor.lastrowid
                
                # Update both to CHATTING
                cursor.execute('''
                    UPDATE users
                    SET state = 'CHATTING', current_chat_id = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id IN (?, ?)
                ''', (chat_id, user_id, partner_id))
                
                # Remove from queue
                cursor.execute('DELETE FROM search_queue WHERE user_id IN (?, ?)', (user_id, partner_id))
                
                # Log
                cursor.execute('''
                    INSERT INTO chat_history (user1_id, user2_id, started_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (user_id, partner_id))
                
                conn.commit()
                
                # Get partner info
                partner_info = {
                    'user_id': partner_id,
                    'gender': candidate_row['gender'],
                    'age': candidate_row['age'],
                    'is_vip': candidate_row['is_vip']
                }
                
                return (True, 'matched', {'partner': partner_info, 'chat_id': chat_id})
            else:
                # No match, join queue
                cursor.execute('''
                    INSERT INTO search_queue (user_id, target_gender, is_vip)
                    SELECT ?, ?, is_vip FROM users WHERE user_id = ?
                ''', (user_id, target_gender, user_id))
                
                cursor.execute('''
                    UPDATE users
                    SET state = 'SEARCHING', search_target_gender = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (target_gender, user_id))
                
                conn.commit()
                return (True, 'searching', {'message': 'Searching for next partner'})
        
        except Exception as e:
            conn.rollback()
            return (False, 'error', {'message': f'Error: {str(e)}'})
