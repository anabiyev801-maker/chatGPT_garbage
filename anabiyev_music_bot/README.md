# 🎧 Anabiyev Music Bot

Telegram uchun to'liq ishlaydigan musiqa boti. YouTube'dan qidiradi va
yuklaydi, linklarni (YouTube/Instagram/TikTok/Facebook) qabul qiladi,
MP3/Video/Dumaloq video (video note) formatlarini beradi va Shazam
orqali voice/video/audio'dan qo'shiqni aniqlaydi. O'zbek, English,
Русский tillarini qo'llab-quvvatlaydi.

## Loyiha strukturasi

```
anabiyev_music_bot/
├── main.py                 # ishga tushirish nuqtasi
├── config.py                # .env, yo'llar, logging sozlamalari
├── middlewares.py            # til aniqlash + global error handling
├── requirements.txt
├── .env.example
├── database/
│   └── db.py                 # aiosqlite: users, search_history
├── handlers/
│   ├── start.py               # /start, til tanlash, /help
│   ├── search.py               # matn: qidiruv yoki link aniqlash
│   ├── download.py             # MP3 / Video / Round video yuborish
│   └── shazam.py               # voice/audio/video'dan aniqlash
├── keyboards/
│   ├── reply.py                # doimiy pastki menyu
│   └── inline.py                # til, natijalar, format tugmalari
├── services/
│   ├── youtube.py               # yt-dlp: qidiruv, ma'lumot, yuklash
│   ├── converter.py             # ffmpeg: audio namuna, round video
│   └── recognizer.py            # shazamio orqali aniqlash
└── utils/
    ├── texts.py                  # UZ/EN/RU tarjimalar
    ├── store.py                   # callback_data uchun token do'koni
    └── cleanup.py                  # foydalanuvchiga xos temp papkalar
```

## O'rnatish

1. **Tizim talablari:** Python 3.12+, va `ffmpeg` (+ `ffprobe`) tizimda
   o'rnatilgan bo'lishi shart.

   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg

   # macOS (Homebrew)
   brew install ffmpeg
   ```

2. **Virtual environment va kutubxonalar:**

   ```bash
   cd anabiyev_music_bot
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Sozlash:**

   ```bash
   cp .env.example .env
   ```

   `.env` faylini oching va `BOT_TOKEN` qiymatiga @BotFather'dan olingan
   tokenni kiriting.

## Ishga tushirish

```bash
python main.py
```

Bot ishga tushgach, Telegram'da botingizga `/start` yuboring.

## Eslatmalar

- `downloads/` va `logs/` papkalari avtomatik yaratiladi; `downloads/tmp/`
  ichidagi vaqtinchalik fayllar har bir so'rovdan so'ng avtomatik
  o'chiriladi.
- Agar ba'zi YouTube videolari login talab qilsa, brauzeringizdan
  eksport qilingan `cookies.txt` faylini loyiha papkasiga qo'ying
  (Netscape formatida) — bot uni avtomatik topadi.
- `MAX_FILE_SIZE_MB` qiymatidan katta fayllar Telegram orqali
  yuborilmaydi (Telegram Bot API cheklovi tufayli) — foydalanuvchiga
  tushunarli xabar chiqadi.
