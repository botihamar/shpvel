# Frequently Asked Questions (FAQ)

## 📚 Table of Contents
1. [Getting Started](#getting-started)
2. [Configuration](#configuration)
3. [Features & Usage](#features--usage)
4. [VIP System](#vip-system)
5. [Moderation](#moderation)
6. [Technical Issues](#technical-issues)
7. [Deployment](#deployment)
8. [Advanced Topics](#advanced-topics)

---

## Getting Started

### Q: What do I need to start?
**A:** You need:
- Python 3.8 or higher
- A Telegram bot token from @BotFather
- Your Telegram user ID (get from @userinfobot)
- Optionally: Telegram channels for forced subscription

### Q: How do I get a bot token?
**A:** 
1. Message @BotFather on Telegram
2. Send `/newbot`
3. Choose a name and username
4. Copy the token (format: `1234567890:ABCdefGHI...`)

### Q: How do I find my user ID?
**A:** Message @userinfobot on Telegram. It will reply with your user ID.

### Q: Can I run this bot without programming knowledge?
**A:** Basic knowledge is helpful, but we've made it as simple as possible:
1. Run `python setup.py` for guided configuration
2. Follow the QUICKSTART.md guide
3. Most tasks are automated

---

## Configuration

### Q: What should I put in the .env file?
**A:** Example:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_IDS=123456789,987654321
REQUIRED_CHANNELS=@channel1,@channel2
VIP_PRICE_STARS=100
```

### Q: Can I have multiple admins?
**A:** Yes! Separate user IDs with commas:
```env
ADMIN_IDS=123456789,987654321,555666777
```

### Q: Do I need to use channel subscription?
**A:** No, it's optional. Leave `REQUIRED_CHANNELS` empty to skip:
```env
REQUIRED_CHANNELS=
```

### Q: How do I change the VIP price?
**A:** Edit the `.env` file:
```env
VIP_PRICE_STARS=50
```
Restart the bot for changes to take effect.

### Q: Can I use a custom database location?
**A:** Yes, set in `.env`:
```env
DATABASE_PATH=/path/to/your/database.db
```

---

## Features & Usage

### Q: How does anonymous matching work?
**A:** 
1. User sends `/search`
2. Bot adds them to a queue
3. When another user searches, they're paired
4. Messages relay through the bot
5. Neither user sees the other's identity

### Q: What information do users share?
**A:** 
- **Regular users:** Nothing (completely anonymous)
- **VIP users:** Can see partner's age and gender only

### Q: Can users block each other?
**A:** Not directly, but they can:
- Use `/next` to find a new partner
- Report bad behavior with ⛔ rating
- Admins can ban problematic users

### Q: What happens if a user leaves mid-chat?
**A:** 
- The other user is notified
- Chat ends automatically
- Both can search for new partners

### Q: Can users chat with the same person again?
**A:** Yes, but it's random. There's no friend/favorite system.

---

## VIP System

### Q: How does VIP payment work?
**A:** 
1. Users tap "Buy VIP" in `/vip` command
2. Telegram Stars invoice is sent
3. User pays through Telegram
4. Bot receives confirmation
5. VIP status granted automatically

### Q: What are Telegram Stars?
**A:** Telegram's in-app currency for digital purchases. Users buy Stars through Telegram and use them in bots.

### Q: How do I enable VIP payments?
**A:** 
1. Go to @BotFather
2. Select your bot → Payments
3. Choose "Use Telegram Stars"
4. Accept the terms

### Q: Can I test payments without real money?
**A:** Yes, Telegram provides a test environment. See [Telegram Payments Testing](https://core.telegram.org/bots/payments#testing-payments).

### Q: Can I manually grant VIP to users?
**A:** Yes! Use the admin command:
```
/givevip 123456789
```

### Q: Is VIP permanent or subscription-based?
**A:** Currently permanent. To add expiration, you'd need to modify the code to track VIP end dates.

### Q: Can I refund VIP purchases?
**A:** Telegram handles refunds. Contact their support for payment issues.

---

## Moderation

### Q: How do I ban a user?
**A:** Use the admin command:
```
/ban 123456789
```

### Q: What triggers automatic bans?
**A:** Users are auto-banned after receiving 3 ⛔ (scam/report) ratings from different users.

### Q: How do I unban someone?
**A:** Use the admin command:
```
/unban 123456789
```

### Q: Can I see chat messages as an admin?
**A:** No, messages aren't logged by default (privacy). You only see user IDs in reports.

### Q: How do I view reported users?
**A:** Use the admin command:
```
/reports
```

### Q: What gets filtered automatically?
**A:** 
- URLs and links
- @usernames
- Phone numbers (optional)
- Bad words (customizable list)

### Q: How do I add more bad words to the filter?
**A:** Edit `config.py`:
```python
BAD_WORDS = [
    'spam', 'scam', 'fraud',
    'yourword1', 'yourword2'
]
```

### Q: Can I disable link blocking?
**A:** Not recommended, but you can modify `bot.py` to remove the `contains_link()` check.

---

## Technical Issues

### Q: Bot doesn't respond to commands
**A:** Check:
1. Is `bot.py` running? (`python bot.py`)
2. Is the BOT_TOKEN correct in `.env`?
3. Any errors in the terminal?
4. Is your internet working?

### Q: "Import telegram could not be resolved"
**A:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Q: "Database is locked" error
**A:** 
- Another process might be using the database
- Kill other bot instances
- Check file permissions
- Consider using PostgreSQL for high concurrency

### Q: Channel subscription not verifying
**A:** Check:
1. Bot is admin of the channels
2. Channel usernames are correct (include @)
3. Channels are public or bot has access
4. Bot has "View Members" permission

### Q: VIP purchase not working
**A:** 
1. Ensure payments enabled in @BotFather
2. Check BOT_TOKEN is correct
3. Try with test payment first
4. Check logs for error messages

### Q: Users can't register (age validation fails)
**A:** 
- They must enter a number
- Age must be 18-100
- Check for typos
- They might need to restart with `/start`

### Q: "Permission denied" when starting bot
**A:** 
- Check file permissions
- Ensure Python has write access to directory
- Database directory needs write permission

---

## Deployment

### Q: Can I run this on my computer?
**A:** Yes, but:
- Computer must stay on
- Bot stops if you close terminal
- Better to use a server for 24/7 operation

### Q: What hosting do I need?
**A:** Any of these work:
- VPS (DigitalOcean, Linode, AWS EC2)
- PaaS (Heroku, Railway, Render)
- Your own server/computer
- Minimum: 1GB RAM, 10GB storage

### Q: How do I keep the bot running 24/7?
**A:** 
- **Linux:** Use systemd or screen
- **Windows:** Use Task Scheduler or run as service
- **Docker:** Use restart policies
- See QUICKSTART.md for details

### Q: How much does it cost to run?
**A:** 
- VPS: $5-20/month
- Free tiers: Heroku free tier (limited)
- Bandwidth: Minimal (<1GB/month for small bots)

### Q: Can I use free hosting?
**A:** Some options:
- Heroku (500 free hours/month)
- Railway (limited free tier)
- Oracle Cloud (always free tier)
- Your own computer (free but must stay on)

### Q: Do I need a domain name?
**A:** No, the bot works through Telegram. Domains are only needed for webhook setup (optional).

### Q: Should I use polling or webhooks?
**A:** 
- **Polling (current):** Simpler, no SSL needed, works everywhere
- **Webhooks:** More efficient, requires HTTPS domain, better for scale

---

## Advanced Topics

### Q: How many users can this bot handle?
**A:** 
- Current setup: 1,000-10,000 users
- With optimizations: 50,000+ users
- See ARCHITECTURE.md for scaling strategies

### Q: Can I add interest-based matching?
**A:** Not built-in, but you can:
1. Add an `interests` field to User table
2. Modify matching logic in `/search`
3. Match users with similar interests

### Q: Can I allow photo/video sharing?
**A:** 
- Currently text-only for safety
- To add media: Modify message handler to accept `filters.PHOTO`, etc.
- Warning: Requires image moderation to prevent abuse

### Q: How do I add more languages?
**A:** 
1. Create translation dictionaries
2. Store user's language preference
3. Replace text strings with translations
4. Consider using i18n library

### Q: Can I integrate with other bots?
**A:** Yes! The bot can:
- Forward messages to other bots
- Use inline mode
- Share data via APIs
- Integrate with external services

### Q: How do I migrate from SQLite to PostgreSQL?
**A:** 
1. Install `psycopg2`: `pip install psycopg2-binary`
2. Modify `database.py` to use PostgreSQL connection
3. Export SQLite data: `sqlite3 chatbot.db .dump`
4. Import to PostgreSQL: `psql -f dump.sql`

### Q: Can I run multiple bot instances?
**A:** 
- Not recommended with current architecture (shared in-memory state)
- For multiple instances, need Redis for shared state
- See ARCHITECTURE.md for details

### Q: How do I add analytics/tracking?
**A:** 
- Log events to database
- Use external analytics (Mixpanel, Amplitude)
- Create admin dashboard
- Export data to CSV/JSON

### Q: Can users delete their data?
**A:** To implement:
1. Add `/deleteaccount` command
2. Remove user from database
3. Comply with GDPR right to erasure

### Q: How do I backup the database?
**A:** 
```bash
# Manual backup
cp chatbot.db chatbot_backup_$(date +%Y%m%d).db

# Automated backup (cron)
0 2 * * * cp /path/to/chatbot.db /backups/chatbot_$(date +\%Y\%m\%d).db
```

---

## Troubleshooting Common Errors

### Error: "ModuleNotFoundError: No module named 'telegram'"
**Solution:** `pip install python-telegram-bot`

### Error: "telegram.error.Unauthorized: Forbidden: bot was blocked by the user"
**Solution:** Normal - user blocked the bot. Handle gracefully in code.

### Error: "sqlite3.OperationalError: database is locked"
**Solution:** Close other connections or use PostgreSQL

### Error: "telegram.error.BadRequest: Chat not found"
**Solution:** Check channel username is correct and bot is admin

### Error: "AttributeError: 'NoneType' object has no attribute"
**Solution:** User doesn't exist in database. Check registration flow.

---

## Best Practices

### For Users
- Be respectful to chat partners
- Don't share personal information
- Use report feature for bad behavior
- Read the rules before chatting

### For Admins
- Check reports daily
- Respond to user feedback
- Update bad word filter regularly
- Backup database weekly
- Monitor bot performance

### For Developers
- Keep dependencies updated
- Test before deploying changes
- Use environment variables
- Comment your code
- Follow Python PEP 8 style

---

## Still Have Questions?

1. **Check Documentation:**
   - README.md - Complete documentation
   - QUICKSTART.md - Setup guide
   - ARCHITECTURE.md - Technical details

2. **Search Issues:**
   - Check if others had same problem
   - Look at closed issues/PRs

3. **Debug:**
   - Check terminal for errors
   - Run `python test.py`
   - Enable debug logging

4. **Resources:**
   - [Telegram Bot API Docs](https://core.telegram.org/bots/api)
   - [python-telegram-bot Docs](https://python-telegram-bot.readthedocs.io/)
   - [Telegram Bot Community](https://t.me/BotDevelopment)

---

**Can't find your answer?**
- Review the code (it's well-commented!)
- Experiment in a test environment
- Consult Telegram's official documentation

**Remember:** The best way to learn is by doing! 🚀
