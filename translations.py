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
    "profile_vip_days": {
        "en": "👑 VIP Member ({days} days remaining)",
        "ru": "👑 VIP Участник (осталось {days} дн.)",
        "hy": "👑 VIP Անդամ ({days} օր մնացել է)",
    },

    "vip_renew_button": {
        "en": "🔄 Renew VIP",
        "ru": "🔄 Продлить VIP",
        "hy": "🔄 Թարմացնել VIP-ը",
    },
    "vip_buy_button": {
        "en": "⭐ Buy VIP",
        "ru": "⭐ Купить VIP",
        "hy": "⭐ Գնել VIP",
    },
    "vip_choose_plan": {
        "en": "⭐ Choose a VIP plan:",
        "ru": "⭐ Выберите VIP тариф:",
        "hy": "⭐ Ընտրեք VIP փաթեթը՝",
    },
    "vip_plan_button": {
        "en": "{days} days — {stars} Stars",
        "ru": "{days} дн. — {stars} Stars",
        "hy": "{days} օր — {stars} Stars",
    },
    "vip_active_text": {
        "en": "👑 You are a VIP Member!\n\n⏰ Your VIP expires in {days} days\n\nVIP Benefits:\n• Choose partner gender\n• See partner's age and gender\n• Priority matching\n• Special VIP badge\n\n💡 You can renew your subscription anytime!",
        "ru": "👑 У вас VIP статус!\n\n⏰ Ваш VIP истекает через {days} дн.\n\nПреимущества VIP:\n• Выбор пола собеседника\n• Просмотр пола и возраста собеседника\n• Приоритет в поиске\n• Специальный VIP значок\n\n💡 Вы можете продлить подписку в любой момент!",
        "hy": "👑 Դուք VIP անդամ եք։\n\n⏰ Ձեր VIP-ը կլրանա {days} օրից\n\nVIP առավելություններ՝\n• Ընտրել զրուցակցի սեռը\n• Տեսնել զրուցակցի սեռն ու տարիքը\n• Առաջնահերթ որոնում\n• Հատուկ VIP նշան\n\n💡 Կարող եք թարմացնել բաժանորդագրությունը ցանկացած պահին։",
    },
    "vip_expired_text": {
        "en": "⚠️ Your VIP subscription has expired!\n\nRenew now to get back:\n• Choose partner gender\n• See partner's age and gender\n• Priority matching\n• Special VIP badge\n\nAvailable plans:\n{plans}",
        "ru": "⚠️ Ваша VIP подписка истекла!\n\nПродлите сейчас, чтобы снова получить:\n• Выбор пола собеседника\n• Просмотр пола и возраста собеседника\n• Приоритет в поиске\n• Специальный VIP значок\n\nДоступные тарифы:\n{plans}",
        "hy": "⚠️ Ձեր VIP բաժանորդագրությունը լրացել է։\n\nԹարմացրեք հիմա, որպեսզի կրկին ստանաք՝\n• Զրուցակցի սեռի ընտրություն\n• Զրուցակցի սեռի և տարիքի տեսանելիություն\n• Առաջնահերթ որոնում\n• Հատուկ VIP նշան\n\nՀասանելի փաթեթներ՝\n{plans}",
    },
    "vip_lifetime_text": {
        "en": "👑 You have lifetime VIP status!\n\nVIP Benefits:\n• Choose partner gender\n• See partner's age and gender\n• Priority matching\n• Special VIP badge",
        "ru": "👑 У вас пожизненный VIP статус!\n\nПреимущества VIP:\n• Выбор пола собеседника\n• Просмотр пола и возраста собеседника\n• Приоритет в поиске\n• Специальный VIP значок",
        "hy": "👑 Դուք ունեք ցմահ VIP կարգավիճակ։\n\nVIP առավելություններ՝\n• Ընտրել զրուցակցի սեռը\n• Տեսնել զրուցակցի սեռն ու տարիքը\n• Առաջնահերթ որոնում\n• Հատուկ VIP նշան",
    },
    "vip_info_text": {
        "en": "👑 VIP Membership Benefits:\n\n✅ Choose your partner's gender before matching\n✅ See your partner's age and gender during chats\n✅ Priority matching in the queue\n✅ Special VIP badge in your profile\n✅ Support the bot development\n\nAvailable plans:\n{plans}\n\nUpgrade now to enhance your anonymous chat experience!",
        "ru": "👑 Преимущества VIP подписки:\n\n✅ Выбор пола собеседника перед поиском\n✅ Просмотр пола и возраста собеседника во время чата\n✅ Приоритет в очереди поиска\n✅ Специальный VIP значок в профиле\n✅ Поддержка развития бота\n\nДоступные тарифы:\n{plans}\n\nУлучшите свой анонимный чат уже сейчас!",
        "hy": "👑 VIP բաժանորդագրության առավելությունները՝\n\n✅ Ընտրել զրուցակցի սեռը մինչև որոնումը\n✅ Տեսնել զրուցակցի սեռն ու տարիքը զրույցի ընթացքում\n✅ Առաջնահերթ հերթ որոնման մեջ\n✅ Հատուկ VIP նշան պրոֆիլում\n✅ Աջակցել բոտի զարգացմանը\n\nՀասանելի փաթեթներ՝\n{plans}\n\nԹարմացրեք հիմա՝ ձեր անանուն զրույցը բարելավելու համար։",
    },
    "vip_invoice_title": {
        "en": "VIP Membership ({days} days)",
        "ru": "VIP Подписка ({days} дн.)",
        "hy": "VIP Բաժանորդագրություն ({days} օր)",
    },
    "vip_invoice_description": {
        "en": "Get VIP status for {days} days with exclusive benefits!",
        "ru": "Получите VIP статус на {days} дн. с эксклюзивными преимуществами!",
        "hy": "Ստացեք VIP կարգավիճակ {days} օրով բացառիկ առավելություններով։",
    },
    "vip_payment_success": {
        "en": "🎉 Congratulations! You are now a VIP member!\n\n✨ Your VIP subscription is active for {days} days\n\nVIP Benefits:\n• Choose your partner's gender\n• See partner's age and gender\n• Priority matching\n• Special VIP badge\n\n💡 Use /vip to check your subscription status anytime!",
        "ru": "🎉 Поздравляем! Теперь у вас VIP статус!\n\n✨ Ваша VIP подписка активна {days} дн.\n\nПреимущества VIP:\n• Выбор пола собеседника\n• Просмотр пола и возраста собеседника\n• Приоритет в поиске\n• Специальный VIP значок\n\n💡 Используйте /vip, чтобы проверить статус подписки в любое время!",
        "hy": "🎉 Շնորհավորում ենք։ Այժմ դուք VIP անդամ եք։\n\n✨ Ձեր VIP բաժանորդագրությունը ակտիվ է {days} օր\n\nVIP առավելություններ՝\n• Ընտրել զրուցակցի սեռը\n• Տեսնել զրուցակցի սեռն ու տարիքը\n• Առաջնահերթ որոնում\n• Հատուկ VIP նշան\n\n💡 Օգտագործեք /vip՝ ցանկացած պահին բաժանորդագրության կարգավիճակը ստուգելու համար։",
    },
    "rules_text": {
        "en": "📜 Chat Rules\n\n1️⃣ No sharing of links or external contact info\n2️⃣ Be respectful - harassment and hate speech are not allowed\n3️⃣ No spam, scams, or fraudulent activities\n4️⃣ No explicit, sexual, or inappropriate content\n5️⃣ No impersonation or misleading information\n6️⃣ Use the rating system to report bad behavior\n\n⚠️ Violation of these rules may result in:\n• Warnings\n• Temporary or permanent ban\n• Reported to admins\n\nRemember: Your chats are anonymous to your matches, but admins can trace your Telegram ID if you get reported.\n\nBe kind and enjoy chatting! 💬",
        "ru": "📜 Правила чата\n\n1️⃣ Нельзя делиться ссылками или внешними контактами\n2️⃣ Будьте уважительны: травля и язык ненависти запрещены\n3️⃣ Никакого спама, мошенничества и обмана\n4️⃣ Никакого откровенного, сексуального или неприемлемого контента\n5️⃣ Никакого выдавания себя за другого или введения в заблуждение\n6️⃣ Используйте систему оценок, чтобы сообщать о плохом поведении\n\n⚠️ Нарушение этих правил может привести к:\n• Предупреждениям\n• Временному или постоянному бану\n• Жалобе администраторам\n\nПомните: ваши чаты анонимны для собеседников, но администраторы могут установить ваш Telegram ID, если на вас пожалуются.\n\nБудьте вежливы и приятного общения! 💬",
        "hy": "📜 Զրույցի կանոններ\n\n1️⃣ Մի կիսվեք հղումներով կամ արտաքին կոնտակտներով\n2️⃣ Եղեք հարգալից. հետապնդումն ու ատելության խոսքը արգելված են\n3️⃣ Ոչ մի սպամ, խաբեություն կամ կեղծ գործունեություն\n4️⃣ Ոչ մի բացահայտ, սեռական կամ անպատշաճ բովանդակություն\n5️⃣ Մի ներկայացեք ուրիշի անունից և մի մոլորեցրեք\n6️⃣ Օգտագործեք գնահատման համակարգը վատ վարքագիծը հայտնելու համար\n\n⚠️ Այս կանոնների խախտումը կարող է հանգեցնել՝\n• Զգուշացման\n• Ժամանակավոր կամ մշտական արգելափակման\n• Բողոքի ադմիններին\n\nՀիշեք. ձեր զրույցները անանուն են զրուցակիցների համար, բայց բողոքի դեպքում ադմինները կարող են պարզել ձեր Telegram ID-ն։\n\nԵղեք բարի և հաճելի զրույց մաղթում ենք։ 💬",
    },
    "help_text": {
        "en": "🤖 Anonymous Chat Bot Help\n\nCommands:\n/start - Start the bot and register\n/search - Find a random chat partner\n/stop - End current chat\n/next - Find next partner\n/profile - View/edit your profile\n/vip - Learn about VIP membership\n/rules - View chat rules\n/help - Show this help message\n\nHow it works:\n1️⃣ Register with your gender and age\n2️⃣ Use /search to find a random partner\n3️⃣ Chat anonymously - your identity is hidden\n4️⃣ Rate your partner after each chat\n5️⃣ Use /next to find a new partner anytime\n\n💡 Tip: Upgrade to VIP to see your partner's info!",
        "ru": "🤖 Помощь по анонимному чат-боту\n\nКоманды:\n/start - Запустить бота и зарегистрироваться\n/search - Найти случайного собеседника\n/stop - Завершить текущий чат\n/next - Найти следующего собеседника\n/profile - Просмотреть или изменить профиль\n/vip - Узнать о VIP подписке\n/rules - Посмотреть правила чата\n/help - Показать это сообщение\n\nКак это работает:\n1️⃣ Зарегистрируйтесь, указав пол и возраст\n2️⃣ Используйте /search, чтобы найти случайного собеседника\n3️⃣ Общайтесь анонимно: ваша личность скрыта\n4️⃣ Оценивайте собеседника после каждого чата\n5️⃣ Используйте /next, чтобы в любой момент найти нового собеседника\n\n💡 Совет: оформите VIP, чтобы видеть информацию о собеседнике!",
        "hy": "🤖 Անանուն չաթ բոտի օգնություն\n\nՀրամաններ՝\n/start - Մեկնարկել բոտը և գրանցվել\n/search - Գտնել պատահական զրուցակից\n/stop - Ավարտել ընթացիկ զրույցը\n/next - Գտնել հաջորդ զրուցակցին\n/profile - Տեսնել կամ խմբագրել պրոֆիլը\n/vip - Տեղեկանալ VIP բաժանորդագրության մասին\n/rules - Տեսնել զրույցի կանոնները\n/help - Ցույց տալ այս օգնությունը\n\nԻնչպես է աշխատում՝\n1️⃣ Գրանցվեք՝ նշելով սեռը և տարիքը\n2️⃣ Օգտագործեք /search պատահական զրուցակից գտնելու համար\n3️⃣ Զրուցեք անանուն. ձեր ինքնությունը թաքնված է\n4️⃣ Ամեն զրույցից հետո գնահատեք զրուցակցին\n5️⃣ Օգտագործեք /next ցանկացած պահին նոր զրուցակից գտնելու համար\n\n💡 Խորհուրդ. միացրեք VIP-ը, որպեսզի տեսնեք զրուցակցի տվյալները։",
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
    "subscription_not_all_with_channels": {
        "en": "❗️ You haven't joined all required channels yet.\n\nPlease subscribe to these channels:\n\n{channel_links}\n\nAfter subscribing, click the button below again:",
        "ru": "❗️ Вы еще не подписались на все обязательные каналы.\n\nПожалуйста, подпишитесь на эти каналы:\n\n{channel_links}\n\nПосле подписки снова нажмите кнопку ниже:",
        "hy": "❗️ Դուք դեռ բաժանորդագրված չեք բոլոր պարտադիր ալիքներին։\n\nԽնդրում ենք բաժանորդագրվել այս ալիքներին՝\n\n{channel_links}\n\nԲաժանորդագրվելուց հետո կրկին սեղմեք ստորև գտնվող կոճակը:",
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
        "en": "Usage: /givevip <user_id | @username> <days>",
        "ru": "Использование: /givevip <user_id | @username> <days>",
        "hy": "Օգտագործում՝ /givevip <user_id | @username> <days>",
    },
    "admin_usage_takevip": {
        "en": "Usage: /takevip <user_id | @username>",
        "ru": "Использование: /takevip <user_id | @username>",
        "hy": "Օգտագործում՝ /takevip <user_id | @username>",
    },
    "admin_usage_viplist": {
        "en": "Usage: /viplist",
        "ru": "Использование: /viplist",
        "hy": "Օգտագործում՝ /viplist",
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
    "admin_invalid_days": {
        "en": "❗️ Days must be a positive number.",
        "ru": "❗️ Количество дней должно быть положительным числом.",
        "hy": "❗️ Օրերի քանակը պետք է լինի դրական թիվ։",
    },
    "admin_vip_granted_target": {
        "en": "🎉 You have been granted VIP status by an admin for {days} days!",
        "ru": "🎉 Администратор выдал вам VIP статус на {days} дн.!",
        "hy": "🎉 Ադմինը ձեզ տվել է VIP կարգավիճակ {days} օրով։",
    },
    "admin_vip_granted_done": {
        "en": "✅ VIP status granted to user {user_id} for {days} days.",
        "ru": "✅ Пользователю {user_id} выдан VIP на {days} дн.",
        "hy": "✅ {user_id} օգտատիրոջը տրվեց VIP {days} օրով։",
    },
    "admin_vip_removed_target": {
        "en": "ℹ️ Your VIP status was removed by an admin.",
        "ru": "ℹ️ Администратор снял ваш VIP статус.",
        "hy": "ℹ️ Ադմինը հեռացրել է ձեր VIP կարգավիճակը։",
    },
    "admin_vip_removed_done": {
        "en": "✅ VIP status removed from user {user_id}.",
        "ru": "✅ У пользователя {user_id} снят VIP статус.",
        "hy": "✅ {user_id} օգտատիրոջ VIP կարգավիճակը հեռացվեց։",
    },
    "admin_viplist_empty": {
        "en": "No active VIP users.",
        "ru": "Нет активных VIP пользователей.",
        "hy": "Ակտիվ VIP օգտատերեր չկան։",
    },
    "admin_viplist_header": {
        "en": "👑 VIP users: {count}\n",
        "ru": "👑 VIP пользователи: {count}\n",
        "hy": "👑 VIP օգտատերեր՝ {count}\n",
    },
    "admin_viplist_user_label": {
        "en": "@{username} | ID: {user_id}",
        "ru": "@{username} | ID: {user_id}",
        "hy": "@{username} | ID: {user_id}",
    },
    "admin_viplist_user_id_only": {
        "en": "ID: {user_id}",
        "ru": "ID: {user_id}",
        "hy": "ID: {user_id}",
    },
    "admin_viplist_line_days": {
        "en": "{index}. {user_label}\n   ⏳ {days} days left",
        "ru": "{index}. {user_label}\n   ⏳ Осталось {days} дн.",
        "hy": "{index}. {user_label}\n   ⏳ Մնացել է {days} օր",
    },
    "admin_viplist_line_lifetime": {
        "en": "{index}. {user_label}\n   ♾ Lifetime VIP",
        "ru": "{index}. {user_label}\n   ♾ Пожизненный VIP",
        "hy": "{index}. {user_label}\n   ♾ Ցմահ VIP",
    },
    "help_admin_block": {
        "en": "\n\nAdmin commands:\n/commands - Show admin command list\n/stats - Bot statistics\n/reports - Recent reports\n/ban <user_id | @username> - Ban user\n/unban <user_id | @username> - Unban user\n/unbanall - Unban everyone\n/givevip <user_id | @username> <days> - Grant VIP for a number of days\n/takevip <user_id | @username> - Remove VIP\n/viplist - Show VIP users and days left\n/broadcast <message> - Send announcement to all users",
        "ru": "\n\nКоманды администратора:\n/commands - Показать список команд администратора\n/stats - Статистика бота\n/reports - Последние жалобы\n/ban <user_id | @username> - Забанить пользователя\n/unban <user_id | @username> - Разбанить пользователя\n/unbanall - Разбанить всех\n/givevip <user_id | @username> <days> - Выдать VIP на нужное число дней\n/takevip <user_id | @username> - Снять VIP\n/viplist - Показать VIP пользователей и сколько дней осталось\n/broadcast <message> - Отправить объявление всем пользователям",
        "hy": "\n\nԱդմինի հրամաններ՝\n/commands - Ցույց տալ ադմինի հրամանների ցանկը\n/stats - Բոտի վիճակագրություն\n/reports - Վերջին բողոքները\n/ban <user_id | @username> - Արգելափակել օգտատիրոջը\n/unban <user_id | @username> - Ապաարգելափակել օգտատիրոջը\n/unbanall - Ապաարգելափակել բոլորին\n/givevip <user_id | @username> <days> - Տալ VIP նշված օրերի համար\n/takevip <user_id | @username> - Հեռացնել VIP\n/viplist - Ցույց տալ VIP օգտատերերին և մնացած օրերը\n/broadcast <message> - Հայտարարություն ուղարկել բոլոր օգտատերերին",
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
            "/givevip <user_id | @username> <days> - Give VIP\n"
            "/takevip <user_id | @username> - Remove VIP\n"
            "/viplist - Show VIP users and days left\n"
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
            "/givevip <user_id | @username> <days> - Выдать VIP\n"
            "/takevip <user_id | @username> - Снять VIP\n"
            "/viplist - Показать VIP и оставшиеся дни\n"
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
            "/givevip <user_id | @username> <days> - Տալ VIP\n"
            "/takevip <user_id | @username> - Հեռացնել VIP\n"
            "/viplist - Ցուցադրել VIP-ներին և մնացած օրերը\n"
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
    "vip_match_upsell": {
        "en": "\n\nTo view your partner's gender, age, and ratings, buy VIP: /vip",
        "ru": "\n\nЧтобы видеть пол, возраст и оценки собеседника, купите VIP: /vip",
        "hy": "\n\nԶրուցակցի սեռը, տարիքը և գնահատականները տեսնելու համար գնեք VIP՝ /vip",
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
