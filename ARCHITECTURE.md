# Technical Architecture - Anonymous Chat Bot

## System Overview

This document provides a detailed technical overview of the Anonymous Chat Bot architecture, design decisions, and implementation details.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Telegram API                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Bot Application                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Command Handlers                        │  │
│  │  /start /search /stop /profile /vip /rules          │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Message Processing                      │  │
│  │  • Link Detection  • Bad Word Filter                │  │
│  │  • Message Relay   • Rate Limiting                  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              State Management                        │  │
│  │  • Active Chats    • Search Queue                   │  │
│  │  • User Context    • Session Data                   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer (SQLite)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Users     │  │   Ratings    │  │ Chat History │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Bot Application (`bot.py`)

The main application file containing all bot logic and handlers.

**Key Classes:**
- `AnonymousChatBot`: Main bot class managing all functionality

**State Variables:**
- `active_chats`: Dictionary mapping user IDs to their chat partners
- `search_queue`: List of users waiting for a match

**Handler Types:**
- Command Handlers: Process bot commands (/start, /search, etc.)
- Message Handlers: Process regular text messages
- Callback Handlers: Process inline button clicks
- Payment Handlers: Process VIP purchases

### 2. Database Layer (`database.py`)

SQLite-based persistent storage with thread-safe connections.

**Tables Schema:**

```sql
-- Users table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    gender TEXT NOT NULL,
    age INTEGER NOT NULL,
    is_vip BOOLEAN DEFAULT 0,
    is_banned BOOLEAN DEFAULT 0,
    subscribed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ratings table
CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rater_id INTEGER NOT NULL,
    target_id INTEGER NOT NULL,
    rating_type TEXT NOT NULL,  -- 'good', 'bad', or 'scam'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rater_id) REFERENCES users(user_id),
    FOREIGN KEY (target_id) REFERENCES users(user_id)
);

-- Chat history table
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user1_id INTEGER NOT NULL,
    user2_id INTEGER NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    FOREIGN KEY (user1_id) REFERENCES users(user_id),
    FOREIGN KEY (user2_id) REFERENCES users(user_id)
);
```

**Key Methods:**
- `create_user()`: Register new user
- `get_user()`: Retrieve user data
- `add_rating()`: Record post-chat rating
- `ban_user()`: Ban problematic user
- `set_vip_status()`: Grant/revoke VIP

### 3. Configuration (`config.py`)

Centralized configuration using environment variables.

**Environment Variables:**
```python
BOT_TOKEN          # Telegram bot token
ADMIN_IDS          # Comma-separated admin user IDs
REQUIRED_CHANNELS  # Comma-separated channel usernames
VIP_PRICE_STARS    # VIP price in Telegram Stars
DATABASE_PATH      # Path to SQLite database
```

### 4. Utilities (`utils.py`)

Helper classes and functions for common operations.

**Key Classes:**
- `MessageFilter`: URL and content detection
- `RateLimiter`: Spam prevention
- `TextFormatter`: Message formatting
- `ValidationHelper`: Input validation

## Data Flow

### User Registration Flow

```
User sends /start
    ↓
Check channel subscriptions
    ↓
Request gender selection (inline buttons)
    ↓
Request age input (text)
    ↓
Validate age (18+)
    ↓
Create user in database
    ↓
Registration complete
```

### Chat Matching Flow

```
User sends /search
    ↓
Check if user is banned
    ↓
Check if already in chat
    ↓
Check search queue for waiting user
    ↓
If queue empty:
    Add user to queue
If queue has user:
    Create chat pair
    Store in active_chats
    Notify both users
    Show VIP info if applicable
```

### Message Relay Flow

```
User sends message
    ↓
Check if in active chat
    ↓
Get partner ID from active_chats
    ↓
Filter message:
    • Check for links → Block
    • Check for bad words → Block
    • Sanitize text
    ↓
Forward to partner
```

### Rating Flow

```
Chat ends (/stop or /next)
    ↓
Remove from active_chats
    ↓
Show rating buttons to both users
    ↓
User selects rating (👍/👎/⛔)
    ↓
Store in ratings table
    ↓
If ⛔ selected:
    Notify admins
    Check report count
    If count >= 3: Auto-ban user
```

### VIP Purchase Flow

```
User sends /vip
    ↓
Show VIP benefits and price
    ↓
User clicks "Buy VIP"
    ↓
Send Telegram invoice (XTR currency)
    ↓
User completes payment via Telegram
    ↓
Receive successful_payment callback
    ↓
Update user is_vip = True
    ↓
Confirm VIP activation
```

## Security Considerations

### 1. Anonymity Protection

**Implementation:**
- User IDs never exposed to chat partners
- Messages relayed through bot (no direct contact)
- Only VIP users see limited info (age/gender)
- No profile pictures or usernames shared

**Code Example:**
```python
# Messages are relayed, never direct
partner_id = self.active_chats[user_id]
await context.bot.send_message(partner_id, message_text)
```

### 2. Content Filtering

**Link Detection:**
```python
patterns = [
    r'http[s]?://',
    r'www\.',
    r't\.me/',
    r'@\w+',
    r'[\w-]+\.(com|net|org|...)'
]
```

**Bad Word Filter:**
- Configurable word list in `config.py`
- Case-insensitive matching
- Blocks message before relay

### 3. Spam Prevention

**Rate Limiting:**
```python
class RateLimiter:
    max_requests = 10  # Max requests
    time_window = 60   # Per 60 seconds
```

**Queue Management:**
- Users can only be in queue once
- Queue position cleaned on disconnect

### 4. User Accountability

