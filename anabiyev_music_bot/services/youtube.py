"""
Anabiyev Music Bot — YouTube va boshqa platformalar bilan ishlash servisi.

yt-dlp orqali:
* matn bo'yicha YouTube qidiruvi
* to'g'ridan-to'g'ri link (YouTube/Instagram/TikTok/Facebook/Telegram)
  haqida ma'lumot olish
* audio (MP3) va video yuklab olish

yt-dlp o'zi sinxron (blocking) kutubxona bo'lgani uchun barcha og'ir
chaqiriqlar `asyncio.to_thread` orqali alohida thread'da bajariladi —
shu bilan asyncio event loop bloklanmaydi.
"""

import asyncio
import logging
import re
import time
import uuid
from pathlib import Path
from typing import Optional

import yt_dlp

from config import COOKIE_FILE, SEARCH_CACHE_TTL, SEARCH_RESULTS_LIMIT

logger = logging.getLogger(__name__)

_URL_RE = re.compile(r"^https?://", re.IGNORECASE)

_PLATFORM_PATTERNS = {
    "youtube": re.compile(r"(youtube\.com|youtu\.be)", re.IGNORECASE),
    "instagram": re.compile(r"instagram\.com", re.IGNORECASE),
    "tiktok": re.compile(r"tiktok\.com", re.IGNORECASE),
    "facebook": re.compile(r"(facebook\.com|fb\.watch)", re.IGNORECASE),
    "telegram": re.compile(r"t\.me", re.IGNORECASE),
}

# query -> (timestamp, results) — sodda in-memory qidiruv keshi
_search_cache: dict[str, tuple[float, list[dict]]] = {}


def is_url(text: str) -> bool:
    """Berilgan matn URL ekanligini tekshiradi."""
    return bool(_URL_RE.match(text.strip()))


def get_platform(url: str) -> Optional[str]:
    """URL qaysi platformaga tegishli ekanligini aniqlaydi."""
    for platform, pattern in _PLATFORM_PATTERNS.items():
        if pattern.search(url):
            return platform
    return None


def _base_options() -> dict:
    """Barcha yt-dlp chaqiriqlari uchun umumiy sozlamalar."""
    options = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "geo_bypass": True,
        "socket_timeout": 20,
        "retries": 3,
    }
    if COOKIE_FILE:
        options["cookiefile"] = COOKIE_FILE
    return options


def _format_duration(seconds: Optional[int]) -> str:
    if not seconds:
        return ""
    seconds = int(seconds)
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"({hours}:{minutes:02d}:{secs:02d})"
    return f"({minutes}:{secs:02d})"


def _sync_search(query: str, limit: int) -> list[dict]:
    """YouTube'da qidiradi (sinxron, thread ichida chaqiriladi)."""
    options = _base_options()
    options["extract_flat"] = "in_playlist"
    options["default_search"] = f"ytsearch{limit}"
    options["skip_download"] = True

    results: list[dict] = []
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(query, download=False)
        entries = info.get("entries") if info else None
        if not entries:
            return results

        for entry in entries:
            if not entry:
                continue
            video_id = entry.get("id")
            if not video_id:
                continue
            results.append(
                {
                    "id": video_id,
                    "title": entry.get("title") or "Nomsiz",
                    "uploader": entry.get("uploader") or entry.get("channel") or "",
                    "duration": entry.get("duration"),
                    "duration_text": _format_duration(entry.get("duration")),
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                }
            )
    return results


async def search_youtube(query: str, limit: int = SEARCH_RESULTS_LIMIT) -> list[dict]:
    """
    YouTube'dan qidiradi, natijalarni qaytaradi.

    Bir xil so'rov qisqa vaqt ichida qayta yuborilsa, keshdan javob
    beriladi (ortiqcha tarmoq so'rovlarini kamaytirish uchun).
    """
    cache_key = query.strip().lower()
    cached = _search_cache.get(cache_key)
    if cached and (time.time() - cached[0]) < SEARCH_CACHE_TTL:
        logger.info("Qidiruv keshdan olindi: %s", query)
        return cached[1]

    try:
        results = await asyncio.to_thread(_sync_search, query, limit)
    except Exception:
        logger.exception("YouTube qidiruvida xatolik: %s", query)
        return []

    _search_cache[cache_key] = (time.time(), results)
    return results


