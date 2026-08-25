"""
Anabiyev Music Bot — barcha matnlar (O'zbek / English / Русский).

Har bir kalit uchun 3 tilda tarjima mavjud. Yangi matn qo'shganda
uni har uchala tilda ham to'ldirish shart.
"""

TEXTS: dict[str, dict[str, str]] = {
    "choose_language": {
        "uz": "🌐 Tilni tanlang:",
        "en": "🌐 Choose your language:",
        "ru": "🌐 Выберите язык:",
    },
    "language_set": {
        "uz": "✅ Til o'zbekcha qilib o'rnatildi.",
        "en": "✅ Language set to English.",
        "ru": "✅ Язык установлен на русский.",
    },
    "welcome": {
        "uz": (
            "🎧 <b>Anabiyev Music Bot</b>ga xush kelibsiz!\n\n"
            "Menga quyidagilarni yuborishingiz mumkin:\n"
            "🎵 Qo'shiq nomi — YouTube'dan qidirib beraman\n"
            "🔗 YouTube/Instagram/TikTok/Facebook link — yuklab beraman\n"
            "🎤 Ovozli xabar (voice) — qo'shiqni aniqlab beraman\n"
            "🎬 Video yoki 🎵 Audio fayl — qo'shiqni aniqlab beraman\n\n"
            "Boshlash uchun shunchaki xabar yuboring! 👇"
        ),
        "en": (
            "🎧 Welcome to <b>Anabiyev Music Bot</b>!\n\n"
            "You can send me:\n"
            "🎵 Song name — I'll search it on YouTube\n"
            "🔗 YouTube/Instagram/TikTok/Facebook link — I'll download it\n"
            "🎤 Voice message — I'll recognize the song\n"
            "🎬 Video or 🎵 Audio file — I'll recognize the song\n\n"
            "Just send a message to get started! 👇"
        ),
        "ru": (
            "🎧 Добро пожаловать в <b>Anabiyev Music Bot</b>!\n\n"
            "Вы можете отправить мне:\n"
            "🎵 Название песни — я найду её на YouTube\n"
            "🔗 Ссылку YouTube/Instagram/TikTok/Facebook — я скачаю медиа\n"
            "🎤 Голосовое сообщение — я распознаю песню\n"
            "🎬 Видео или 🎵 Аудио файл — я распознаю песню\n\n"
            "Просто отправьте сообщение, чтобы начать! 👇"
        ),
    },
    "btn_help": {
        "uz": "ℹ️ Yordam",
        "en": "ℹ️ Help",
        "ru": "ℹ️ Помощь",
    },
    "btn_language": {
        "uz": "🌐 Til / Language",
        "en": "🌐 Language",
        "ru": "🌐 Язык",
    },
    "help_text": {
        "uz": (
            "ℹ️ <b>Yordam</b>\n\n"
            "1️⃣ Qo'shiq nomini yozing — men YouTube'dan qidiraman.\n"
            "2️⃣ Havola (link) yuboring — men uni to'g'ridan-to'g'ri yuklab beraman.\n"
            "3️⃣ Ovozli xabar, video yoki audio yuboring — men Shazam orqali "
            "qo'shiqni aniqlayman.\n"
            "4️⃣ Har bir qo'shiq uchun 🎵 MP3, 🎬 Video yoki ⭕ Dumaloq video "
            "formatini tanlashingiz mumkin."
        ),
        "en": (
            "ℹ️ <b>Help</b>\n\n"
            "1️⃣ Type a song name — I'll search it on YouTube.\n"
            "2️⃣ Send a link — I'll download the media directly.\n"
            "3️⃣ Send a voice message, video or audio — I'll recognize the "
            "song using Shazam.\n"
            "4️⃣ For every song you can choose 🎵 MP3, 🎬 Video or ⭕ Round "
            "video format."
        ),
        "ru": (
            "ℹ️ <b>Помощь</b>\n\n"
            "1️⃣ Напишите название песни — я найду её на YouTube.\n"
            "2️⃣ Отправьте ссылку — я скачаю медиа напрямую.\n"
            "3️⃣ Отправьте голосовое сообщение, видео или аудио — я распознаю "
            "песню через Shazam.\n"
            "4️⃣ Для каждой песни можно выбрать формат 🎵 MP3, 🎬 Видео или "
            "⭕ Кружок (video note)."
        ),
    },
    "searching": {
        "uz": "🔎 Qidirilmoqda, biroz kuting...",
        "en": "🔎 Searching, please wait...",
        "ru": "🔎 Идёт поиск, подождите...",
    },
    "no_results": {
        "uz": "😕 Hech narsa topilmadi. Boshqa nom bilan urinib ko'ring.",
        "en": "😕 Nothing found. Try a different search term.",
        "ru": "😕 Ничего не найдено. Попробуйте другой запрос.",
    },
    "choose_track": {
        "uz": "🎶 Natijalardan birini tanlang:",
        "en": "🎶 Choose one of the results:",
        "ru": "🎶 Выберите один из результатов:",
    },
    "choose_format": {
        "uz": "🎧 <b>{title}</b>\n\nQaysi formatda olmoqchisiz?",
        "en": "🎧 <b>{title}</b>\n\nWhich format would you like?",
        "ru": "🎧 <b>{title}</b>\n\nВ каком формате скачать?",
    },
    "btn_mp3": {
        "uz": "🎵 MP3",
        "en": "🎵 MP3",
        "ru": "🎵 MP3",
    },
    "btn_video": {
        "uz": "🎬 Video",
        "en": "🎬 Video",
        "ru": "🎬 Видео",
    },
    "btn_round": {
        "uz": "⭕ Dumaloq video",
        "en": "⭕ Round video",
        "ru": "⭕ Кружок",
    },
    "btn_back": {
        "uz": "🔙 Orqaga",
        "en": "🔙 Back",
        "ru": "🔙 Назад",
    },
    "back_to_search": {
        "uz": "🔍 Yangi qidiruv uchun qo'shiq nomi yoki link yuboring.",
        "en": "🔍 Send a song name or a link to search again.",
        "ru": "🔍 Отправьте название песни или ссылку для нового поиска.",
    },
    "expired": {
        "uz": "⌛ Bu so'rovning muddati tugagan. Iltimos, qaytadan qidiring.",
        "en": "⌛ This request has expired. Please search again.",
        "ru": "⌛ Срок действия запроса истёк. Пожалуйста, найдите заново.",
    },
    "preparing_mp3": {
        "uz": "🎵 MP3 tayyorlanmoqda, biroz kuting...",
        "en": "🎵 Preparing MP3, please wait...",
        "ru": "🎵 Готовим MP3, подождите...",
    },
    "preparing_video": {
        "uz": "🎬 Video tayyorlanmoqda, biroz kuting...",
        "en": "🎬 Preparing video, please wait...",
        "ru": "🎬 Готовим видео, подождите...",
    },
    "preparing_round": {
        "uz": "⭕ Dumaloq video tayyorlanmoqda, biroz kuting...",
        "en": "⭕ Preparing round video, please wait...",
        "ru": "⭕ Готовим кружок, подождите...",
    },
    "download_failed": {
        "uz": "❌ Yuklab bo'lmadi. Qayta urinib ko'ring yoki boshqa qo'shiq tanlang.",
        "en": "❌ Download failed. Please try again or choose another song.",
        "ru": "❌ Не удалось скачать. Попробуйте снова или выберите другую песню.",
    },
    "file_too_large": {
        "uz": "❌ Fayl juda katta ({size} MB). Telegram orqali yuborib bo'lmaydi.",
        "en": "❌ File is too large ({size} MB). Cannot be sent via Telegram.",
        "ru": "❌ Файл слишком большой ({size} MB). Невозможно отправить через Telegram.",
    },
    "round_failed": {
        "uz": "❌ Dumaloq videoni tayyorlab bo'lmadi. Video juda uzun yoki noto'g'ri formatda bo'lishi mumkin.",
        "en": "❌ Could not create the round video. It may be too long or in an unsupported format.",
        "ru": "❌ Не удалось создать видео-кружок. Возможно, видео слишком длинное или в неподдерживаемом формате.",
    },
    "unsupported_link": {
        "uz": "❌ Bu link qo'llab-quvvatlanmaydi. YouTube, Instagram, TikTok, Facebook yoki Telegram linklarini yuboring.",
        "en": "❌ This link isn't supported. Please send a YouTube, Instagram, TikTok, Facebook or Telegram link.",
        "ru": "❌ Эта ссылка не поддерживается. Отправьте ссылку YouTube, Instagram, TikTok, Facebook или Telegram.",
    },
    "link_processing": {
        "uz": "🔗 Havola tekshirilmoqda...",
        "en": "🔗 Checking the link...",
        "ru": "🔗 Проверяем ссылку...",
    },
    "link_failed": {
        "uz": "❌ Bu havoladan ma'lumot olib bo'lmadi. Havola to'g'riligini tekshiring.",
        "en": "❌ Couldn't fetch info from this link. Please check that it's correct.",
        "ru": "❌ Не удалось получить информацию по ссылке. Проверьте правильность ссылки.",
    },
    "listening": {
        "uz": "👂 Tinglanmoqda, qo'shiq aniqlanmoqda...",
        "en": "👂 Listening, recognizing the song...",
        "ru": "👂 Слушаю, распознаю песню...",
    },
    "recognize_failed": {
        "uz": (
            "😕 Musiqani aniqlab bo'lmadi.\n"
            "Iltimos, aniqroq va kamida 5-10 soniyalik ovoz/video yuboring."
        ),
        "en": (
            "😕 Couldn't recognize the song.\n"
            "Please send a clearer audio/video of at least 5-10 seconds."
        ),
        "ru": (
            "😕 Не удалось распознать песню.\n"
            "Пожалуйста, отправьте более чёткое аудио/видео длительностью хотя бы 5-10 секунд."
        ),
    },
    "recognized": {
        "uz": "🎯 Topildi: <b>{artist} — {title}</b>",
        "en": "🎯 Found: <b>{artist} — {title}</b>",
        "ru": "🎯 Найдено: <b>{artist} — {title}</b>",
    },
    "recognized_no_youtube": {
        "uz": "🎯 Aniqlandi: <b>{artist} — {title}</b>\n\n😕 Lekin YouTube'da mos natija topilmadi.",
        "en": "🎯 Recognized: <b>{artist} — {title}</b>\n\n😕 But no matching result found on YouTube.",
        "ru": "🎯 Распознано: <b>{artist} — {title}</b>\n\n😕 Но подходящий результат на YouTube не найден.",
    },
    "media_too_short": {
        "uz": "⚠️ Media juda qisqa. Aniqlash uchun kamida bir necha soniyalik audio kerak.",
        "en": "⚠️ Media is too short. At least a few seconds of audio is needed for recognition.",
        "ru": "⚠️ Медиа слишком короткое. Для распознавания нужно хотя бы несколько секунд аудио.",
    },
    "generic_error": {
        "uz": "⚠️ Kutilmagan xatolik yuz berdi. Iltimos, birozdan so'ng qayta urinib ko'ring.",
        "en": "⚠️ An unexpected error occurred. Please try again in a moment.",
        "ru": "⚠️ Произошла непредвиденная ошибка. Пожалуйста, попробуйте снова чуть позже.",
    },
    "ready": {
        "uz": "✅ Tayyor!",
        "en": "✅ Done!",
        "ru": "✅ Готово!",
    },
}


def all_variants(key: str) -> list[str]:
    """Berilgan kalitning barcha tillardagi variantlarini ro'yxat qilib qaytaradi."""
    entry = TEXTS.get(key, {})
    return list(entry.values())


def t(lang: str, key: str, **kwargs) -> str:
    """
    Berilgan til va kalit bo'yicha matnni qaytaradi.

    Agar til yoki kalit topilmasa, xavfsiz fallback sifatida
    o'zbek tilidagi matn (yoki kalitning o'zi) qaytariladi.
    """
    entry = TEXTS.get(key)
    if entry is None:
        return key

    text = entry.get(lang) or entry.get("uz") or next(iter(entry.values()))

    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass

    return text
