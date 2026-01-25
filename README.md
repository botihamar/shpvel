# Anonymous Telegram Chat Bot

A feature-rich Telegram bot that allows users to chat anonymously with random partners, complete with VIP features, content moderation, and admin controls.

## Features

### 🎭 Anonymous Chat System
- **Random Matching**: Users are paired randomly for one-on-one anonymous conversations
- **Complete Anonymity**: No personal information shared between chat partners
- **Easy Navigation**: Simple commands to start, stop, and switch between chat partners
- **Message Relay**: Bot acts as intermediary to maintain complete anonymity

### 👑 VIP Membership System
- **Partner Information**: VIP users can see their chat partner's age and gender
- **Telegram Stars Payment**: Seamless in-app purchase using Telegram's native currency
- **Manual VIP Grants**: Admins can grant VIP status manually
- **Exclusive Benefits**: Enhanced chat experience for premium users

### 📊 Rating System
- **Post-Chat Ratings**: Rate partners after each conversation
  - 👍 Good - Positive experience
  - 👎 Bad - Negative experience
  - ⛔ Report - Serious violations or scam attempts
- **Automated Moderation**: Users with 3+ reports are automatically banned
- **Behavior Tracking**: Encourages respectful interactions

### 🛡️ Content Moderation
- **Link Blocking**: Automatically prevents sharing of URLs and external contacts
- **Bad Word Filter**: Filters inappropriate language
- **Spam Prevention**: Rate limiting and anti-spam measures
- **Report System**: Users can flag inappropriate behavior

### 🔒 Channel Subscription Requirement
- **Forced Subscribe**: Users must join specified channels before using the bot
- **Automatic Verification**: Bot verifies channel membership via Telegram API
- **Growth Tool**: Helps grow partner channels and communities

### 👨‍💼 Admin Panel
- **User Management**: Ban/unban users
- **VIP Control**: Manually grant or revoke VIP status
- **Statistics**: View bot usage stats (users, chats, ratings)
- **Reports Dashboard**: Review user reports and take action
- **Broadcast**: Send announcements to all users

### 📱 User Commands
- `/start` - Start the bot and register
- `/search` - Find a random chat partner
- `/stop` - End current chat
- `/next` - Find next partner immediately
- `/profile` - View and edit your profile
- `/vip` - Learn about VIP membership
- `/rules` - View chat rules
- `/help` - Show help message

### 🔧 Admin Commands
- `/stats` - View bot statistics
- `/ban <user_id>` - Ban a user
- `/unban <user_id>` - Unban a user
- `/givevip <user_id>` - Grant VIP status
- `/reports` - View recent reports
- `/broadcast <message>` - Send message to all users

## Installation

### Prerequisites
- Python 3.8 or higher
- A Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))
- Telegram channels for forced subscription (optional)

### Setup Instructions