def _sync_get_info(url: str) -> Optional[dict]:
    """Berilgan URL haqida ma'lumot oladi (yuklamasdan)."""
    options = _base_options()
    options["skip_download"] = True
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
        if info is None:
            return None
        if "entries" in info and info["entries"]:
            info = info["entries"][0]
        return {
            "id": info.get("id"),
            "title": info.get("title") or "Nomsiz",
            "uploader": info.get("uploader") or info.get("channel") or "",
            "duration": info.get("duration"),
            "webpage_url": info.get("webpage_url") or url,
        }


async def get_info(url: str) -> Optional[dict]:
    """Link haqida ma'lumotni asinxron oladi."""
    try:
        return await asyncio.to_thread(_sync_get_info, url)
    except Exception:
        logger.exception("Link haqida ma'lumot olishda xatolik: %s", url)
        return None


def _sync_download_audio(url: str, dest_dir: str) -> Optional[Path]:
    """URL'dan audio yuklab, MP3 formatiga o'giradi (sinxron)."""
    out_template = str(Path(dest_dir) / f"{uuid.uuid4().hex}.%(ext)s")
    options = _base_options()
    options.update(
        {
            "format": "bestaudio/best",
            "outtmpl": out_template,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
    )
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        if "entries" in info and info["entries"]:
            info = info["entries"][0]
        filename = ydl.prepare_filename(info)
        mp3_path = Path(filename).with_suffix(".mp3")
        if mp3_path.exists():
            return mp3_path
        # Ba'zi hollarda kengaytma boshqacha bo'lishi mumkin — papkani tekshiramiz
        for candidate in Path(dest_dir).glob("*.mp3"):
            return candidate
        return None


async def download_audio(url: str, dest_dir: str) -> Optional[Path]:
    """MP3 audio yuklab oladi, tayyor faylning yo'lini qaytaradi."""
    try:
        return await asyncio.to_thread(_sync_download_audio, url, dest_dir)
    except Exception:
        logger.exception("Audio yuklashda xatolik: %s", url)
        return None


def _sync_download_video(url: str, dest_dir: str, max_height: int = 720) -> Optional[Path]:
    """URL'dan video yuklab oladi (sinxron), MP4 formatida."""
    out_template = str(Path(dest_dir) / f"{uuid.uuid4().hex}.%(ext)s")
    options = _base_options()
    options.update(
        {
            "format": (
                f"bestvideo[height<={max_height}][ext=mp4]+bestaudio[ext=m4a]/"
                f"best[height<={max_height}][ext=mp4]/best"
            ),
            "outtmpl": out_template,
            "merge_output_format": "mp4",
        }
    )
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        if "entries" in info and info["entries"]:
            info = info["entries"][0]
        filename = ydl.prepare_filename(info)
        video_path = Path(filename)
        if not video_path.exists():
            video_path = video_path.with_suffix(".mp4")
        if video_path.exists():
            return video_path
        for candidate in sorted(Path(dest_dir).glob("*")):
            if candidate.suffix.lower() in (".mp4", ".mkv", ".webm"):
                return candidate
        return None


async def download_video(url: str, dest_dir: str, max_height: int = 720) -> Optional[Path]:
    """Video yuklab oladi, tayyor faylning yo'lini qaytaradi."""
    try:
        return await asyncio.to_thread(_sync_download_video, url, dest_dir, max_height)
    except Exception:
        logger.exception("Video yuklashda xatolik: %s", url)
        return None