**Reporting System:**
- All actions tied to Telegram user ID
- Admins can trace reported users
- Auto-ban after threshold (3 reports)
- Manual admin override available

### 5. Data Protection

**Database Security:**
- Local SQLite (no external exposure)
- Minimal data collection (only needed info)
- Thread-safe connections
- No message content stored (optional logging)

**Environment Variables:**
- Sensitive data in `.env` (not committed)
- Token and IDs never hardcoded

## API Integration

### Telegram Bot API

**Polling vs Webhook:**
- Current: Long polling (simple, no SSL needed)
- Production: Consider webhook for better performance

**Key API Methods Used:**
```python
# Messaging
send_message()
send_invoice()

# User Management
get_chat_member()  # Channel subscription check

# Payments
sendInvoice()      # Telegram Stars payment
successful_payment # Payment confirmation
```

### Payment Integration (Telegram Stars)

**Invoice Parameters:**
```python
{
    'title': 'VIP Membership',
    'description': 'Get VIP status...',
    'payload': 'vip_{user_id}',
    'provider_token': '',  # Empty for Stars
    'currency': 'XTR',     # Telegram Stars
    'prices': [LabeledPrice('VIP', amount)]
}
```

## Performance Considerations

### Scalability Limits

**Current Architecture:**
- Single-process Python application
- In-memory chat state (`active_chats`, `search_queue`)
- SQLite database (suitable for <100k users)

**Bottlenecks:**
- Message processing is synchronous
- Database writes can block
- In-memory state lost on restart

**Scaling Strategies:**

For 1k-10k concurrent users:
- Use PostgreSQL instead of SQLite
- Add Redis for state management
- Implement webhook instead of polling

For 10k+ concurrent users:
- Multiple bot instances (load balancing)
- Separate matching service
- Message queue (RabbitMQ/Kafka)
- Horizontal database scaling

### Memory Management

**Current Usage:**
- ~50 bytes per active chat pair
- ~100 bytes per queued user
- Database handles most persistent data

**Example:**
```python
1000 active chats = ~50 KB
1000 queued users = ~100 KB
Total in-memory: ~150 KB (negligible)
```

### Database Optimization

**Indexes:**
```sql
CREATE INDEX idx_ratings_target ON ratings(target_id);
CREATE INDEX idx_ratings_type ON ratings(rating_type);
CREATE INDEX idx_users_vip ON users(is_vip);
CREATE INDEX idx_users_banned ON users(is_banned);
```

**Query Optimization:**
- Use parameterized queries (SQL injection protection)
- Batch operations where possible
- Connection pooling for concurrent access

## Error Handling

### Network Errors

**Telegram API Failures:**
```python
try:
    await context.bot.send_message(...)
except TelegramError as e:
    logger.error(f"Failed to send: {e}")
    # Graceful degradation
```

### Database Errors

**Connection Issues:**
```python
def get_connection(self):
    if not hasattr(self.local, 'conn'):
        self.local.conn = sqlite3.connect(...)
    return self.local.conn
```

**Transaction Rollback:**
- Use `try/except` blocks
- Commit only on success
- Log errors for debugging

### User Input Validation

**Age Validation:**
```python
try:
    age = int(input_text)
    if age < 18: reject()
    if age > 100: reject()
except ValueError:
    request_valid_input()
```

## Testing Strategy

### Unit Tests

**Test Coverage:**
- Database operations (CRUD)
- Utility functions (filters, validators)
- Message processing logic

**Run Tests:**
```bash
python test.py
```

### Integration Tests

**Manual Testing:**
- Create multiple test accounts
- Test full chat flow
- Test VIP purchase (sandbox mode)
- Test admin commands

### Load Testing

**Simulate Users:**
```python
# Create bot API client
# Simulate multiple users
# Test concurrent chat matching
# Monitor performance metrics
```

## Deployment

### Development

```bash
python bot.py
```

### Production (Systemd)

```bash
sudo systemctl start chatbot
sudo systemctl enable chatbot  # Auto-start on boot
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

```bash
docker-compose up -d
```

### Monitoring

**Logs:**
```python
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
```

**Metrics to Track:**
- Active users
- Chat pairs formed
- Rating distribution
- Ban rate
- VIP conversion rate

## Future Enhancements

### Planned Features

1. **Advanced Matching**
   - Gender preference filtering
   - Age range preferences
   - Interest-based matching
   - Location-based matching (optional)

2. **Enhanced Moderation**
   - AI-powered content detection
   - Image/video support with moderation
   - Real-time admin dashboard
   - Appeal system for bans

3. **Premium Features**
   - Multiple VIP tiers
   - Custom profile themes
   - Priority queue
   - Extended chat history

4. **Analytics**
   - User engagement metrics
   - Conversion funnel analysis
   - A/B testing framework
   - Revenue analytics

### Technical Improvements

1. **Performance**
   - Migrate to PostgreSQL
   - Implement Redis caching
   - Use async/await throughout
   - Webhook instead of polling

2. **Architecture**
   - Microservices separation
   - Separate matching service
   - Message queue integration
   - CDN for media content

3. **Reliability**
   - Automated backups
   - Failover mechanisms
   - Rate limiting per user
   - Circuit breaker pattern

## Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document functions with docstrings
- Keep functions small and focused

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add: new feature description"

# Push and create PR
git push origin feature/new-feature
```

### Pull Request Guidelines

- Clear description of changes
- Test all affected functionality
- Update documentation
- No breaking changes without discussion

## License

This project is provided as-is for educational purposes.

## Support

For technical issues or questions:
- Review this documentation
- Check the [README.md](README.md)
- Consult [Telegram Bot API docs](https://core.telegram.org/bots/api)

---

**Last Updated:** December 2025
