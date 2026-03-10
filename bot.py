"""
Anonymous Telegram Chat Bot
Main bot file with all handlers and logic
"""

import logging
from telegram.error import BadRequest, Forbidden
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
from config import BOT_TOKEN, ADMIN_IDS, REQUIRED_CHANNELS, VIP_PRICES
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
        # REMOVED: self.active_chats and self.search_queue
        # All state now managed atomically in database
        pass

    def _format_vip_plan_lines(self, lang: str) -> str:
        return "\n".join(
            f"• {get_text('vip_plan_button', lang, days=days, stars=stars)}"
            for days, stars in VIP_PRICES.items()
        )

    def _vip_plan_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    get_text("vip_plan_button", lang, days=days, stars=stars),
                    callback_data=f"buy_vip_{days}",
                )
            ]
            for days, stars in VIP_PRICES.items()
        ])

    def _format_partner_ratings_line(self, target_user_id: int, lang: str = 'en') -> str:
        """VIP-only: return a one-line summary of partner ratings."""
        ratings = db.get_user_ratings(target_user_id)

        good = int(ratings.get('good') or 0)
        bad = int(ratings.get('bad') or 0)
        scam = int(ratings.get('scam') or 0)
        total = good + bad + scam

        if total == 0:
            return get_text('vip_partner_ratings_none', lang)

        return get_text(
            'vip_partner_ratings_line',
            lang,
            good=good,
            bad=bad,
            scam=scam,
            total=total,
        )
    
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
    
    def _get_partner_id(self, user_id: int):
        """
        Get partner_id from active chat session.
        Returns None if user is not in CHATTING state.
        """
        state_info = db.get_user_state(user_id)
        if not state_info or state_info['state'] != 'CHATTING' or not state_info['chat_id']:
            return None
        
        # Get partner from chat_sessions table
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user1_id, user2_id FROM chat_sessions WHERE chat_id = ?
        ''', (state_info['chat_id'],))
        row = cursor.fetchone()
        if not row:
            return None
        
        return row['user2_id'] if row['user1_id'] == user_id else row['user1_id']
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        username = (update.effective_user.username or None)

        # Check if user exists in database
        user = db.get_user(user_id)

        if not user:
            # New user - check if language was already selected
            if 'language' not in context.user_data:
                # Show language selection first (before captcha)
                keyboard = [
                    [InlineKeyboardButton("🇬🇧 English", callback_data="lang_select_en")],
                    [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_select_ru")],
                    [InlineKeyboardButton("🇦🇲 Հայերեն", callback_data="lang_select_hy")],
                ]
                
                await update.message.reply_text(
                    get_text("language_select_start", self._detect_language(update)),
                    reply_markup=InlineKeyboardMarkup(keyboard),
                )
                return
            
            # Language selected, now check subscriptions
            if not await self.check_subscriptions(update, context):
                return
            
            # Subscription verified, show gender selection
            lang = context.user_data.get('language', 'en')
            await update.message.reply_text(
                get_text("welcome_new", lang),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(get_text("gender_male", lang), callback_data="gender_male")],
                    [InlineKeyboardButton(get_text("gender_female", lang), callback_data="gender_female")],
                ]),
            )
        else:
            # Existing user - check subscriptions first
            if not await self.check_subscriptions(update, context):
                return
            
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

    async def _get_missing_required_channels(self, user_id: int, context: ContextTypes.DEFAULT_TYPE):
        """Return required channels the user is not currently subscribed to."""
        if not REQUIRED_CHANNELS:
            return []

        not_subscribed = []
        for channel in REQUIRED_CHANNELS:
            try:
                member = await context.bot.get_chat_member(channel, user_id)
                if member.status in ['left', 'kicked']:
                    not_subscribed.append(channel)
            except Exception as e:
                logger.error(f"Error checking subscription for {channel}: {e}")
                not_subscribed.append(channel)

        return not_subscribed

    async def _send_subscription_required_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str, channels=None):
        """Send a subscription prompt that works for both messages and callbacks."""
        channel_links = '\n'.join([f"• {ch}" for ch in (channels or REQUIRED_CHANNELS)])
        keyboard = [[
            InlineKeyboardButton(get_text("subscription_btn", lang), callback_data="verify_subscription")
        ]]

        await update.effective_chat.send_message(
            get_text("subscription_missing", lang, channel_links=channel_links),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def _disconnect_user_for_subscription_loss(self, user_id: int, context: ContextTypes.DEFAULT_TYPE):
        """Force user out of queue/chat after they unsubscribe from required channels."""
        state_info = db.get_user_state(user_id)
        if not state_info:
            return

        if state_info['state'] == 'SEARCHING':
            db.atomic_leave_queue(user_id)
            return

        if state_info['state'] in ('CHATTING', 'RATING'):
            success, partner_id, _ = db.atomic_end_chat(user_id)
            if success and partner_id:
                partner_lang = self._get_user_lang(partner_id)
                try:
                    await context.bot.send_message(
                        partner_id,
                        get_text("partner_left", partner_lang)
                    )
                except (Forbidden, BadRequest) as e:
                    logger.warning(f"[SUBSCRIPTION] Could not notify partner {partner_id}: {e}")

                try:
                    await self.show_rating_to_user(context, partner_id, user_id)
                except (Forbidden, BadRequest) as e:
                    logger.warning(f"[SUBSCRIPTION] Could not send rating to partner {partner_id}: {e}")

    async def enforce_live_subscription(self, update: Update, context: ContextTypes.DEFAULT_TYPE, disconnect_active: bool = True) -> bool:
        """Re-check required channels on every important interaction."""
        user_id = update.effective_user.id
        if user_id in ADMIN_IDS:
            return True

        user = db.get_user(user_id)
        lang = (
            (user.get('language') if user else None)
            or context.user_data.get('language')
            or self._detect_language(update)
        )

        not_subscribed = await self._get_missing_required_channels(user_id, context)
        if not not_subscribed:
            if user:
                db.update_user_subscription(user_id, True)
            return True

        if user:
            db.update_user_subscription(user_id, False)

        if disconnect_active:
            await self._disconnect_user_for_subscription_loss(user_id, context)

        await self._send_subscription_required_message(update, context, lang, not_subscribed)
        return False
    
    async def check_subscriptions(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Check if user has subscribed to required channels"""
        return await self.enforce_live_subscription(update, context, disconnect_active=True)
    
    async def verify_subscription_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle subscription verification button"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = db.get_user(user_id)
        lang = (
            (user.get('language') if user else None)
            or context.user_data.get('language')
            or self._detect_language(update)
        )
        not_subscribed = await self._get_missing_required_channels(user_id, context)
        
        if not_subscribed:
            channel_links = '\n'.join([f"• {ch}" for ch in not_subscribed])
            keyboard = [[
                InlineKeyboardButton(get_text("subscription_btn", lang), callback_data="verify_subscription")
            ]]
            await query.edit_message_text(
                get_text("subscription_not_all_with_channels", lang, channel_links=channel_links),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            db.update_user_subscription(user_id, True)

            await query.edit_message_text(get_text("subscription_verified", lang))
            
            # Start registration with selected language
            await context.bot.send_message(
                chat_id=user_id,
                text=get_text("welcome_new", lang),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(get_text("gender_male", lang), callback_data="gender_male")],
                    [InlineKeyboardButton(get_text("gender_female", lang), callback_data="gender_female")],
                ])
            )
    
    async def gender_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle gender selection"""
        query = update.callback_query
        await query.answer()
        
        lang = context.user_data.get('language', 'en')
        
        gender = query.data.split('_')[1]
        if gender not in ("male", "female"):
            await query.edit_message_text(get_text("gender_invalid", lang))
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
        """Handle /search command - atomic matchmaking with state machine"""
        user_id = update.effective_user.id
        msg = update.effective_message
        lang = self._get_user_lang(user_id)

        if not await self.enforce_live_subscription(update, context):
            return
        
        # Check if user is registered
        user = db.get_user(user_id)
        if not user:
            await msg.reply_text(
                get_text("register_first", lang)
            )
            return
        
        # Check if user is banned
        if user['is_banned']:
            await msg.reply_text(
                get_text("banned", lang)
            )
            return
        
        # Check current state
        state_info = db.get_user_state(user_id)
        if state_info and state_info['state'] == 'CHATTING':
            await msg.reply_text(
                get_text("already_in_chat", lang)
            )
            return
        
        if state_info and state_info['state'] == 'SEARCHING':
            await msg.reply_text(
                get_text("already_searching", lang)
            )
            return
        
        # VIP users can choose gender preference
        if user.get('is_vip'):
            # Check if preference already set in this session
            if 'vip_target_gender' not in context.user_data:
                keyboard = [
                    [
                            InlineKeyboardButton("👧 Girl", callback_data="vip_search_female"),
                            InlineKeyboardButton("👦 Boy", callback_data="vip_search_male"),
                    ],
                    [InlineKeyboardButton("🎲 Random", callback_data="vip_search_any")],
                ]
                await msg.reply_text(
                    get_text("vip_choose_gender", lang),
                    reply_markup=InlineKeyboardMarkup(keyboard),
                )
                return
            
            target_gender = context.user_data.get('vip_target_gender', 'any')
        else:
            target_gender = 'any'
        
        logger.info(f"[ATOMIC] User {user_id} searching with filter: {target_gender}")
        
        # Try atomic match first
        success, partner_id, message = db.atomic_match(user_id, target_gender)
        
        if success and partner_id:
            # MATCHED!
            partner = db.get_user(partner_id)
            
            # Notify both users
            user_is_vip = user['is_vip']
            partner_is_vip = partner['is_vip']
            partner_lang = self._get_user_lang(partner_id)
            
            user_message = get_text("match_found", lang)
            partner_message = get_text("match_found", partner_lang)
            
            # Add VIP info
            if user_is_vip:
                gender_emoji = "♂️" if partner['gender'] == 'male' else "♀️" if partner['gender'] == 'female' else "⚧️"
                user_message += f"\n\n👑 VIP Info: {gender_emoji} {partner['gender'].capitalize()}, {partner['age']} years old"
                user_message += "\n" + self._format_partner_ratings_line(partner_id, lang)
            else:
                user_message += get_text("vip_match_upsell", lang)
            
            if partner_is_vip:
                gender_emoji = "♂️" if user['gender'] == 'male' else "♀️" if user['gender'] == 'female' else "⚧️"
                partner_message += f"\n\n👑 VIP Info: {gender_emoji} {user['gender'].capitalize()}, {user['age']} years old"
                partner_message += "\n" + self._format_partner_ratings_line(user_id, partner_lang)
            else:
                partner_message += get_text("vip_match_upsell", partner_lang)
            
            await msg.reply_text(user_message)
            await context.bot.send_message(partner_id, partner_message)
            
            logger.info(f"[ATOMIC] Matched {user_id} <-> {partner_id} (filter: {target_gender}, partner_gender: {partner['gender']})")
            
        else:
            # No match found, join queue
            success, queue_message = db.atomic_join_queue(user_id, target_gender)
            
            if success:
                await msg.reply_text(
                    get_text("searching", lang)
                )
                logger.info(f"[ATOMIC] User {user_id} joined queue with filter: {target_gender}")
            else:
                await msg.reply_text(
                    f"❗️ {queue_message}"
                )
                logger.warning(f"[ATOMIC] User {user_id} failed to join queue: {queue_message}")

    async def vip_search_choice_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """VIP-only: handle gender choice before searching."""
        query = update.callback_query
        await query.answer()

        if not await self.enforce_live_subscription(update, context):
            return
        
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)
        
        # Prevent choice change if already searching/chatting
        state_info = db.get_user_state(user_id)
        if state_info and state_info['state'] in ('SEARCHING', 'CHATTING'):
            await query.edit_message_text(
                get_text("already_in_state", lang).format(state=state_info['state'].lower())
            )
            return

        choice = query.data
        if choice == "vip_search_male":
            context.user_data['vip_target_gender'] = 'male'
            label = get_text('vip_label_boy', lang)
        elif choice == "vip_search_female":
            context.user_data['vip_target_gender'] = 'female'
            label = get_text('vip_label_girl', lang)
        else:
            context.user_data['vip_target_gender'] = 'any'
            label = get_text('vip_label_random', lang)

        await query.edit_message_text(
            get_text('vip_search_preference_set', lang, label=label)
        )

        # Continue with atomic search
        await self.search(update, context)
    
    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stop command - end current chat or search (atomic)"""
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        if not await self.enforce_live_subscription(update, context):
            return

        # Clear VIP preference for next search
        if 'vip_target_gender' in context.user_data:
            del context.user_data['vip_target_gender']

        # Check state
        state_info = db.get_user_state(user_id)
        if not state_info:
            await update.message.reply_text(
                get_text("not_in_chat_or_search", lang)
            )
            return
        
        if state_info['state'] == 'SEARCHING':
            # Leave queue
            success, message = db.atomic_leave_queue(user_id)
            if success:
                await update.message.reply_text(
                    get_text("search_cancelled", lang)
                )
                logger.info(f"[ATOMIC] User {user_id} left search queue")
            else:
                await update.message.reply_text(f"❗️ {message}")
            return
        
        if state_info['state'] == 'CHATTING':
            # End chat
            success, partner_id, message = db.atomic_end_chat(user_id)
            if success and partner_id:
                # Show rating to the user who stopped
                await self.show_rating(update, context, user_id, partner_id)

                partner_lang = self._get_user_lang(partner_id)
                # Send "partner left" first, then rating — each wrapped so one failure
                # doesn't block the other (e.g. partner blocked the bot)
                try:
                    await context.bot.send_message(
                        partner_id,
                        get_text("partner_left", partner_lang)
                    )
                except (Forbidden, BadRequest) as e:
                    logger.warning(f"[STOP] Could not send partner_left to {partner_id}: {e}")
                try:
                    await self.show_rating_to_user(context, partner_id, user_id)
                except (Forbidden, BadRequest) as e:
                    logger.warning(f"[STOP] Could not send rating to {partner_id}: {e}")

                logger.info(f"[ATOMIC] User {user_id} ended chat with {partner_id}")
            else:
                await update.message.reply_text(f"❗️ {message}")
            return
        
        await update.message.reply_text(
            get_text("not_in_chat_or_search", lang)
        )

    async def sharelink(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Share your Telegram @username / t.me link with your current partner (consent-based)."""
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        if not await self.enforce_live_subscription(update, context):
            return

        partner_id = self._get_partner_id(user_id)
        if not partner_id:
            await update.message.reply_text(
                get_text("not_in_chat", lang)
            )
            return

        username = update.effective_user.username
        if not username:
            await update.message.reply_text(
                get_text("no_username", lang)
            )
            return

        # Ask for confirmation to avoid accidental doxxing.
        keyboard = [[
            InlineKeyboardButton(get_text("sharelink_btn_share", lang), callback_data="sharelink_confirm"),
            InlineKeyboardButton(get_text("sharelink_btn_cancel", lang), callback_data="sharelink_cancel"),
        ]]
        await update.message.reply_text(
            get_text("sharelink_prompt", lang, username=username),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    async def sharelink_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle sharelink confirmation/cancel buttons."""
        query = update.callback_query
        await query.answer()

        if not await self.enforce_live_subscription(update, context):
            return

        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)
        action = query.data

        if action == "sharelink_cancel":
            await query.edit_message_text(get_text("share_cancelled", lang))
            return

        partner_id = self._get_partner_id(user_id)
        if not partner_id:
            await query.edit_message_text(
                get_text("not_in_chat", lang)
            )
            return

        username = update.effective_user.username
        if not username:
            await query.edit_message_text(
                get_text("no_username", lang)
            )
            return

        link = f"https://t.me/{username}"

        await context.bot.send_message(
            partner_id,
            f"🔗 Your partner shared their Telegram: @{username}\n{link}"
        )
        await query.edit_message_text(get_text("sharelink_shared", lang))
    
    async def next_partner(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /next command - atomic super-operation.
        Ends current chat + starts new search in one transaction.
        Prevents race conditions.
        """
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)
        msg = update.effective_message

        if not await self.enforce_live_subscription(update, context):
            return

        # Clear VIP preference
        if 'vip_target_gender' in context.user_data:
            del context.user_data['vip_target_gender']
        
        # Get user info for VIP filter
        user = db.get_user(user_id)
        if not user:
            await msg.reply_text(
                get_text("register_first", lang)
            )
            return
        
        # VIP users can choose target gender for /next
        target_gender = 'any'
        if user.get('is_vip'):
            # Check if preference set for /next
            if 'vip_next_target_gender' not in context.user_data:
                keyboard = [
                    [
                        InlineKeyboardButton("👧 Girl", callback_data="vip_next_female"),
                        InlineKeyboardButton("👦 Boy", callback_data="vip_next_male"),
                    ],
                    [InlineKeyboardButton("🎲 Random", callback_data="vip_next_any")],
                ]
                await msg.reply_text(
                    "👑 VIP /next: Choose gender preference:",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                )
                return
            
            target_gender = context.user_data.get('vip_next_target_gender', 'any')
            del context.user_data['vip_next_target_gender']
        
        logger.info(f"[ATOMIC /next] User {user_id} with filter: {target_gender}")
        
        # Execute atomic next operation
        success, action, data = db.atomic_next_partner(user_id, target_gender)
        
        if not success:
            await msg.reply_text(
                f"❗️ Error: {data.get('message', 'Unknown error')}"
            )
            logger.error(f"[ATOMIC /next] Failed for {user_id}: {data.get('message')}")
            return
        
        # Notify old partner that the chat was ended (applies to both 'matched' and 'searching')
        old_partner_id = data.get('old_partner_id')
        if old_partner_id:
            old_partner_lang = self._get_user_lang(old_partner_id)
            try:
                await context.bot.send_message(
                    old_partner_id,
                    get_text("partner_left", old_partner_lang)
                )
            except (Forbidden, BadRequest) as e:
                logger.warning(f"[NEXT] Could not send partner_left to old partner {old_partner_id}: {e}")
            try:
                await self.show_rating_to_user(context, old_partner_id, user_id)
            except (Forbidden, BadRequest) as e:
                logger.warning(f"[NEXT] Could not send rating to old partner {old_partner_id}: {e}")

        if action == 'matched':
            # Matched immediately!
            partner_info = data['partner']
            partner_id = partner_info['user_id']
            partner_lang = self._get_user_lang(partner_id)
            
            # Notify both users
            user_message = get_text("match_found", lang)
            partner_message = get_text("match_found", partner_lang)
            
            # Add VIP info
            if user.get('is_vip'):
                gender_emoji = "♂️" if partner_info['gender'] == 'male' else "♀️" if partner_info['gender'] == 'female' else "⚧️"
                user_message += f"\n\n👑 VIP Info: {gender_emoji} {partner_info['gender'].capitalize()}, {partner_info['age']} years old"
                user_message += "\n" + self._format_partner_ratings_line(partner_id, lang)
            else:
                user_message += get_text("vip_match_upsell", lang)
            
            if partner_info['is_vip']:
                gender_emoji = "♂️" if user['gender'] == 'male' else "♀️" if user['gender'] == 'female' else "⚧️"
                partner_message += f"\n\n👑 VIP Info: {gender_emoji} {user['gender'].capitalize()}, {user['age']} years old"
                partner_message += "\n" + self._format_partner_ratings_line(user_id, partner_lang)
            else:
                partner_message += get_text("vip_match_upsell", partner_lang)
            
            await msg.reply_text(user_message)
            await context.bot.send_message(partner_id, partner_message)
            
            logger.info(f"[ATOMIC /next] Matched {user_id} <-> {partner_id}")
            
        elif action == 'searching':
            # Joined queue
            await msg.reply_text(
                get_text("searching", lang)
            )
            logger.info(f"[ATOMIC /next] User {user_id} joined queue")
        
        else:
            await msg.reply_text(
                f"❗️ Unexpected result: {action}"
            )
    
    async def vip_next_choice_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """VIP-only: handle gender choice for /next command."""
        query = update.callback_query
        await query.answer()

        if not await self.enforce_live_subscription(update, context):
            return
        
        choice = query.data
        if choice == "vip_next_male":
            context.user_data['vip_next_target_gender'] = 'male'
            label = "Boy"
        elif choice == "vip_next_female":
            context.user_data['vip_next_target_gender'] = 'female'
            label = "Girl"
        else:
            context.user_data['vip_next_target_gender'] = 'any'
            label = "Random"
        
        await query.edit_message_text(
            f"👑 VIP /next preference: {label}\n\n🔄 Finding next partner..."
        )
        
        # Continue with atomic next
        await self.next_partner(update, context)
    
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
            get_text("rate_partner", self._get_user_lang(rater_id)),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def rating_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle rating button press"""
        query = update.callback_query
        await query.answer()

        if not await self.enforce_live_subscription(update, context, disconnect_active=False):
            return
        
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
            
            await query.edit_message_text(
                get_text("thanks_report", self._get_user_lang(rater_id))
            )
        else:
            await query.edit_message_text(
                get_text("thanks_rating_with_type", self._get_user_lang(rater_id), rating_type=rating_type)
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages - relay to chat partner"""
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        if not await self.enforce_live_subscription(update, context):
            return

        # Profile edit: age input
        if context.user_data.get('awaiting_age_edit'):
            try:
                age = int(update.message.text)
                if age < 12 or age > 99:
                    await update.message.reply_text(
                        get_text("age_invalid_range", lang)
                    )
                    return

                db.update_age(user_id, age)
                context.user_data['awaiting_age_edit'] = False
                await update.message.reply_text(
                    get_text("age_updated", lang)
                )
            except ValueError:
                await update.message.reply_text(get_text("age_invalid_number_simple", lang))
            return
        
        # Check if awaiting age input
        if context.user_data.get('awaiting_age'):
            await self.handle_age_input(update, context)
            return
        
        # Check if in active chat (atomic)
        partner_id = self._get_partner_id(user_id)
        if not partner_id:
            await update.message.reply_text(
                get_text("not_in_chat", lang)
            )
            return
        
        message_text = update.message.text
        
        # Check for links
        if self.contains_link(message_text):
            await update.message.reply_text(
                get_text("no_links", lang)
            )
            return
        
        # Check for bad words (basic filter)
        if self.contains_bad_words(message_text):
            await update.message.reply_text(
                get_text("keep_respectful", lang)
            )
            return
        
        # Forward message to partner
        try:
            await context.bot.send_message(partner_id, message_text)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            await update.message.reply_text(
                get_text("send_failed", lang)
            )

    async def handle_media(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Relay non-text messages (photos, videos, GIFs, etc.) to chat partner."""
        user_id = update.effective_user.id

        if not await self.enforce_live_subscription(update, context):
            return

        partner_id = self._get_partner_id(user_id)
        if not partner_id:
            await update.effective_message.reply_text(
                "❗️ You're not in an active chat.\nUse /search to find a partner."
            )
            return

        msg = update.effective_message

        # Copy keeps anonymity (no forward header) and preserves caption + formatting.
        try:
            await context.bot.copy_message(
                chat_id=partner_id,
                from_chat_id=msg.chat_id,
                message_id=msg.message_id,
            )
        except Exception as e:
            logger.error(f"Error sending media: {e}")
            await update.effective_message.reply_text(
                "❗️ Failed to send media. Your partner may have left."
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
        lang = self._get_user_lang(user_id)

        if not await self.enforce_live_subscription(update, context):
            return

        user = db.get_user(user_id)

        if not user:
            await update.effective_message.reply_text(
                get_text("register_first", lang)
            )
            return

        gender_emoji = (
            "♂️" if user["gender"] == "male" else "♀️" if user["gender"] == "female" else "⚧️"
        )
        gender_label = get_text(f"gender_{user['gender']}", lang).split(" ", 1)[1]
        vip_status = get_text("vip_member", lang) if user["is_vip"] else get_text("regular_user", lang)
        
        # Add VIP expiration info if user is VIP
        vip_info = vip_status
        if user["is_vip"]:
            days_remaining = db.get_vip_days_remaining(user_id)
            if days_remaining is not None:
                vip_info = get_text("profile_vip_days", lang, days=days_remaining)

        ratings = db.get_user_ratings(user_id)

        profile_text = get_text(
            "profile_text",
            lang,
            gender_emoji=gender_emoji,
            gender=gender_label,
            age=user['age'],
            status=vip_info,
            good=ratings['good'],
            bad=ratings['bad'],
            scam=ratings['scam'],
        )

        keyboard = [[InlineKeyboardButton(get_text("edit_profile_button", lang), callback_data="edit_profile")]]
        await update.effective_message.reply_text(
            profile_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    async def edit_profile_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show profile edit menu."""
        query = update.callback_query
        await query.answer()

        if not await self.enforce_live_subscription(update, context):
            return

        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        keyboard = [
            [
                InlineKeyboardButton(get_text("gender_male", lang), callback_data="edit_gender_male"),
                InlineKeyboardButton(get_text("gender_female", lang), callback_data="edit_gender_female"),
            ],
            [InlineKeyboardButton(get_text("edit_profile_btn_edit_age", lang), callback_data="edit_age")],
            [InlineKeyboardButton(get_text("edit_profile_btn_back", lang), callback_data="edit_back_profile")],
        ]

        await query.edit_message_text(
            get_text("edit_profile_title", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    async def edit_profile_gender_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle gender change from edit profile menu."""
        query = update.callback_query
        await query.answer()

        if not await self.enforce_live_subscription(update, context):
            return

        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        gender = query.data.split("_")[-1]  # male|female
        if gender not in ("male", "female"):
            await query.edit_message_text(get_text("invalid_gender_choice", lang))
            return

        db.update_gender(user_id, gender)
        await query.edit_message_text(get_text("gender_updated", lang, gender=gender.capitalize()))

    async def edit_profile_age_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start age edit: next text message will be treated as new age."""
        query = update.callback_query
        await query.answer()

        if not await self.enforce_live_subscription(update, context):
            return

        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        context.user_data["awaiting_age_edit"] = True
        await query.edit_message_text(get_text("edit_profile_enter_age", lang))

    async def edit_profile_back_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Go back to profile view from edit menu."""
        query = update.callback_query
        await query.answer()

        if not await self.enforce_live_subscription(update, context):
            return

        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        user = db.get_user(user_id)
        if not user:
            await query.edit_message_text(get_text("register_first", lang))
            return

        gender_emoji = (
            "♂️" if user["gender"] == "male" else "♀️" if user["gender"] == "female" else "⚧️"
        )
        gender_label = get_text(f"gender_{user['gender']}", lang).split(" ", 1)[1]
        vip_status = get_text("vip_member", lang) if user["is_vip"] else get_text("regular_user", lang)
        if user["is_vip"]:
            days_remaining = db.get_vip_days_remaining(user_id)
            if days_remaining is not None:
                vip_status = get_text("profile_vip_days", lang, days=days_remaining)
        ratings = db.get_user_ratings(user_id)
        profile_text = get_text(
            "profile_text",
            lang,
            gender_emoji=gender_emoji,
            gender=gender_label,
            age=user['age'],
            status=vip_status,
            good=ratings['good'],
            bad=ratings['bad'],
            scam=ratings['scam'],
        )

        keyboard = [[InlineKeyboardButton(get_text("edit_profile_button", lang), callback_data="edit_profile")]]
        await query.edit_message_text(
            profile_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    
    async def vip_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /vip command"""
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        if not await self.enforce_live_subscription(update, context):
            return

        user = db.get_user(user_id)
        
        if user and user['is_vip']:
            days_remaining = db.get_vip_days_remaining(user_id)
            if days_remaining is not None:
                if days_remaining > 0:
                    # Active VIP with days remaining
                    keyboard = self._vip_plan_keyboard(lang)
                    await update.message.reply_text(
                        get_text("vip_active_text", lang, days=days_remaining),
                        reply_markup=keyboard
                    )
                else:
                    # VIP expired
                    keyboard = self._vip_plan_keyboard(lang)
                    await update.message.reply_text(
                        get_text("vip_expired_text", lang, plans=self._format_vip_plan_lines(lang)),
                        reply_markup=keyboard
                    )
            else:
                # Old VIP user without expiration (grandfathered)
                await update.message.reply_text(
                    get_text("vip_lifetime_text", lang)
                )
            return
        
        keyboard = self._vip_plan_keyboard(lang)
        
        await update.message.reply_text(
            get_text("vip_info_text", lang, plans=self._format_vip_plan_lines(lang)),
            reply_markup=keyboard
        )
    
    async def buy_vip_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle VIP purchase button"""
        query = update.callback_query
        await query.answer()

        if not await self.enforce_live_subscription(update, context):
            return
        
        user_id = query.from_user.id
        lang = self._get_user_lang(user_id)
        parts = query.data.split('_')

        if len(parts) < 3 or not parts[2].isdigit():
            await query.message.reply_text(
                get_text("vip_choose_plan", lang),
                reply_markup=self._vip_plan_keyboard(lang)
            )
            return

        vip_days = int(parts[2])
        vip_price = VIP_PRICES.get(vip_days)
        if vip_price is None:
            await query.message.reply_text(
                get_text("vip_choose_plan", lang),
                reply_markup=self._vip_plan_keyboard(lang)
            )
            return
        
        # Send invoice
        await context.bot.send_invoice(
            chat_id=user_id,
            title=get_text("vip_invoice_title", lang, days=vip_days),
            description=get_text("vip_invoice_description", lang, days=vip_days),
            payload=f"vip_{user_id}_{vip_days}",
            provider_token="",  # Empty for Telegram Stars
            currency="XTR",
            prices=[LabeledPrice(get_text("vip_invoice_title", lang, days=vip_days), vip_price)]
        )
    
    async def precheckout_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle pre-checkout query"""
        query = update.pre_checkout_query
        await query.answer(ok=True)
    
    async def successful_payment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle successful payment"""
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        if not await self.enforce_live_subscription(update, context, disconnect_active=False):
            return
        
        payload = update.message.successful_payment.invoice_payload or ""
        payload_parts = payload.split('_')
        vip_days = 30
        if len(payload_parts) >= 3 and payload_parts[2].isdigit():
            vip_days = int(payload_parts[2])

        if vip_days not in VIP_PRICES:
            vip_days = 30

        db.set_vip_status(user_id, True, days=vip_days)
        
        await update.message.reply_text(
            get_text("vip_payment_success", lang, days=vip_days)
        )
    
    async def rules(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /rules command"""
        if not await self.enforce_live_subscription(update, context):
            return

        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)
        await update.message.reply_text(get_text("rules_text", lang))
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if not await self.enforce_live_subscription(update, context):
            return

        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        help_text = get_text("help_text", lang)
        if user_id in ADMIN_IDS:
            help_text += get_text("help_admin_block", lang)

        await update.message.reply_text(help_text, reply_markup=self._main_menu_keyboard(lang))
    
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
        lang_code = query.data.split('_')[1]  # lang_en -> en or lang_select_en -> select
        
        # Check if this is initial language selection (new user)
        if query.data.startswith("lang_select_"):
            lang_code = query.data.split('_')[2]  # lang_select_en -> en
            
            if lang_code not in ("en", "ru", "hy"):
                lang_code = "en"
            
            # Store language in context for new user
            context.user_data['language'] = lang_code
            
            # Delete the language selection message
            await query.delete_message()

            # After language selection, only enforce channel subscription check
            if not await self.check_subscriptions(update, context):
                return

            # Subscription verified, show gender selection
            await update.effective_chat.send_message(
                get_text("welcome_new", lang_code),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(get_text("gender_male", lang_code), callback_data="gender_male")],
                    [InlineKeyboardButton(get_text("gender_female", lang_code), callback_data="gender_female")],
                ]),
            )
            return
        
        # Existing user changing language
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
    async def admin_commands(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /commands command (admin only) - show all admin commands."""
        user_id = update.effective_user.id

        if user_id not in ADMIN_IDS:
            return

        lang = self._get_user_lang(user_id)
        await update.message.reply_text(get_text("admin_commands_list", lang))

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
            f"💬 Active Chats: {stats['active_chats']}\n"
            f"🔍 Users in Queue: {stats['in_queue']}\n"
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
            await update.message.reply_text(get_text("admin_usage_ban", "en"))
            return
        
        try:
            target_id = self._resolve_target_user_id(context.args[0])
            if target_id is None:
                await update.message.reply_text(
                    "❗️ Unknown target. Use numeric id or @username. (User must have started the bot at least once.)"
                )
                return
            db.ban_user(target_id)
            
            # Disconnect if in chat (atomic)
            state_info = db.get_user_state(target_id)
            if state_info and state_info['state'] == 'CHATTING':
                success, partner_id, message = db.atomic_end_chat(target_id)
                if success and partner_id:
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
            await update.message.reply_text(get_text("admin_invalid_target", "en"))
    
    async def admin_unban(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /unban command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            return
        
        if not context.args:
            await update.message.reply_text(get_text("admin_usage_unban", "en"))
            return
        
        try:
            target_id = self._resolve_target_user_id(context.args[0])
            if target_id is None:
                await update.message.reply_text(
                    get_text("admin_unknown_target", "en")
                )
                return
            db.unban_user(target_id)
            
            await update.message.reply_text(get_text("admin_unban_done", "en", user_id=target_id))
            
        except (ValueError, IndexError):
            await update.message.reply_text(get_text("admin_invalid_target", "en"))

    async def admin_unban_all(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /unbanall command (admin only)"""
        user_id = update.effective_user.id

        if user_id not in ADMIN_IDS:
            return

        changed = db.unban_all_users()
        await update.message.reply_text(get_text("admin_unban_all_done", "en", count=changed))
    
    async def admin_give_vip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /givevip command (admin only)"""
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)
        
        if user_id not in ADMIN_IDS:
            return
        
        if len(context.args) < 2:
            await update.message.reply_text(get_text("admin_usage_givevip", lang))
            return
        
        try:
            target_id = self._resolve_target_user_id(context.args[0])
            if target_id is None:
                await update.message.reply_text(
                    get_text("admin_unknown_target", lang)
                )
                return

            days = int(context.args[1])
            if days <= 0:
                await update.message.reply_text(get_text("admin_invalid_days", lang))
                return

            db.set_vip_status(target_id, True, days=days)
            
            await context.bot.send_message(
                target_id,
                get_text("admin_vip_granted_target", self._get_user_lang(target_id), days=days)
            )
            
            await update.message.reply_text(get_text("admin_vip_granted_done", lang, user_id=target_id, days=days))
            
        except IndexError:
            await update.message.reply_text(get_text("admin_usage_givevip", lang))
        except ValueError:
            if len(context.args) >= 2 and not context.args[1].lstrip('-').isdigit():
                await update.message.reply_text(get_text("admin_invalid_days", lang))
                return
            await update.message.reply_text(get_text("admin_invalid_target", lang))

    async def admin_take_vip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /takevip command (admin only)."""
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        if user_id not in ADMIN_IDS:
            return

        if not context.args:
            await update.message.reply_text(get_text("admin_usage_takevip", lang))
            return

        try:
            target_id = self._resolve_target_user_id(context.args[0])
            if target_id is None:
                await update.message.reply_text(get_text("admin_unknown_target", lang))
                return

            db.set_vip_status(target_id, False)

            try:
                await context.bot.send_message(
                    target_id,
                    get_text("admin_vip_removed_target", self._get_user_lang(target_id))
                )
            except Exception as e:
                logger.warning(f"Failed to notify {target_id} about VIP removal: {e}")

            await update.message.reply_text(get_text("admin_vip_removed_done", lang, user_id=target_id))

        except (ValueError, IndexError):
            await update.message.reply_text(get_text("admin_invalid_target", lang))

    async def admin_vip_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /viplist command (admin only)."""
        user_id = update.effective_user.id
        lang = self._get_user_lang(user_id)

        if user_id not in ADMIN_IDS:
            return

        vip_users = db.get_vip_users()
        if not vip_users:
            await update.message.reply_text(get_text("admin_viplist_empty", lang))
            return

        vip_entries = []
        for vip_user in vip_users:
            target_id = vip_user['user_id']
            username = vip_user.get('username')
            days_remaining = db.get_vip_days_remaining(target_id)

            if username:
                user_label = get_text("admin_viplist_user_label", lang, username=username, user_id=target_id)
            else:
                user_label = get_text("admin_viplist_user_id_only", lang, user_id=target_id)

            sort_key = days_remaining if days_remaining is not None else 10**9
            vip_entries.append({
                'user_label': user_label,
                'days_remaining': days_remaining,
                'sort_key': sort_key,
            })

        vip_entries.sort(key=lambda item: (item['sort_key'], item['user_label'].lower()))

        lines = [get_text("admin_viplist_header", lang, count=len(vip_entries))]
        for index, vip_entry in enumerate(vip_entries, start=1):
            days_remaining = vip_entry['days_remaining']

            if days_remaining is None:
                lines.append(get_text("admin_viplist_line_lifetime", lang, index=index, user_label=vip_entry['user_label']))
            else:
                lines.append(get_text("admin_viplist_line_days", lang, index=index, user_label=vip_entry['user_label'], days=days_remaining))

        await update.message.reply_text("\n".join(lines))
    
    async def admin_reports(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reports command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            return
        
        reports = db.get_recent_reports()
        
        if not reports:
            await update.message.reply_text(get_text("admin_no_reports", "en"))
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
            await update.message.reply_text(get_text("admin_usage_broadcast", "en"))
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
    
    # Background task to check VIP expirations
    async def check_vip_expirations(context: ContextTypes.DEFAULT_TYPE):
        """Check and expire VIP subscriptions daily"""
        try:
            expired_users = db.check_and_expire_vips()
            if expired_users:
                logger.info(f"Expired {len(expired_users)} VIP subscriptions")

                for expired_user in expired_users:
                    expired_user_id = expired_user['user_id']
                    lang = expired_user.get('language') or 'en'
                    keyboard = bot._vip_plan_keyboard(lang)

                    try:
                        await context.bot.send_message(
                            expired_user_id,
                            get_text("vip_expired_text", lang, plans=bot._format_vip_plan_lines(lang)),
                            reply_markup=keyboard,
                        )
                    except (Forbidden, BadRequest) as e:
                        logger.warning(f"Could not send VIP expiration notice to {expired_user_id}: {e}")
        except Exception as e:
            logger.error(f"Error checking VIP expirations: {e}")
    
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
        
        # Schedule daily VIP expiration check (runs every 24 hours)
        job_queue = app.job_queue
        job_queue.run_repeating(check_vip_expirations, interval=86400, first=10)  # 86400 seconds = 24 hours
    
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
    application.add_handler(CommandHandler("commands", bot.admin_commands))
    application.add_handler(CommandHandler("stats", bot.admin_stats))
    application.add_handler(CommandHandler("ban", bot.admin_ban))
    application.add_handler(CommandHandler("unban", bot.admin_unban))
    application.add_handler(CommandHandler("unbanall", bot.admin_unban_all))
    application.add_handler(CommandHandler("givevip", bot.admin_give_vip))
    application.add_handler(CommandHandler("takevip", bot.admin_take_vip))
    application.add_handler(CommandHandler("viplist", bot.admin_vip_list))
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
    application.add_handler(CallbackQueryHandler(bot.vip_next_choice_callback, pattern="^vip_next_"))
    application.add_handler(CallbackQueryHandler(bot.sharelink_callback, pattern="^sharelink_"))
    application.add_handler(CallbackQueryHandler(bot.buy_vip_callback, pattern=r"^buy_vip(?:_\d+)?$"))
    
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

    # Media handler (photos/videos/GIFs/etc.)
    application.add_handler(
        MessageHandler(
            ~filters.TEXT
            & ~filters.COMMAND
            & ~filters.StatusUpdate.ALL
            & ~filters.UpdateType.EDITED,
            bot.handle_media,
        )
    )
    
    # Start the bot
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
