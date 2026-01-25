"""
Anonymous Telegram Chat Bot
Main bot file with all handlers and logic
"""

import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    BotCommand,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
from database import Database
from config import BOT_TOKEN, ADMIN_IDS, REQUIRED_CHANNELS, VIP_PRICE_STARS
from translations import get_text
import re
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
GENDER, AGE = range(2)

# Initialize database
db = Database()

class AnonymousChatBot:
    def __init__(self):
        self.active_chats = {}  # {user_id: partner_id}
        self.search_queue = []  # Users looking for a chat
    
    def _get_user_lang(self, user_id: int) -> str:
        """Get user's preferred language, default to 'en'."""
        return db.get_user_language(user_id)
    
    def _detect_language(self, update: Update) -> str:
        """Detect language from Telegram client."""
        if update.effective_user and update.effective_user.language_code:
            lang_code = update.effective_user.language_code.lower()
            if lang_code.startswith('ru'):
                return 'ru'
            elif lang_code.startswith('hy'):
                return 'hy'
        return 'en'

    def _main_menu_keyboard(self, lang='en') -> ReplyKeyboardMarkup:
        """Persistent menu so users can tap buttons instead of typing commands."""
        keyboard = [
            [KeyboardButton(get_text("btn_search", lang)), KeyboardButton(get_text("btn_next", lang))],
            [KeyboardButton(get_text("btn_stop", lang)), KeyboardButton(get_text("btn_profile", lang))],
            [KeyboardButton(get_text("btn_vip", lang)), KeyboardButton(get_text("btn_rules", lang))],
            [KeyboardButton(get_text("btn_help", lang))],
        ]
        return ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
        )

    async def _send_main_menu_hint(self, update: Update, text: str, lang='en'):
        """Send a message with the persistent keyboard attached."""
        await update.effective_message.reply_text(
            text,
            reply_markup=self._main_menu_keyboard(lang),
        )

    def _resolve_target_user_id(self, raw_target: str):
        """Resolve admin target from either numeric id or @username.

        Returns:
            int | None: user_id if found
        """
        if raw_target is None:
            return None
        raw_target = raw_target.strip()
        if not raw_target:
            return None

        if raw_target.lstrip('-').isdigit():
            return int(raw_target)

        user_row = db.get_user_by_username(raw_target)
        if not user_row:
            return None
        return int(user_row['user_id'])
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        username = (update.effective_user.username or None)

        # Check if user needs to subscribe to channels
        if not await self.check_subscriptions(update, context):
            return

        # Check if user exists in database
        user = db.get_user(user_id)

        if not user:
            # New user - detect language and start registration
            lang = self._detect_language(update)
            context.user_data['language'] = lang
            
            await update.message.reply_text(
                get_text("welcome_new", lang),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(get_text("gender_male", lang), callback_data="gender_male")],
                    [InlineKeyboardButton(get_text("gender_female", lang), callback_data="gender_female")],
                ]),
            )
        else:
            # Existing user
            lang = self._get_user_lang(user_id)
            
            # Persist username for admin tools (/ban /unban /givevip by @username)
            if username and user.get('username') != username:
                db.set_username(user_id, username)

            # VIP: reset target choice each time user starts the bot, so next /search shows
            # Boy/Girl/Random options again.
            if user.get('is_vip'):
                context.user_data['vip_target_gender'] = None

            await self._send_main_menu_hint(
                update,
                get_text("welcome_back", lang),
                lang,
            )
    
    async def check_subscriptions(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Check if user has subscribed to required channels"""
        user_id = update.effective_user.id
        
        # Check if already verified
        user = db.get_user(user_id)
        if user and user['subscribed']:
            return True
        
        not_subscribed = []
        
        for channel in REQUIRED_CHANNELS:
            try:
                member = await context.bot.get_chat_member(channel, user_id)
                if member.status in ['left', 'kicked']:
                    not_subscribed.append(channel)
            except Exception as e:
                logger.error(f"Error checking subscription for {channel}: {e}")
                not_subscribed.append(channel)
        
        if not_subscribed:
            channel_links = '\n'.join([f"• {ch}" for ch in REQUIRED_CHANNELS])
            keyboard = [[InlineKeyboardButton("✅ I Subscribed", callback_data="verify_subscription")]]
            
            await update.message.reply_text(
                f"🔒 Please subscribe to our channels to use this bot:\n\n"
                f"{channel_links}\n\n"
                f"After subscribing, click the button below:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return False
        
        # Mark as subscribed
        if user:
            db.update_user_subscription(user_id, True)
        
        return True
    
    async def verify_subscription_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle subscription verification button"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        not_subscribed = []
        
        for channel in REQUIRED_CHANNELS:
            try:
                member = await context.bot.get_chat_member(channel, user_id)
                if member.status in ['left', 'kicked']:
                    not_subscribed.append(channel)
            except Exception as e:
                logger.error(f"Error checking subscription: {e}")
                not_subscribed.append(channel)
        
        if not_subscribed:
            await query.edit_message_text(
                "❗️ You haven't joined all required channels yet.\n"
                "Please subscribe to all channels and try again."
            )
        else:
            db.update_user_subscription(user_id, True)
            await query.edit_message_text(
                "✅ Subscription verified! You can now use the bot.\n\n"
                "Let's complete your registration..."
            )
            
            # Start registration
            await context.bot.send_message(
                chat_id=user_id,
                text="Please select your gender:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("♂️ Male", callback_data="gender_male")],
                    [InlineKeyboardButton("♀️ Female", callback_data="gender_female")],
                ])
            )
    
    async def gender_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle gender selection"""
        query = update.callback_query
        await query.answer()
        
        lang = context.user_data.get('language', 'en')
        
        gender = query.data.split('_')[1]
        if gender not in ("male", "female"):
            await query.edit_message_text(
                "❗️ Please select one of the available options: Male or Female."
            )
            return
        context.user_data['gender'] = gender
        
        gender_display = get_text(f"gender_{gender}", lang).replace("♂️ ", "").replace("♀️ ", "")
        
        await query.edit_message_text(
            get_text("enter_age", lang, gender=gender_display)
        )
        
        context.user_data['awaiting_age'] = True
    
    async def handle_age_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle age input during registration"""
        if not context.user_data.get('awaiting_age'):
            return
        
        lang = context.user_data.get('language', 'en')
        
        try:
            age = int(update.message.text)

            if age < 12 or age > 99:
                await update.message.reply_text(
                    get_text("age_invalid", lang)
                )
                return
            
            # Create user profile
            user_id = update.effective_user.id
            gender = context.user_data.get('gender')
            
            username = (update.effective_user.username or None)
            db.create_user(user_id, gender, age, username=username, language=lang)
            
            context.user_data['awaiting_age'] = False
            
            await update.message.reply_text(
                get_text("registration_complete", lang),
                reply_markup=self._main_menu_keyboard(lang),
            )
            
        except ValueError:
            await update.message.reply_text(
                get_text("age_invalid_number", lang)
            )
    
    async def search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /search command - find a chat partner"""
        user_id = update.effective_user.id
        msg = update.effective_message
        
        # Check if user is registered
        user = db.get_user(user_id)
        if not user:
            await msg.reply_text(
                "❗️ Please complete registration first by sending /start"
            )
            return
        
        # Check if user is banned
        if user['is_banned']:
            await msg.reply_text(
                "🚫 You have been banned from using this bot due to violations."
            )
            return
        
        # Check if already in a chat
        if user_id in self.active_chats:
            await msg.reply_text(
                "❗️ You're already in a chat. Use /stop to end it first."
            )
            return
        
        # Check if already searching
        if user_id in self.search_queue:
            await msg.reply_text(
                "⏳ You're already in the search queue. Please wait..."
            )
            return

        # VIP-only: allow choosing preferred partner gender before joining the queue.
        # Stored in memory only (per bot process) via context.user_data.
        if user.get('is_vip') and context.user_data.get('vip_target_gender') is None:
            keyboard = [
                [
                    InlineKeyboardButton("👦 Boy", callback_data="vip_search_male"),
                    InlineKeyboardButton("👧 Girl", callback_data="vip_search_female"),
                ],
                [InlineKeyboardButton("🎲 Random", callback_data="vip_search_any")],
            ]
            await msg.reply_text(
                "👑 VIP Search\n\nChoose who you want to match:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
            return
        
        # Try to find a partner from queue
        if self.search_queue:
            # VIP preference: 'male' | 'female' | 'any' (default)
            target_gender = context.user_data.get('vip_target_gender')
            if not target_gender:
                target_gender = 'any'

            partner_id = None
            if user.get('is_vip') and target_gender in ('male', 'female'):
                # Find the first queued user matching the preferred gender.
                # Note: this is O(n) but queue is expected to be small.
                for idx, candidate_id in enumerate(self.search_queue):
                    if candidate_id == user_id:
                        continue
                    candidate = db.get_user(candidate_id)
                    if candidate and (candidate.get('gender') == target_gender):
                        partner_id = candidate_id
                        # remove selected candidate from queue
                        self.search_queue.pop(idx)
                        break

            # Fallback: just take the first person in queue.
            if partner_id is None:
                partner_id = self.search_queue.pop(0)
            
            # Make sure partner is not the same user
            if partner_id == user_id:
                self.search_queue.append(user_id)
                await msg.reply_text(
                    "🔍 Searching for a chat partner..."
                )
                return

            # If VIP requested a specific gender but we ended up matching a different one (fallback),
            # keep UX transparent.
            if user.get('is_vip') and target_gender in ('male', 'female'):
                partner = db.get_user(partner_id)
                if partner and partner.get('gender') != target_gender:
                    await msg.reply_text(
                        "ℹ️ No preferred match found right now — matched randomly instead."
                    )
            
            # Create chat pair
            self.active_chats[user_id] = partner_id
            self.active_chats[partner_id] = user_id
            
            # Get partner info for VIP users
            partner = db.get_user(partner_id)
            user_is_vip = user['is_vip']
            partner_is_vip = partner['is_vip']
            
            # Notify both users
            user_message = "🔹 You are now connected to a partner! Say hi!"
            partner_message = "🔹 You are now connected to a partner! Say hi!"
            
            if user_is_vip:
                gender_emoji = "♂️" if partner['gender'] == 'male' else "♀️" if partner['gender'] == 'female' else "⚧️"
                user_message += f"\n\n👑 VIP Info: {gender_emoji} {partner['gender'].capitalize()}, {partner['age']} years old"
            
            if partner_is_vip:
                gender_emoji = "♂️" if user['gender'] == 'male' else "♀️" if user['gender'] == 'female' else "⚧️"
                partner_message += f"\n\n👑 VIP Info: {gender_emoji} {user['gender'].capitalize()}, {user['age']} years old"
            
            await msg.reply_text(user_message)
            await context.bot.send_message(partner_id, partner_message)
            
        else:
            # Add to queue
            self.search_queue.append(user_id)
            await msg.reply_text(
                "🔍 Searching for a chat partner...\n"
                "You'll be notified when someone is found."
            )

    async def vip_search_choice_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """VIP-only: handle gender choice before searching."""
        query = update.callback_query
        await query.answer()

        choice = query.data
        if choice == "vip_search_male":
            context.user_data['vip_target_gender'] = 'male'
            label = "Boy"
        elif choice == "vip_search_female":
            context.user_data['vip_target_gender'] = 'female'
            label = "Girl"
        else:
            context.user_data['vip_target_gender'] = 'any'
            label = "Random"

        await query.edit_message_text(
            f"👑 VIP Search preference saved: {label}\n\nStarting search..."
        )

        # Continue with the normal search flow.
        # NOTE: callback queries don't have `update.message`, so `search()` uses
        # `update.effective_message` for replies.
        await self.search(update, context)
    
    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stop command - end current chat"""
        user_id = update.effective_user.id

        # VIP: force choice again next time they search.
        # (We clear it on /stop so user can pick Boy/Girl/Random again.)
        if context.user_data.get('vip_target_gender') is not None:
            context.user_data['vip_target_gender'] = None

        # If user is searching, cancel search.
        if user_id in self.search_queue:
            try:
                self.search_queue.remove(user_id)
            except ValueError:
                pass
            await update.message.reply_text(
                "🛑 Search cancelled.\nUse /search when you want to find a partner again."
            )
            return
        
        if user_id not in self.active_chats:
            await update.message.reply_text(
                "❗️ You're not in an active chat."
            )
            return
        
        partner_id = self.active_chats[user_id]
        
        # End chat
        del self.active_chats[user_id]
        del self.active_chats[partner_id]
        
        # Show rating to both users
        await self.show_rating(update, context, user_id, partner_id)
        await self.show_rating_to_user(context, partner_id, user_id)
        
        # Notify partner
        await context.bot.send_message(
            partner_id,
            "🔸 Your partner has left the chat.\n\n"
            "Use /search to find a new partner."
        )

    async def sharelink(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Share your Telegram @username / t.me link with your current partner (consent-based)."""
        user_id = update.effective_user.id

        if user_id not in self.active_chats:
            await update.message.reply_text(
                "❗️ You're not in an active chat. Use /search to find a partner first."
            )
            return

        username = update.effective_user.username
        if not username:
            await update.message.reply_text(
                "❗️ You don't have a Telegram username set.\n\n"
                "Set one in Telegram Settings → Username, then try /sharelink again."
            )
            return

        # Ask for confirmation to avoid accidental doxxing.
        keyboard = [[
            InlineKeyboardButton("✅ Share", callback_data="sharelink_confirm"),
            InlineKeyboardButton("❌ Cancel", callback_data="sharelink_cancel"),
        ]]
        await update.message.reply_text(
            f"🔗 Share your Telegram link with your partner?\n\n"
            f"This will send: https://t.me/{username}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    async def sharelink_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle sharelink confirmation/cancel buttons."""
        query = update.callback_query
        await query.answer()

        user_id = update.effective_user.id
        action = query.data

        if action == "sharelink_cancel":
            await query.edit_message_text("❌ Share cancelled.")
            return

        if user_id not in self.active_chats:
            await query.edit_message_text(
                "❗️ You're not in an active chat anymore. Use /search to find a partner."
            )
            return

        username = update.effective_user.username
        if not username:
            await query.edit_message_text(
                "❗️ You don't have a Telegram username set.\n\n"
                "Set one in Telegram Settings → Username, then try /sharelink again."
            )
            return

        partner_id = self.active_chats[user_id]
        link = f"https://t.me/{username}"

        await context.bot.send_message(
            partner_id,
            f"🔗 Your partner shared their Telegram: @{username}\n{link}"
        )
        await query.edit_message_text("✅ Your Telegram link was shared with your partner.")
    
    async def next_partner(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /next command - find next partner"""
        user_id = update.effective_user.id

        # VIP: force choice again next time they search.
        if context.user_data.get('vip_target_gender') is not None:
            context.user_data['vip_target_gender'] = None
        
        if user_id in self.active_chats:
            # End current chat first
            partner_id = self.active_chats[user_id]
            del self.active_chats[user_id]
            del self.active_chats[partner_id]
            
            # Show rating
            await self.show_rating(update, context, user_id, partner_id)
            await self.show_rating_to_user(context, partner_id, user_id)
            
            # Notify partner
            await context.bot.send_message(
                partner_id,
                "🔸 Your partner has left the chat.\n\n"
                "Use /search to find a new partner."
            )
        
        # Start new search
        await self.search(update, context)
    
    async def show_rating(self, update: Update, context: ContextTypes.DEFAULT_TYPE, rater_id: int, target_id: int):
        """Show rating buttons to user"""
        keyboard = [
            [
                InlineKeyboardButton("👍 Good", callback_data=f"rate_good_{target_id}"),
                InlineKeyboardButton("👎 Bad", callback_data=f"rate_bad_{target_id}"),
                InlineKeyboardButton("⛔ Report", callback_data=f"rate_scam_{target_id}")
            ]
        ]
        
        await update.message.reply_text(
            "Please rate your chat partner:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def show_rating_to_user(self, context: ContextTypes.DEFAULT_TYPE, rater_id: int, target_id: int):
        """Show rating buttons to a user via bot message"""
        keyboard = [
            [
                InlineKeyboardButton("👍 Good", callback_data=f"rate_good_{target_id}"),
                InlineKeyboardButton("👎 Bad", callback_data=f"rate_bad_{target_id}"),
                InlineKeyboardButton("⛔ Report", callback_data=f"rate_scam_{target_id}")
            ]
        ]
        
        await context.bot.send_message(
            rater_id,
            "Please rate your chat partner:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def rating_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle rating button press"""
        query = update.callback_query
        await query.answer()
        
        rater_id = query.from_user.id
        parts = query.data.split('_')
        rating_type = parts[1]  # good, bad, or scam
        target_id = int(parts[2])
        
        # Record rating
        db.add_rating(rater_id, target_id, rating_type)
        
        if rating_type == 'scam':
            # Notify admins
            scam_count = db.get_scam_count(target_id)
            for admin_id in ADMIN_IDS:
                await context.bot.send_message(
                    admin_id,
                    f"⚠️ REPORT: User {target_id} was reported for scam/abuse\n"
                    f"Total reports: {scam_count}\n"
                    f"Reported by: {rater_id}"
                )
            
            # Auto-ban if too many reports
            if scam_count >= 3:
                db.ban_user(target_id)
                await context.bot.send_message(
                    target_id,
                    "🚫 You have been banned due to multiple reports of misconduct."
                )
                
                for admin_id in ADMIN_IDS:
                    await context.bot.send_message(
                        admin_id,
                        f"🚫 User {target_id} has been automatically banned (3+ reports)"
                    )
            
            await query.edit_message_text(
                "⛔ Thank you for your report. Our team will review this case."
            )
        else:
            await query.edit_message_text(
                f"Thank you for rating your partner! ({rating_type})"
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages - relay to chat partner"""
        user_id = update.effective_user.id

        # Profile edit: age input
        if context.user_data.get('awaiting_age_edit'):
            try:
                age = int(update.message.text)
                if age < 12 or age > 99:
                    await update.message.reply_text(
                        "❗️ Age must be between 12 and 99. Please enter your age again:"
                    )
                    return

                db.update_age(user_id, age)
                context.user_data['awaiting_age_edit'] = False
                await update.message.reply_text(
                    "✅ Age updated!\n\nSend /profile to view your updated profile."
                )
            except ValueError:
                await update.message.reply_text("❗️ Please enter a valid number (12–99):")
            return
        
        # Check if awaiting age input
        if context.user_data.get('awaiting_age'):
            await self.handle_age_input(update, context)
            return
        
        # Check if in active chat
        if user_id not in self.active_chats:
            await update.message.reply_text(
                "❗️ You're not in an active chat.\n"
                "Use /search to find a partner."
            )
            return
        
        partner_id = self.active_chats[user_id]
        message_text = update.message.text
        
        # Check for links
        if self.contains_link(message_text):
            await update.message.reply_text(
                "🚫 Links are not allowed in this chat."
            )
            return
        
        # Check for bad words (basic filter)
        if self.contains_bad_words(message_text):
            await update.message.reply_text(
                "🚫 Please keep the conversation respectful."
            )
            return
        
        # Forward message to partner
        try:
            await context.bot.send_message(partner_id, message_text)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            await update.message.reply_text(
                "❗️ Failed to send message. Your partner may have left."
            )
    
    def contains_link(self, text: str) -> bool:
        """Check if text contains links"""
        url_pattern = re.compile(
            r'http[s]?://|www\.|t\.me|@\w+|[\w-]+\.(com|net|org|io|co|ru|me)'
        )
        return bool(url_pattern.search(text.lower()))
    
    def contains_bad_words(self, text: str) -> bool:
        """Check if text contains bad words (basic filter)"""
        # Add your blacklist here
        bad_words = ['spam', 'scam']  # Expand this list as needed
        text_lower = text.lower()
        return any(word in text_lower for word in bad_words)
    
    async def profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command"""
        user_id = update.effective_user.id
        user = db.get_user(user_id)

        if not user:
            await update.effective_message.reply_text(
                "❗️ Please complete registration first by sending /start"
            )
            return

        gender_emoji = (
            "♂️" if user["gender"] == "male" else "♀️" if user["gender"] == "female" else "⚧️"
        )
        vip_status = "👑 VIP Member" if user["is_vip"] else "Regular User"

        ratings = db.get_user_ratings(user_id)

        profile_text = (
            f"👤 Your Profile\n\n"
            f"{gender_emoji} Gender: {user['gender'].capitalize()}\n"
            f"🎂 Age: {user['age']}\n"
            f"✨ Status: {vip_status}\n\n"
            f"📊 Ratings Received:\n"
            f"👍 Good: {ratings['good']}\n"
            f"👎 Bad: {ratings['bad']}\n"
            f"⛔ Reports: {ratings['scam']}"
        )

        keyboard = [[InlineKeyboardButton("✏️ Edit Profile", callback_data="edit_profile")]]
        await update.effective_message.reply_text(
            profile_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    async def edit_profile_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show profile edit menu."""
        query = update.callback_query
        await query.answer()

        keyboard = [
            [
                InlineKeyboardButton("♂️ Male", callback_data="edit_gender_male"),
                InlineKeyboardButton("♀️ Female", callback_data="edit_gender_female"),
            ],
            [InlineKeyboardButton("🎂 Edit Age", callback_data="edit_age")],
            [InlineKeyboardButton("⬅️ Back", callback_data="edit_back_profile")],
        ]

        await query.edit_message_text(
            "✏️ Edit Profile\n\nChoose what you want to change:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    async def edit_profile_gender_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle gender change from edit profile menu."""
        query = update.callback_query
        await query.answer()

        user_id = update.effective_user.id
        gender = query.data.split('_')[-1]  # male|female
        if gender not in ("male", "female"):
            await query.edit_message_text("❗️ Invalid gender choice.")
            return

        db.update_gender(user_id, gender)
        await query.edit_message_text(
            f"✅ Gender updated to: {gender.capitalize()}\n\nSend /profile to view your updated profile."
        )

    async def edit_profile_age_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start age edit: next text message will be treated as new age."""
        query = update.callback_query
        await query.answer()

        context.user_data['awaiting_age_edit'] = True
        await query.edit_message_text(
            "🎂 Enter your new age (12–99):\n\nSend a number as a message."
        )

    async def edit_profile_back_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Go back to profile view from edit menu."""
        query = update.callback_query
        await query.answer()

        user_id = update.effective_user.id
        user = db.get_user(user_id)
        if not user:
            await query.edit_message_text("❗️ Please complete registration first by sending /start")
            return

        gender_emoji = (
            "♂️" if user["gender"] == "male" else "♀️" if user["gender"] == "female" else "⚧️"
        )
        vip_status = "👑 VIP Member" if user["is_vip"] else "Regular User"
        ratings = db.get_user_ratings(user_id)
        profile_text = (
            f"👤 Your Profile\n\n"
            f"{gender_emoji} Gender: {user['gender'].capitalize()}\n"
            f"🎂 Age: {user['age']}\n"
            f"✨ Status: {vip_status}\n\n"
            f"📊 Ratings Received:\n"
            f"👍 Good: {ratings['good']}\n"
            f"👎 Bad: {ratings['bad']}\n"
            f"⛔ Reports: {ratings['scam']}"
        )

        keyboard = [[InlineKeyboardButton("✏️ Edit Profile", callback_data="edit_profile")]]
        await query.edit_message_text(
            profile_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    
    async def vip_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /vip command"""
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        if user and user['is_vip']:
            await update.message.reply_text(
                "👑 You already have VIP status!\n\n"
                "VIP Benefits:\n"
                "• See your partner's age and gender\n"
                "• Priority matching\n"
                "• Special VIP badge"
            )
            return
        
        keyboard = [
            [InlineKeyboardButton(f"⭐ Buy VIP for {VIP_PRICE_STARS} Stars", callback_data="buy_vip")]
        ]
        
        await update.message.reply_text(
            "👑 VIP Membership Benefits:\n\n"
            "✅ See your partner's age and gender during chats\n"
            "✅ Priority matching in the queue\n"
            "✅ Special VIP badge in your profile\n"
            "✅ Support the bot development\n\n"
            f"💰 Price: {VIP_PRICE_STARS} Telegram Stars\n\n"
            "Upgrade now to enhance your anonymous chat experience!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def buy_vip_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle VIP purchase button"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        # Send invoice
        await context.bot.send_invoice(
            chat_id=user_id,
            title="VIP Membership",
            description="Get VIP status with exclusive benefits!",
            payload=f"vip_{user_id}",
            provider_token="",  # Empty for Telegram Stars
            currency="XTR",
            prices=[LabeledPrice("VIP Membership", VIP_PRICE_STARS)]
        )
    
    async def precheckout_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle pre-checkout query"""
        query = update.pre_checkout_query
        await query.answer(ok=True)
    
    async def successful_payment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle successful payment"""
        user_id = update.effective_user.id
        
        # Grant VIP status
        db.set_vip_status(user_id, True)
        
        await update.message.reply_text(
            "🎉 Congratulations! You are now a VIP member!\n\n"
            "You can now see your partner's age and gender during chats.\n\n"
            "Use /search to start chatting with VIP benefits!"
        )
    
    async def rules(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /rules command"""
        rules_text = (
            "📜 Chat Rules\n\n"
            "1️⃣ No sharing of links or external contact info\n"
            "2️⃣ Be respectful - harassment and hate speech are not allowed\n"
            "3️⃣ No spam, scams, or fraudulent activities\n"
            "4️⃣ No explicit, sexual, or inappropriate content\n"
            "5️⃣ No impersonation or misleading information\n"
            "6️⃣ Use the rating system to report bad behavior\n\n"
            "⚠️ Violation of these rules may result in:\n"
            "• Warnings\n"
            "• Temporary or permanent ban\n"
            "• Reported to admins\n\n"
            "Remember: Your chats are anonymous to your matches, "
            "but admins can trace your Telegram ID if you get reported.\n\n"
            "Be kind and enjoy chatting! 💬"
        )
        
        await update.message.reply_text(rules_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            "🤖 Anonymous Chat Bot Help\n\n"
            "Commands:\n"
            "/start - Start the bot and register\n"
            "/search - Find a random chat partner\n"
            "/stop - End current chat\n"
            "/next - Find next partner\n"
            "/profile - View/edit your profile\n"
            "/vip - Learn about VIP membership\n"
            "/rules - View chat rules\n"
            "/help - Show this help message\n\n"
            "How it works:\n"
            "1️⃣ Register with your gender and age\n"
            "2️⃣ Use /search to find a random partner\n"
            "3️⃣ Chat anonymously - your identity is hidden\n"
            "4️⃣ Rate your partner after each chat\n"
            "5️⃣ Use /next to find a new partner anytime\n\n"
            "💡 Tip: Upgrade to VIP to see your partner's info!"
        )
        
        await update.message.reply_text(help_text, reply_markup=self._main_menu_keyboard())
    
    async def language_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /language command - let user choose language."""
        keyboard = [
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton("🇦🇲 Հայերեն", callback_data="lang_hy")],
        ]
        await update.message.reply_text(
            "🌐 Select your language / Выберите язык / Ընտրեք լեզուն:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    
    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection callback."""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        lang_code = query.data.split('_')[1]  # lang_en -> en
        
        if lang_code not in ("en", "ru", "hy"):
            lang_code = "en"
        
        db.set_user_language(user_id, lang_code)
        context.user_data['language'] = lang_code
        
        await query.edit_message_text(
            get_text("language_changed", lang_code),
            reply_markup=None,
        )
        
        # Show menu with new language
        await self._send_main_menu_hint(
            update,
            get_text("welcome_back", lang_code),
            lang_code,
        )

    async def menu_router(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Route reply-keyboard button presses to the existing command handlers."""
        text = (update.effective_message.text or "").strip()
        
        # Try to detect which button was pressed across all languages
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)
        
        # Build mapping with current language
        mapping = {
            get_text("btn_search", lang): self.search,
            get_text("btn_next", lang): self.next_partner,
            get_text("btn_stop", lang): self.stop,
            get_text("btn_profile", lang): self.profile,
            get_text("btn_vip", lang): self.vip_info,
            get_text("btn_rules", lang): self.rules,
            get_text("btn_help", lang): self.help_command,
        }

        handler = mapping.get(text)
        if handler is None:
            # Try all languages as fallback (user might have old keyboard)
            for fallback_lang in ["en", "ru", "hy"]:
                if fallback_lang == lang:
                    continue
                fallback_mapping = {
                    get_text("btn_search", fallback_lang): self.search,
                    get_text("btn_next", fallback_lang): self.next_partner,
                    get_text("btn_stop", fallback_lang): self.stop,
                    get_text("btn_profile", fallback_lang): self.profile,
                    get_text("btn_vip", fallback_lang): self.vip_info,
                    get_text("btn_rules", fallback_lang): self.rules,
                    get_text("btn_help", fallback_lang): self.help_command,
                }
                handler = fallback_mapping.get(text)
                if handler:
                    break
            
            if handler is None:
                return

        await handler(update, context)
    
    # Admin commands
    async def admin_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            return
        
        stats = db.get_stats()
        
        stats_text = (
            f"📊 Bot Statistics\n\n"
            f"👥 Total Users: {stats['total_users']}\n"
            f"👑 VIP Users: {stats['vip_users']}\n"
            f"🚫 Banned Users: {stats['banned_users']}\n"
            f"💬 Active Chats: {len(self.active_chats) // 2}\n"
            f"🔍 Users in Queue: {len(self.search_queue)}\n"
            f"⭐ Total Ratings: {stats['total_ratings']}\n"
            f"⛔ Total Reports: {stats['total_reports']}"
        )
        
        await update.message.reply_text(stats_text)
    
    async def admin_ban(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ban command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /ban <user_id | @username>")
            return
        
        try:
            target_id = self._resolve_target_user_id(context.args[0])
            if target_id is None:
                await update.message.reply_text(
                    "❗️ Unknown target. Use numeric id or @username. (User must have started the bot at least once.)"
                )
                return
            db.ban_user(target_id)
            
            # Disconnect if in chat
            if target_id in self.active_chats:
                partner_id = self.active_chats[target_id]
                del self.active_chats[target_id]
                del self.active_chats[partner_id]
                
                await context.bot.send_message(
                    partner_id,
                    "Your partner has been disconnected."
                )
            
            await context.bot.send_message(
                target_id,
                "🚫 You have been banned from using this bot."
            )
            
            await update.message.reply_text(f"✅ User {target_id} has been banned.")
            
        except (ValueError, IndexError):
            await update.message.reply_text("❗️ Invalid target (use numeric id or @username)")
    
    async def admin_unban(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /unban command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /unban <user_id | @username>")
            return
        
        try:
            target_id = self._resolve_target_user_id(context.args[0])
            if target_id is None:
                await update.message.reply_text(
                    "❗️ Unknown target. Use numeric id or @username. (User must have started the bot at least once.)"
                )
                return
            db.unban_user(target_id)
            
            await update.message.reply_text(f"✅ User {target_id} has been unbanned.")
            
        except (ValueError, IndexError):
            await update.message.reply_text("❗️ Invalid target (use numeric id or @username)")
    
    async def admin_give_vip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /givevip command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /givevip <user_id | @username>")
            return
        
        try:
            target_id = self._resolve_target_user_id(context.args[0])
            if target_id is None:
                await update.message.reply_text(
                    "❗️ Unknown target. Use numeric id or @username. (User must have started the bot at least once.)"
                )
                return

            db.set_vip_status(target_id, True)
            
            await context.bot.send_message(
                target_id,
                "🎉 You have been granted VIP status by an admin!"
            )
            
            await update.message.reply_text(f"✅ VIP status granted to user {target_id}")
            
        except (ValueError, IndexError):
            await update.message.reply_text("❗️ Invalid target (use numeric id or @username)")
    
    async def admin_reports(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reports command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            return
        
        reports = db.get_recent_reports()
        
        if not reports:
            await update.message.reply_text("No recent reports.")
            return
        
        reports_text = "⛔ Recent Reports:\n\n"
        for report in reports[:10]:  # Show last 10
            reports_text += f"User {report['target_id']}: {report['count']} reports\n"
        
        await update.message.reply_text(reports_text)
    
    async def admin_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /broadcast command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /broadcast <message>")
            return
        
        message = ' '.join(context.args)
        users = db.get_all_users()
        
        success = 0
        failed = 0
        
        for user in users:
            try:
                await context.bot.send_message(user['user_id'], f"📢 Announcement:\n\n{message}")
                success += 1
            except Exception as e:
                failed += 1
                logger.error(f"Failed to send to {user['user_id']}: {e}")
        
        await update.message.reply_text(
            f"✅ Broadcast complete!\n"
            f"Sent: {success}\n"
            f"Failed: {failed}"
        )

def main():
    """Start the bot"""
    # Create bot instance
    bot = AnonymousChatBot()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Set bot commands (menu in Telegram UI)
    async def post_init(app: Application):
        await app.bot.set_my_commands([
            BotCommand("start", "Start the bot / register"),
            BotCommand("search", "🔍 Find a chat partner"),
            BotCommand("next", "⏭ Find next partner"),
            BotCommand("stop", "🛑 End current chat"),
            BotCommand("profile", "👤 View/edit your profile"),
            BotCommand("vip", "⭐ Get VIP membership"),
            BotCommand("sharelink", "🔗 Share your Telegram link"),
            BotCommand("rules", "📜 View chat rules"),
            BotCommand("help", "🆘 Show help"),
        ])
    
    application.post_init = post_init
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("search", bot.search))
    application.add_handler(CommandHandler("stop", bot.stop))
    application.add_handler(CommandHandler("sharelink", bot.sharelink))
    application.add_handler(CommandHandler("next", bot.next_partner))
    application.add_handler(CommandHandler("profile", bot.profile))
    application.add_handler(CommandHandler("vip", bot.vip_info))
    application.add_handler(CommandHandler("rules", bot.rules))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("language", bot.language_command))
    
    # Admin commands
    application.add_handler(CommandHandler("stats", bot.admin_stats))
    application.add_handler(CommandHandler("ban", bot.admin_ban))
    application.add_handler(CommandHandler("unban", bot.admin_unban))
    application.add_handler(CommandHandler("givevip", bot.admin_give_vip))
    application.add_handler(CommandHandler("reports", bot.admin_reports))
    application.add_handler(CommandHandler("broadcast", bot.admin_broadcast))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(bot.verify_subscription_callback, pattern="^verify_subscription$"))
    application.add_handler(CallbackQueryHandler(bot.gender_callback, pattern="^gender_"))
    application.add_handler(CallbackQueryHandler(bot.rating_callback, pattern="^rate_"))
    application.add_handler(CallbackQueryHandler(bot.language_callback, pattern="^lang_"))
    application.add_handler(CallbackQueryHandler(bot.edit_profile_callback, pattern="^edit_profile$"))
    application.add_handler(CallbackQueryHandler(bot.edit_profile_gender_callback, pattern="^edit_gender_"))
    application.add_handler(CallbackQueryHandler(bot.edit_profile_age_callback, pattern="^edit_age$"))
    application.add_handler(CallbackQueryHandler(bot.edit_profile_back_callback, pattern="^edit_back_profile$"))
    application.add_handler(CallbackQueryHandler(bot.vip_search_choice_callback, pattern="^vip_search_"))
    application.add_handler(CallbackQueryHandler(bot.sharelink_callback, pattern="^sharelink_"))
    application.add_handler(CallbackQueryHandler(bot.buy_vip_callback, pattern="^buy_vip$"))
    
    # Payment handlers
    application.add_handler(PreCheckoutQueryHandler(bot.precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, bot.successful_payment))

    # Reply-keyboard menu buttons (must run before generic text relay)
    # Accepts any button text (menu_router handles language detection)
    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & filters.Regex(r"^(🔍|⏭|🛑|👤|⭐|📜|🆘)"),
            bot.menu_router,
        )
    )
    
    # Message handler (must be last)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Start the bot
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
