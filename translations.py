"""
Translation module for Anonymous Chat Bot
Supports: Armenian (hy), Russian (ru), English (en)
"""

TRANSLATIONS = {
    # Welcome messages
    "welcome_new": {
        "en": "👋 Welcome to Anonymous Chat Bot!\n\nBefore we start, I need some basic information.\n\nPlease select your gender:",
        "ru": "👋 Добро пожаловать в Анонимный чат-бот!\n\nПеред началом мне нужна немного информации.\n\nПожалуйста, выберите ваш пол:",
        "hy": "👋 Բարի գալուստ Անանուն Չաթ Բոտ!\n\nՍկսելուց առաջ ինձ պետք է մի փոքր տեղեկություն։\n\nԽնդրում եմ ընտրեք ձեր սեռը:",
    },
    "welcome_back": {
        "en": "👋 Welcome back!\n\nUse the buttons below or type commands if you prefer.",
        "ru": "👋 С возвращением!\n\nИспользуйте кнопки ниже или вводите команды, если хотите.",
        "hy": "👋 Բարի վերադարձ!\n\nՕգտագործեք ներքևի կոճակները կամ մուտքագրեք հրամաններ, եթե նախընտրում եք:",
    },
    
    # Gender buttons
    "gender_male": {
        "en": "♂️ Male",
        "ru": "♂️ Мужской",
        "hy": "♂️ Արական",
    },
    "gender_female": {
        "en": "♀️ Female",
        "ru": "♀️ Женский",
        "hy": "♀️ Իգական",
    },
    
    # Age prompt
    "enter_age": {
        "en": "Great! You selected: {gender}\n\nNow, please enter your age (12–99):",
        "ru": "Отлично! Вы выбрали: {gender}\n\nТеперь введите ваш возраст (12–99):",
        "hy": "Հիանալի! Դուք ընտրեցիք՝ {gender}\n\nԱյժմ մուտքագրեք ձեր տարիքը (12–99):",
    },
    "age_invalid": {
        "en": "❗️ Age must be between 12 and 99. Please enter your age again:",
        "ru": "❗️ Возраст должен быть от 12 до 99. Пожалуйста, введите возраст снова:",
        "hy": "❗️ Տարիքը պետք է լինի 12-ից 99։ Խնդրում եմ մուտքագրեք տարիքը կրկին:",
    },
    "age_invalid_number": {
        "en": "❗️ Please enter a valid number (12–99):",
        "ru": "❗️ Пожалуйста, введите правильное число (12–99):",
        "hy": "❗️ Խնդրում եմ մուտքագրեք ճիշտ թիվ (12–99):",
    },
    
    # Registration complete
    "registration_complete": {
        "en": "✅ Registration complete!\n\nYou can now start chatting anonymously.\n\nUse the menu buttons below (or type commands).",
        "ru": "✅ Регистрация завершена!\n\nТеперь вы можете начать анонимный чат.\n\nИспользуйте кнопки меню ниже (или вводите команды).",
        "hy": "✅ Գրանցումը ավարտված է!\n\nԴուք այժմ կարող եք սկսել անանուն զրույց։\n\nՕգտագործեք մենյուի կոճակները ներքևում (կամ մուտքագրեք հրամաններ):",
    },
    
    # Search/Chat
    "search_already_chatting": {
        "en": "❗️ You're already in a chat. Use /stop to end it first.",
        "ru": "❗️ Вы уже в чате. Используйте /stop, чтобы завершить его.",
        "hy": "❗️ Դուք արդեն զրուցում եք։ Օգտագործեք /stop այն ավարտելու համար:",
    },
    "search_already_searching": {
        "en": "⏳ You're already in the search queue. Please wait...",
        "ru": "⏳ Вы уже в очереди поиска. Пожалуйста, подождите...",
        "hy": "⏳ Դուք արդեն որոնման հերթում եք։ Խնդրում եմ սպասեք...",
    },
    "search_started": {
        "en": "🔍 Searching for a chat partner...\nYou'll be notified when someone is found.",
        "ru": "🔍 Ищем собеседника...\nВы получите уведомление, когда кто-то найдется.",
        "hy": "🔍 Որոնում ենք զրուցակից...\nԴուք կտեղեկացվեք, երբ որևէ մեկը գտնվի:",
    },
    "partner_found": {
        "en": "🔹 You are now connected to a partner! Say hi!",
        "ru": "🔹 Вы подключены к собеседнику! Поздоровайтесь!",
        "hy": "🔹 Դուք կապված եք զրուցակցի հետ։ Բարև ասեք!",
    },
    
    # VIP info in chat
    "vip_partner_info": {
        "en": "\n\n👑 VIP Info: {emoji} {gender}, {age} years old",
        "ru": "\n\n👑 VIP Инфо: {emoji} {gender}, {age} лет",
        "hy": "\n\n👑 VIP Տեղեկություն՝ {emoji} {gender}, {age} տարեկան",
    },

    "vip_partner_ratings_line": {
        "en": "📊 Partner ratings ({total}): 👍 {good} | 👎 {bad} | ⛔ {scam}",
        "ru": "📊 Оценки собеседника ({total}): 👍 {good} | 👎 {bad} | ⛔ {scam}",
        "hy": "📊 Զրուցակցի գնահատականները ({total}): 👍 {good} | 👎 {bad} | ⛔ {scam}",
    },
    "vip_partner_ratings_none": {
        "en": "📊 Partner ratings: no ratings yet",
        "ru": "📊 Оценки собеседника: пока нет оценок",
        "hy": "📊 Զրուցակցի գնահատականները՝ դեռ գնահատականներ չկան",
    },
    
    # Stop
    "stop_not_chatting": {
        "en": "❗️ You're not in an active chat.",
        "ru": "❗️ Вы не в активном чате.",
        "hy": "❗️ Դուք ակտիվ զրույցում չեք:",
    },
    "search_cancelled": {
        "en": "🛑 Search cancelled.\nUse /search when you want to find a partner again.",
        "ru": "🛑 Поиск отменен.\nИспользуйте /search, когда захотите найти собеседника снова.",
        "hy": "🛑 Որոնումը չեղարկված է։\nՕգտագործեք /search, երբ ցանկանաք նորից գտնել զրուցակից:",
    },
    "partner_left": {
        "en": "🔸 Your partner has left the chat.\n\nUse /search to find a new partner.",
        "ru": "🔸 Ваш собеседник покинул чат.\n\nИспользуйте /search, чтобы найти нового.",
        "hy": "🔸 Ձեր զրուցակիցը լքել է զրույցը։\n\nՕգտագործեք /search նոր զրուցակից գտնելու համար:",
    },
    
    # Rating
    "rate_partner": {
        "en": "Please rate your chat partner:",
        "ru": "Пожалуйста, оцените вашего собеседника:",
        "hy": "Խնդրում եմ գնահատեք ձեր զրուցակցին:",
    },
    "rate_good": {
        "en": "👍 Good",
        "ru": "👍 Хорошо",
        "hy": "👍 Լավ",
    },
    "rate_bad": {
        "en": "👎 Bad",
        "ru": "👎 Плохо",
        "hy": "👎 Վատ",
    },
    "rate_report": {
        "en": "⛔ Report",
        "ru": "⛔ Пожаловаться",
        "hy": "⛔ Բողոքել",
    },
    "thanks_rating": {
        "en": "Thank you for rating your partner!",
        "ru": "Спасибо за оценку вашего собеседника!",
        "hy": "Շնորհակալություն ձեր զրուցակցին գնահատելու համար!",
    },
    "thanks_report": {
        "en": "⛔ Thank you for your report. Our team will review this case.",
        "ru": "⛔ Спасибо за вашу жалобу. Наша команда рассмотрит этот случай.",
        "hy": "⛔ Շնորհակալություն ձեր բողոքի համար։ Մեր թիմը կուսումնասիրի այս դեպքը:",
    },
    
    # Profile
    "profile_text": {
        "en": "👤 Your Profile\n\n{gender_emoji} Gender: {gender}\n🎂 Age: {age}\n✨ Status: {status}\n\n📊 Ratings Received:\n👍 Good: {good}\n👎 Bad: {bad}\n⛔ Reports: {scam}",
        "ru": "👤 Ваш Профиль\n\n{gender_emoji} Пол: {gender}\n🎂 Возраст: {age}\n✨ Статус: {status}\n\n📊 Полученные оценки:\n👍 Хорошо: {good}\n👎 Плохо: {bad}\n⛔ Жалобы: {scam}",
        "hy": "👤 Ձեր Պրոֆիլ\n\n{gender_emoji} Սեռ՝ {gender}\n🎂 Տարիք՝ {age}\n✨ Կարգավիճակ՝ {status}\n\n📊 Ստացված գնահատականներ՝\n👍 Լավ՝ {good}\n👎 Վատ՝ {bad}\n⛔ Բողոքներ՝ {scam}",
    },
    "vip_member": {
        "en": "👑 VIP Member",
        "ru": "👑 VIP Участник",
        "hy": "👑 VIP Անդամ",
    },
    "regular_user": {
        "en": "Regular User",
        "ru": "Обычный пользователь",
        "hy": "Սովորական օգտատեր",
    },
    "edit_profile_button": {
        "en": "✏️ Edit Profile",
        "ru": "✏️ Редактировать профиль",
        "hy": "✏️ Խմբագրել պրոֆիլը",
    },
    
    # Menu buttons
    "btn_search": {
        "en": "🔍 Search",
        "ru": "🔍 Искать",
        "hy": "🔍 Որոնել",
    },
    "btn_next": {
        "en": "⏭ Next",
        "ru": "⏭ Следующий",
        "hy": "⏭ Հաջորդ",
    },
    "btn_stop": {
        "en": "🛑 Stop",
        "ru": "🛑 Стоп",
        "hy": "🛑 Կանգ",
    },
    "btn_profile": {
        "en": "👤 Profile",
        "ru": "👤 Профиль",
        "hy": "👤 Պրոֆիլ",
    },
    "btn_vip": {
        "en": "⭐ VIP",
        "ru": "⭐ VIP",
        "hy": "⭐ VIP",
    },
    "btn_rules": {
        "en": "📜 Rules",
        "ru": "📜 Правила",
        "hy": "📜 Կանոններ",
    },
    "btn_help": {
        "en": "🆘 Help",
        "ru": "🆘 Помощь",
        "hy": "🆘 Օգնություն",
    },
    
    # Language
    "language_changed": {
        "en": "✅ Language changed to English!",
        "ru": "✅ Язык изменен на русский!",
        "hy": "✅ Լեզուն փոխվել է հայերենի!",
    },
    "language_select": {
        "en": "🌐 Select your language:",
        "ru": "🌐 Выберите ваш язык:",
        "hy": "🌐 Ընտրեք ձեր լեզուն:",
    },
    "language_select_start": {
        "en": "👋 Select your language:",
        "ru": "👋 Выберите язык:",
        "hy": "👋 Ընտրեք լեզուն:",
    },
    "subscription_missing": {
        "en": "🔒 Please subscribe to our channels to use this bot:\n\n{channel_links}\n\nAfter subscribing, click the button below:",
        "ru": "🔒 Пожалуйста, подпишитесь на наши каналы, чтобы использовать этот бот:\n\n{channel_links}\n\nПосле подписки нажмите кнопку ниже:",
        "hy": "🔒 Խնդրում ենք բաժանորդագրվել մեր ալիքներին՝ այս բոտն օգտագործելու համար:\n\n{channel_links}\n\nԲաժանորդագրվելուց հետո սեղմեք ստորև գտնվող կոճակը:",
    },
    "subscription_btn": {
        "en": "✅ I Subscribed",
        "ru": "✅ Я подписался",
        "hy": "✅ Ես բաժանորդագրվել եմ",
    },
    "subscription_not_all": {
        "en": "❗️ You haven't joined all required channels yet.\nPlease subscribe to all channels and try again.",
        "ru": "❗️ Вы еще не подписались на все обязательные каналы.\nПожалуйста, подпишитесь на все каналы и попробуйте снова.",
        "hy": "❗️ Դուք դեռ բաժանորդագրված չեք բոլոր պարտադիր ալիքներին։\nԽնդրում ենք բաժանորդագրվել բոլոր ալիքներին և փորձել կրկին։",
    },
    "subscription_verified": {
        "en": "✅ Subscription verified! You can now use the bot.\n\nLet's complete your registration...",
        "ru": "✅ Подписка подтверждена! Теперь вы можете пользоваться ботом.\n\nДавайте завершим вашу регистрацию...",
        "hy": "✅ Բաժանորդագրությունը հաստատված է։ Այժմ կարող եք օգտագործել բոտը։\n\nԵկեք ավարտենք ձեր գրանցումը...",
    },

    # Admin
    "admin_usage_ban": {
        "en": "Usage: /ban <user_id | @username>",
        "ru": "Использование: /ban <user_id | @username>",
        "hy": "Օգտագործում՝ /ban <user_id | @username>",
    },
    "admin_usage_unban": {
        "en": "Usage: /unban <user_id | @username>",
        "ru": "Использование: /unban <user_id | @username>",
        "hy": "Օգտագործում՝ /unban <user_id | @username>",
    },
    "admin_usage_givevip": {
        "en": "Usage: /givevip <user_id | @username>",
        "ru": "Использование: /givevip <user_id | @username>",
        "hy": "Օգտագործում՝ /givevip <user_id | @username>",
    },
    "admin_usage_broadcast": {
        "en": "Usage: /broadcast <message>",
        "ru": "Использование: /broadcast <сообщение>",
        "hy": "Օգտագործում՝ /broadcast <հաղորդագրություն>",
    },
    "admin_invalid_target": {
        "en": "❗️ Invalid target (use numeric id or @username)",
        "ru": "❗️ Неверная цель (используйте числовой id или @username)",
        "hy": "❗️ Սխալ թիրախ (օգտագործեք թվային id կամ @username)",
    },
    "admin_unknown_target": {
        "en": "❗️ Unknown target. Use numeric id or @username. (User must have started the bot at least once.)",
        "ru": "❗️ Цель не найдена. Используйте числовой id или @username. (Пользователь должен хотя бы раз запустить бота.)",
        "hy": "❗️ Թիրախը չի գտնվել։ Օգտագործեք թվային id կամ @username։ (Օգտատերը պետք է գոնե մեկ անգամ մեկնարկած լինի բոտը։)",
    },
    "admin_unban_all_done": {
        "en": "✅ Unbanned {count} users.",
        "ru": "✅ Разблокировано пользователей: {count}.",
        "hy": "✅ Ապաարգելափակվեց {count} օգտատեր։",
    },
    "admin_unban_done": {
        "en": "✅ User {user_id} has been unbanned.",
        "ru": "✅ Пользователь {user_id} разбанен.",
        "hy": "✅ Օգտատերը {user_id} ապաարգելափակվել է։",
    },
    "admin_no_reports": {
        "en": "No recent reports.",
        "ru": "Нет недавних жалоб.",
        "hy": "Վերջին բողոքներ չկան։",
    },

    "admin_commands_list": {
        "en": (
            "🛠 Admin commands:\n\n"
            "/commands - Show this list\n"
            "/stats - Bot statistics\n"
            "/reports - Recent reports\n"
            "/ban <user_id | @username> - Ban user\n"
            "/unban <user_id | @username> - Unban user\n"
            "/unbanall - Unban everyone\n"
            "/givevip <user_id | @username> - Give VIP\n"
            "/broadcast <message> - Send message to all users"
        ),
        "ru": (
            "🛠 Команды администратора:\n\n"
            "/commands - Показать список\n"
            "/stats - Статистика бота\n"
            "/reports - Последние жалобы\n"
            "/ban <user_id | @username> - Забанить пользователя\n"
            "/unban <user_id | @username> - Разбанить пользователя\n"
            "/unbanall - Разбанить всех\n"
            "/givevip <user_id | @username> - Выдать VIP\n"
            "/broadcast <message> - Рассылка всем пользователям"
        ),
        "hy": (
            "🛠 Ադմինի հրամաններ՝\n\n"
            "/commands - Ցուցադրել ցանկը\n"
            "/stats - Բոտի վիճակագրություն\n"
            "/reports - Վերջին բողոքները\n"
            "/ban <user_id | @username> - Արգելափակել օգտատիրոջը\n"
            "/unban <user_id | @username> - Ապաարգելափակել օգտատիրոջը\n"
            "/unbanall - Ապաարգելափակել բոլորին\n"
            "/givevip <user_id | @username> - Տալ VIP\n"
            "/broadcast <message> - Ուղարկել բոլոր օգտատերերին"
        ),
    },
    
    # Errors
    "not_registered": {
        "en": "❗️ Please complete registration first by sending /start",
        "ru": "❗️ Пожалуйста, завершите регистрацию, отправив /start",
        "hy": "❗️ Խնդրում եմ նախ ավարտեք գրանցումը՝ ուղարկելով /start",
    },
    "banned": {
        "en": "🚫 You have been banned from using this bot due to violations.",
        "ru": "🚫 Вы были заблокированы за нарушения правил.",
        "hy": "🚫 Դուք արգելափակվել եք կանոնների խախտման պատճառով:",
    },
    "not_in_chat": {
        "en": "❗️ You're not in an active chat.\nUse /search to find a partner.",
        "ru": "❗️ Вы не в активном чате.\nИспользуйте /search, чтобы найти собеседника.",
        "hy": "❗️ Դուք ակտիվ զրույցում չեք։\nՕգտագործեք /search զրուցակից գտնելու համար:",
    },
    "links_not_allowed": {
        "en": "🚫 Links are not allowed in this chat.",
        "ru": "🚫 Ссылки запрещены в этом чате.",
        "hy": "🚫 Հղումները թույլատրված չեն այս զրույցում:",
    },
    "keep_respectful": {
        "en": "🚫 Please keep the conversation respectful.",
        "ru": "🚫 Пожалуйста, будьте вежливы в общении.",
        "hy": "🚫 Խնդրում եմ զրույցը պահեք հարգալից:",
    },
    
    # VIP expiration (for future multilingual VIP messages)
    "vip_expires_in": {
        "en": "⏰ Your VIP expires in {days} days",
        "ru": "⏰ Ваш VIP истекает через {days} дней",
        "hy": "⏰ Ձեր VIP-ը կլրանա {days} օրից",
    },
    "vip_expired": {
        "en": "⚠️ Your VIP subscription has expired!",
        "ru": "⚠️ Ваша VIP подписка истекла!",
        "hy": "⚠️ Ձեր VIP բաժանորդագրությունը լրացել է!",
    },
    "vip_lifetime": {
        "en": "👑 You have lifetime VIP status!",
        "ru": "👑 У вас пожизненный VIP статус!",
        "hy": "👑 Դուք ունեք մշտական VIP կարգավիճակ!",
    },
    
    # Atomic matchmaking messages
    "register_first": {
        "en": "❗️ Please complete registration first by sending /start",
        "ru": "❗️ Пожалуйста, сначала завершите регистрацию, отправив /start",
        "hy": "❗️ Խնդրում եմ նախ ավարտեք գրանցումը՝ ուղարկելով /start",
    },
    "banned": {
        "en": "🚫 You have been banned from using this bot due to violations.",
        "ru": "🚫 Вы забанены за нарушения.",
        "hy": "🚫 Դուք արգելափակված եք խախտումների համար։",
    },
    "already_in_chat": {
        "en": "❗️ You're already in a chat. Use /stop to end it first.",
        "ru": "❗️ Вы уже в чате. Используйте /stop чтобы завершить его.",
        "hy": "❗️ Դուք արդեն զրույցում եք։ Օգտագործեք /stop՝ ավարտելու համար։",
    },
    "already_searching": {
        "en": "⏳ You're already in the search queue. Please wait...",
        "ru": "⏳ Вы уже в очереди поиска. Пожалуйста, подождите...",
        "hy": "⏳ Դուք արդեն որոնման հերթում եք։ Խնդրում եմ սպասեք...",
    },
    "vip_choose_gender": {
        "en": "👑 VIP Search\n\nChoose who you want to match:",
        "ru": "👑 VIP Поиск\n\nВыберите, с кем хотите найти собеседника:",
        "hy": "👑 VIP Որոնում\n\nԸնտրեք ում հետ ցանկանում եք զրուցել:",
    },
    "match_found": {
        "en": "🔹 You are now connected to a partner! Say hi!",
        "ru": "🔹 Вы подключены к собеседнику! Поздоровайтесь!",
        "hy": "🔹 Դուք կապված եք զրուցակցի հետ! Ողջունեք!",
    },
    "searching": {
        "en": "🔍 Searching for a chat partner...\nYou'll be notified when someone is found.",
        "ru": "🔍 Ищем собеседника...\nМы уведомим вас, когда кто-то найдется.",
        "hy": "🔍 Որոնում ենք զրուցակից...\nԿտեղեկացնենք, երբ գտնենք։",
    },
    "not_in_chat_or_search": {
        "en": "❗️ You're not in an active chat or search.",
        "ru": "❗️ Вы не в активном чате и не в поиске.",
        "hy": "❗️ Դուք ակտիվ զրույցում կամ որոնման մեջ չեք։",
    },
    "search_cancelled": {
        "en": "🛑 Search cancelled.\nUse /search when you want to find a partner again.",
        "ru": "🛑 Поиск отменён.\nИспользуйте /search когда захотите найти собеседника снова.",
        "hy": "🛑 Որոնումը չեղարկվեց։\nՕգտագործեք /search երբ կրկին ցանկանաք գտնել զրուցակից։",
    },
    "partner_left": {
        "en": "🔸 Your partner has left the chat.\n\nUse /search to find a new partner.",
        "ru": "🔸 Ваш собеседник покинул чат.\n\nИспользуйте /search чтобы найти нового.",
        "hy": "🔸 Ձեր զրուցակիցը լքեց զրույցը։\n\nՕգտագործեք /search նոր զրուցակից գտնելու համար։",
    },
    "not_in_chat": {
        "en": "❗️ You're not in an active chat. Use /search to find a partner first.",
        "ru": "❗️ Вы не в активном чате. Используйте /search чтобы найти собеседника.",
        "hy": "❗️ Դուք ակտիվ զրույցում չեք։ Օգտագործեք /search գտնելու համար։",
    },
    "no_username": {
        "en": "❗️ You don't have a Telegram username set.\n\nSet one in Telegram Settings → Username, then try /sharelink again.",
        "ru": "❗️ У вас не установлен Telegram username.\n\nУстановите его в Настройках Telegram → Имя пользователя, затем попробуйте /sharelink снова.",
        "hy": "❗️ Դուք չունեք Telegram օգտանուն։\n\nԿարգավորեք Telegram Կարգավորումներ → Օգտանուն, ապա փորձեք /sharelink կրկին։",
    },
    "already_in_state": {
        "en": "❗️ You're already {state}. Please wait...",
        "ru": "❗️ Вы уже {state}. Пожалуйста, подождите...",
        "hy": "❗️ Դուք արդեն {state}։ Խնդրում եմ սպասեք...",
    },

    "gender_invalid": {
        "en": "❗️ Please select one of the available options: Male or Female.",
        "ru": "❗️ Пожалуйста, выберите один из доступных вариантов: Мужской или Женский.",
        "hy": "❗️ Խնդրում եմ ընտրեք հասանելի տարբերակներից մեկը՝ Արական կամ Իգական։",
    },

    "vip_search_preference_set": {
        "en": "👑 VIP Search preference: {label}\n\n🔍 Starting search...",
        "ru": "👑 VIP Поиск: предпочтение — {label}\n\n🔍 Начинаем поиск...",
        "hy": "👑 VIP Որոնում՝ նախընտրությունը՝ {label}\n\n🔍 Սկսում ենք որոնումը...",
    },

    "vip_label_boy": {
        "en": "Boy",
        "ru": "Парень",
        "hy": "Տղա",
    },
    "vip_label_girl": {
        "en": "Girl",
        "ru": "Девушка",
        "hy": "Աղջիկ",
    },
    "vip_label_random": {
        "en": "Random",
        "ru": "Случайно",
        "hy": "Պատահական",
    },

    "share_cancelled": {
        "en": "❌ Share cancelled.",
        "ru": "❌ Отправка отменена.",
        "hy": "❌ Ուղարկումը չեղարկվեց։",
    },
    "sharelink_shared": {
        "en": "✅ Your Telegram link was shared with your partner.",
        "ru": "✅ Ваша ссылка Telegram отправлена собеседнику.",
        "hy": "✅ Ձեր Telegram հղումը ուղարկվեց զրուցակցին։",
    },
    "invalid_gender_choice": {
        "en": "❗️ Invalid gender choice.",
        "ru": "❗️ Неверный выбор пола.",
        "hy": "❗️ Սեռի ընտրությունը սխալ է։",
    },
    "age_invalid_number_simple": {
        "en": "❗️ Please enter a valid number (12–99):",
        "ru": "❗️ Пожалуйста, введите правильное число (12–99):",
        "hy": "❗️ Խնդրում եմ մուտքագրեք ճիշտ թիվ (12–99):",
    },

    "thanks_report": {
        "en": "⛔ Thank you for your report. Our team will review this case.",
        "ru": "⛔ Спасибо за вашу жалобу. Наша команда рассмотрит этот случай.",
        "hy": "⛔ Շնորհակալություն ձեր բողոքի համար։ Մեր թիմը կուսումնասիրի այս դեպքը:",
    },
    "thanks_rating_with_type": {
        "en": "Thank you for rating your partner! ({rating_type})",
        "ru": "Спасибо за оценку собеседника! ({rating_type})",
        "hy": "Շնորհակալություն զրուցակցին գնահատելու համար։ ({rating_type})",
    },
    "age_invalid_range": {
        "en": "❗️ Age must be between 12 and 99. Please enter your age again:",
        "ru": "❗️ Возраст должен быть от 12 до 99. Пожалуйста, введите возраст снова:",
        "hy": "❗️ Տարիքը պետք է լինի 12-ից 99։ Խնդրում եմ մուտքագրեք տարիքը կրկին:",
    },
    "age_updated": {
        "en": "✅ Age updated!\n\nSend /profile to view your updated profile.",
        "ru": "✅ Возраст обновлён!\n\nОтправьте /profile чтобы посмотреть профиль.",
        "hy": "✅ Տարիքը թարմացվեց։\n\nՈւղարկեք /profile՝ տեսնելու համար ձեր պրոֆիլը։",
    },
    "no_links": {
        "en": "🚫 Links are not allowed in this chat.",
        "ru": "🚫 Ссылки запрещены в этом чате.",
        "hy": "🚫 Հղումները թույլատրված չեն այս զրույցում:",
    },
    "send_failed": {
        "en": "❗️ Failed to send message. Your partner may have left.",
        "ru": "❗️ Не удалось отправить сообщение. Возможно, собеседник вышел.",
        "hy": "❗️ Չհաջողվեց ուղարկել հաղորդագրությունը։ Հնարավոր է՝ զրուցակիցը դուրս է եկել։",
    },

    "sharelink_prompt": {
        "en": "🔗 Share your Telegram link with your partner?\n\nThis will send: https://t.me/{username}",
        "ru": "🔗 Поделиться вашей Telegram ссылкой с собеседником?\n\nБудет отправлено: https://t.me/{username}",
        "hy": "🔗 Կիսվել ձեր Telegram հղումով զրուցակցի հետ՞\n\nԿուղարկվի՝ https://t.me/{username}",
    },
    "sharelink_btn_share": {
        "en": "✅ Share",
        "ru": "✅ Отправить",
        "hy": "✅ Ուղարկել",
    },
    "sharelink_btn_cancel": {
        "en": "❌ Cancel",
        "ru": "❌ Отмена",
        "hy": "❌ Չեղարկել",
    },

    "edit_profile_title": {
        "en": "✏️ Edit Profile\n\nChoose what you want to change:",
        "ru": "✏️ Редактировать профиль\n\nВыберите, что хотите изменить:",
        "hy": "✏️ Խմբագրել պրոֆիլը\n\nԸնտրեք՝ ինչն եք ուզում փոխել:",
    },
    "edit_profile_btn_edit_age": {
        "en": "🎂 Edit Age",
        "ru": "🎂 Изменить возраст",
        "hy": "🎂 Փոխել տարիքը",
    },
    "edit_profile_btn_back": {
        "en": "⬅️ Back",
        "ru": "⬅️ Назад",
        "hy": "⬅️ Հետ",
    },
    "gender_updated": {
        "en": "✅ Gender updated to: {gender}\n\nSend /profile to view your updated profile.",
        "ru": "✅ Пол изменён на: {gender}\n\nОтправьте /profile чтобы посмотреть профиль.",
        "hy": "✅ Սեռը փոխվեց՝ {gender}\n\nՈւղարկեք /profile՝ տեսնելու համար ձեր պրոֆիլը։",
    },
    "edit_profile_enter_age": {
        "en": "🎂 Enter your new age (12–99):\n\nSend a number as a message.",
        "ru": "🎂 Введите ваш новый возраст (12–99):\n\nОтправьте число сообщением.",
        "hy": "🎂 Մուտքագրեք ձեր նոր տարիքը (12–99):\n\nՈւղարկեք թիվը հաղորդագրությամբ։",
    },
    "not_in_chat": {
        "en": "❗️ You're not in an active chat. Use /search to find a partner first.",
        "ru": "❗️ Вы не в активном чате. Используйте /search чтобы найти собеседника.",
        "hy": "❗️ Դուք ակտիվ զրույցում չեք։ Օգտագործեք /search գտնելու համար։",
    },
}

def get_text(key: str, lang: str = "en", **kwargs) -> str:
    """Get translated text by key and language code.
    
    Args:
        key: Translation key
        lang: Language code (en, ru, hy)
        **kwargs: Format arguments for string formatting
    
    Returns:
        Translated and formatted text
    """
    if lang not in ("en", "ru", "hy"):
        lang = "en"
    
    text = TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get("en", key))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text
