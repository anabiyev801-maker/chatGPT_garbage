"""
Anabiyev Music Bot — Shazam orqali qo'shiq aniqlash servisi.

ShazamIO tabiiy ravishda asyncio ustida ishlaydi, shuning uchun uni
to'g'ridan-to'g'ri (to_thread'siz) `await` qilamiz.
"""

import logging
from pathlib import Path
from typing import Optional

from shazamio import Shazam

logger = logging.getLogger(__name__)


async def recognize_song(audio_path: Path) -> Optional[dict]:
    """
    Berilgan audio fayldan qo'shiqni aniqlashga urinadi.

    Muvaffaqiyatli bo'lsa {"title": str, "artist": str} qaytaradi,
    aks holda None.
    """
    try:
        shazam = Shazam()
        result = await shazam.recognize(str(audio_path))
    except Exception:
        logger.exception("Shazam orqali aniqlashda xatolik: %s", audio_path)
        return None

    if not result:
        return None

    track = result.get("track")
    if not track:
        return None

    title = track.get("title")
    artist = track.get("subtitle")

    if not title:
        return None

    return {
        "title": title,
        "artist": artist or "",
    }