1. **Clone or download this project**
   ```bash
   cd "anonim bot"
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   
   Create a `.env` file in the project directory with the following:
   
   ```env
   # Your bot token from @BotFather
   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   
   # Admin user IDs (comma-separated)
   ADMIN_IDS=123456789,987654321
   
   # Required channels for subscription (comma-separated, use @username format)
   REQUIRED_CHANNELS=@yourchannel1,@yourchannel2
   
   # VIP price in Telegram Stars
   VIP_PRICE_STARS=100
   ```

4. **Set up your bot with BotFather**
   
   Send these commands to [@BotFather](https://t.me/botfather):
   
   ```
   /mybots
   [Select your bot]
   /setcommands
   
   Then paste:
   start - Start the bot
   search - Find a chat partner
   stop - End current chat
   next - Find next partner
   profile - View your profile
   vip - Get VIP status
   rules - View chat rules
   help - Show help
   ```

5. **Enable Payments (for VIP feature)**
   
   - Go to [@BotFather](https://t.me/botfather)
   - Select your bot → Payments
   - Connect a payment provider or use Telegram Stars
   - For Telegram Stars, ensure you have the latest API version

6. **Make your bot admin of required channels**
   
   For the forced subscription feature to work:
   - Add your bot to each required channel as an administrator
   - Bot needs permission to view channel members

## Running the Bot

```bash
python bot.py
```

The bot will start and begin polling for updates. You should see:
```
Bot started!
```

## Project Structure

```
anonim bot/
├── bot.py              # Main bot file with all handlers
├── database.py         # Database operations (SQLite)
├── config.py           # Configuration and settings
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .env.example       # Example environment file
├── README.md          # This file
└── chatbot.db         # SQLite database (created automatically)
```

## Database Schema

### Users Table
- `user_id` - Telegram user ID (PRIMARY KEY)
- `gender` - User's gender
- `age` - User's age
- `is_vip` - VIP status (boolean)
- `is_banned` - Ban status (boolean)
- `subscribed` - Channel subscription status (boolean)
- `created_at` - Registration timestamp

### Ratings Table
- `id` - Auto-increment ID
- `rater_id` - User who gave the rating
- `target_id` - User who received the rating
- `rating_type` - Type: 'good', 'bad', or 'scam'
- `created_at` - Rating timestamp

### Chat History Table
- `id` - Auto-increment ID
- `user1_id` - First user in pair
- `user2_id` - Second user in pair
- `started_at` - Chat start time
- `ended_at` - Chat end time

## Configuration Options

Edit `config.py` or use environment variables:

- `BOT_TOKEN` - Your Telegram bot token
- `ADMIN_IDS` - List of admin user IDs
- `REQUIRED_CHANNELS` - Channels users must join
- `VIP_PRICE_STARS` - VIP membership price in Telegram Stars
- `DATABASE_PATH` - Path to SQLite database file
- `BAD_WORDS` - List of filtered words
- `URL_PATTERNS` - Regex patterns for link detection

## How It Works

### Registration Flow
1. User sends `/start`
2. Bot checks channel subscriptions
3. User selects gender and enters age
4. Profile is created in database
5. User can now search for partners

### Chat Flow
1. User sends `/search`
2. Bot adds user to queue or pairs with waiting user
3. Messages are relayed between partners
4. Links and inappropriate content are filtered
5. Either user can `/stop` or `/next`
6. Both users rate each other after chat

### VIP Purchase Flow
1. User sends `/vip`
2. Bot shows VIP benefits and price
3. User clicks "Buy VIP"
4. Telegram Stars payment invoice is sent
5. After successful payment, VIP status is granted
6. VIP users see partner info in future chats

### Moderation Flow
1. Users rate partners after each chat
2. ⛔ Reports are logged and admins notified
3. Users with 3+ reports are auto-banned
4. Admins can view reports via `/reports`
5. Admins can manually ban/unban users

## Safety Features

- **Link Blocking**: Prevents sharing contact info
- **Bad Word Filter**: Blocks inappropriate language
- **Rating System**: Community-driven moderation
- **Auto-Ban**: Automatic ban after multiple reports
- **Admin Oversight**: Admins can trace and ban bad actors
- **Channel Verification**: Ensures legitimate users
- **Age Restriction**: Minimum age 18 years

## Monetization

The bot includes built-in monetization through:
- **VIP Subscriptions**: Paid via Telegram Stars
- **Channel Growth**: Required channel subscriptions
- **Admin Controls**: Easy management of paid features

## Deployment

### Local Development
```bash
python bot.py
```

### Production Deployment Options

**Option 1: VPS/Cloud Server**
```bash
# Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt

# Run with systemd or screen
screen -S chatbot
python3 bot.py
```

**Option 2: Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

**Option 3: Heroku**
1. Create `Procfile`: `worker: python bot.py`
2. Deploy via Git or GitHub integration

## Troubleshooting

### Bot doesn't respond
- Check if `BOT_TOKEN` is correct
- Ensure bot is running (`python bot.py`)
- Check logs for errors

### Channel subscription not working
- Bot must be admin of the channels
- Use correct format: `@channelname`
- Check bot has permission to view members

### Payments not working
- Ensure Telegram Stars are enabled for your bot
- Check provider token is empty (`""`) for Stars
- Test in Telegram's payment sandbox first

### Database errors
- Check file permissions for `chatbot.db`
- Delete database to reset (users will need to re-register)

## Security Considerations

- Keep `BOT_TOKEN` secret (never commit to Git)
- Regularly review reported users
- Monitor database for suspicious activity
- Implement rate limiting for spam prevention
- Consider adding CAPTCHA for new registrations
- Regularly update dependencies

## Future Enhancements

Potential features to add:
- [ ] Interest-based matching
- [ ] Gender preference filtering
- [ ] Profile photos (for VIP)
- [ ] Voice messages (with moderation)
- [ ] Chat history export
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile admin panel
- [ ] AI-powered content moderation
- [ ] Premium channel ads system

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational purposes. Feel free to modify and use for your own projects.

## Support

For issues or questions:
- Check this README first
- Review Telegram Bot API documentation
- Check Python-telegram-bot library docs

## Credits

Built with:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [SQLite](https://www.sqlite.org/) - Database
- [Telegram Bot API](https://core.telegram.org/bots/api) - Bot platform

## Disclaimer

This bot is designed for anonymous chatting. Users are responsible for their own behavior. Bot operators should:
- Clearly state terms of service
- Implement appropriate content moderation
- Comply with local laws and regulations
- Protect user privacy and data

---

**Made with ❤️ for the Telegram community**

Need help? Check out the [Telegram Bot API Documentation](https://core.telegram.org/bots)
