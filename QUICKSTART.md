# Quick Start Guide - Anonymous Chat Bot

## Step-by-Step Setup

### 1. Create Your Bot

1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow the prompts to choose a name and username
4. Copy the bot token (format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Get Your Admin User ID

1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. Copy your user ID (it's a number like `123456789`)

### 3. Create Channels (Optional)

If you want forced subscription:
1. Create Telegram channels (or use existing ones)
2. Make sure they have a username (like `@mychannel`)
3. Add your bot as administrator to each channel

### 4. Install Dependencies

```bash
cd "anonim bot"
pip install -r requirements.txt
```

Or install manually:
```bash
pip install python-telegram-bot==20.7 python-dotenv==1.0.0
```

### 5. Configure the Bot

**Option A: Use the setup script (Recommended)**
```bash
python setup.py
```
Follow the interactive prompts.

**Option B: Manual configuration**
1. Copy `.env.example` to `.env`
2. Edit `.env` with your values:

```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=your_user_id_here
REQUIRED_CHANNELS=@channel1,@channel2
VIP_PRICE_STARS=100
```

### 6. Set Bot Commands

1. Go to [@BotFather](https://t.me/botfather)
2. Send `/mybots` and select your bot
3. Click "Edit Bot" → "Edit Commands"
4. Paste this:

```
start - Start the bot
search - Find a chat partner
stop - End current chat
next - Find next partner
profile - View your profile
vip - Get VIP status
rules - View chat rules
help - Show help
```

### 7. Enable Payments (For VIP Feature)

1. In [@BotFather](https://t.me/botfather), select your bot
2. Go to "Payments"
3. Choose a payment provider
4. For Telegram Stars, select "Use Telegram Stars"
5. Agree to the terms

### 8. Run the Bot

```bash
python bot.py
```

You should see:
```
Bot started!
```

### 9. Test the Bot

1. Open your bot in Telegram
2. Send `/start`
3. Follow the registration process
4. Try commands like `/search`, `/profile`, `/vip`

## Common Issues

### Bot doesn't respond
- ✅ Check if `bot.py` is running
- ✅ Verify BOT_TOKEN is correct
- ✅ Check your internet connection

### "Channel subscription not working"
- ✅ Bot must be admin of the channels
- ✅ Channels must have usernames (starting with @)
- ✅ Check REQUIRED_CHANNELS format in .env

### "Import errors"
- ✅ Run `pip install -r requirements.txt`
- ✅ Make sure Python 3.8+ is installed
- ✅ Try creating a virtual environment

### "Database errors"
- ✅ Check write permissions in the directory
- ✅ Delete `chatbot.db` to reset database

## Usage Examples

### For Users

**Starting a chat:**
```
/start → Register → /search → Chat begins
```

**Ending a chat:**
```
/stop → Rate partner → Chat ends
```

**Finding next partner:**
```
/next → Rate current partner → New search begins
```

**Getting VIP:**
```
/vip → Buy VIP → Pay with Stars → VIP activated
```

### For Admins

**View statistics:**
```
/stats
```

**Ban a user:**
```
/ban 123456789
```

**Grant VIP manually:**
```
/givevip 123456789
```

**View reports:**
```
/reports
```

**Send announcement:**
```
/broadcast Hello everyone! New features coming soon!
```

## File Structure Explained

```
anonim bot/
├── bot.py              # Main bot logic and handlers
├── database.py         # Database operations (SQLite)
├── config.py           # Settings and configuration
├── requirements.txt    # Python dependencies
├── setup.py            # Interactive setup script
├── .env               # Your configuration (create this)
├── .env.example       # Example configuration
├── README.md          # Full documentation
├── QUICKSTART.md      # This file
└── chatbot.db         # Database (created automatically)
```

## Feature Overview

### Anonymous Chat
- Users register with gender and age
- Random pairing with other users
- Messages relayed through bot
- Complete anonymity maintained

### VIP System
- See partner's age and gender
- Purchase with Telegram Stars
- Admins can grant manually
- Lifetime membership

### Safety Features
- Links automatically blocked
- Bad word filtering
- Post-chat rating system
- Auto-ban after 3 reports
- Admin moderation tools

### Admin Controls
- `/stats` - Bot statistics
- `/ban` - Ban users
- `/unban` - Unban users
- `/givevip` - Grant VIP
- `/reports` - View reports
- `/broadcast` - Send announcements

## Customization Tips

### Change VIP Price
Edit `.env`:
```env
VIP_PRICE_STARS=50
```

### Add More Channels
Edit `.env`:
```env
REQUIRED_CHANNELS=@channel1,@channel2,@channel3,@channel4
```

### Add Bad Words Filter
Edit `config.py`:
```python
BAD_WORDS = [
    'spam', 'scam', 'fraud',
    'badword1', 'badword2'
]
```

### Change Age Restriction
Edit `bot.py`, find:
```python
if age < 18:
```
Change `18` to your preferred minimum age.

## Deployment Options

### Local (Development)
```bash
python bot.py
```

### Screen (Keeps running after logout)
```bash
screen -S chatbot
python bot.py
# Press Ctrl+A then D to detach
```

### Systemd Service (Linux)
Create `/etc/systemd/system/chatbot.service`:
```ini
[Unit]
Description=Anonymous Chat Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/anonim bot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable chatbot
sudo systemctl start chatbot
```

### Docker
```bash
docker build -t chatbot .
docker run -d --name chatbot --env-file .env chatbot
```

## Monitoring

### View Logs
```bash
tail -f bot.log
```

### Check Bot Status
```bash
ps aux | grep bot.py
```

### Database Queries
```bash
sqlite3 chatbot.db
> SELECT COUNT(*) FROM users;
> SELECT * FROM users WHERE is_vip = 1;
> .quit
```

## Getting Help

1. Read the full [README.md](README.md)
2. Check [Telegram Bot API Docs](https://core.telegram.org/bots/api)
3. Review [python-telegram-bot docs](https://python-telegram-bot.readthedocs.io/)

## Pro Tips

💡 **Test before launching**: Use a test bot first to ensure everything works

💡 **Backup your database**: Regularly backup `chatbot.db`

💡 **Monitor reports**: Check `/reports` daily for abusive users

💡 **Update rules**: Adjust bad words filter based on your community

💡 **Promote VIP**: Use `/broadcast` to inform users about VIP benefits

💡 **Grow channels**: Encourage quality content in required channels

---

**Ready to launch? Run `python bot.py` and start connecting people! 🚀**
