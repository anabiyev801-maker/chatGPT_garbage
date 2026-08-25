"""
Anabiyev Music Bot — konfiguratsiya moduli.

Bu modul .env faylidan sozlamalarni o'qiydi va loyihada
ishlatiladigan barcha yo'llarni (path) tayyorlaydi.
"""

import os
import logging

from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------------------------------------
# Asosiy yo'llar
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
TEMP_DIR = os.path.join(DOWNLOAD_DIR, "tmp")
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "music.db")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "bot.log")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# Bot token
# ----------------------------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN topilmadi! Loyiha papkasida .env fayl yarating "
        "(.env.example namunasiga qarang) va BOT_TOKEN qiymatini kiriting."
    )

# ----------------------------------------------------------------------
# yt-dlp uchun ixtiyoriy cookie fayli (login talab qiladigan videolar uchun)
# ----------------------------------------------------------------------
_cookie_file_name = os.getenv("COOKIE_FILE", "cookies.txt").strip()
_cookie_path = os.path.join(BASE_DIR, _cookie_file_name)
COOKIE_FILE = _cookie_path if os.path.isfile(_cookie_path) else None

# ----------------------------------------------------------------------
# Boshqa sozlamalar
# ----------------------------------------------------------------------
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
SEARCH_RESULTS_LIMIT = int(os.getenv("SEARCH_RESULTS_LIMIT", "10"))
SHAZAM_SAMPLE_SECONDS = int(os.getenv("SHAZAM_SAMPLE_SECONDS", "20"))
ROUND_VIDEO_MAX_SECONDS = int(os.getenv("ROUND_VIDEO_MAX_SECONDS", "60"))
ROUND_VIDEO_SIZE = int(os.getenv("ROUND_VIDEO_SIZE", "480"))  # px (kvadrat)
SEARCH_CACHE_TTL = int(os.getenv("SEARCH_CACHE_TTL", "600"))  # soniya

DEFAULT_LANGUAGE = "uz"
SUPPORTED_LANGUAGES = ("uz", "en", "ru")

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logging() -> None:
    """Bot uchun logging'ni sozlaydi (konsol + fayl)."""
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)

    # Eski handlerlarni tozalash (qayta ishga tushirilganda dublikat bo'lmasin)
    root_logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Uchinchi tomon kutubxonalarning ortiqcha loglarini kamaytiramiz
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    logging.getLogger("yt_dlp").setLevel(logging.WARNING)
    logging.getLogger("shazamio").setLevel(logging.WARNING)
