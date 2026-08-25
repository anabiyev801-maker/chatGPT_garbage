"""
Anabiyev Music Bot — yuklab olish va yetkazib berish handlerlari.

Foydalanuvchi format (MP3 / Video / Dumaloq video) tanlagach, shu
yerda haqiqiy yuklash, kerak bo'lsa konvertatsiya va Telegram orqali
yuborish amalga oshiriladi. Har bir so'rov uchun alohida vaqtinchalik
papka ishlatiladi va oxirida albatta tozalanadi.
"""

import logging
from pathlib import Path
from typing import Optional

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, Message

from config import MAX_FILE_SIZE_MB, ROUND_VIDEO_SIZE
from services import converter, youtube
from utils.cleanup import cleanup_dir, create_user_temp_dir
from utils.store import store
from utils.texts import t

logger = logging.getLogger(__name__)

router = Router(name="download")

_ROUND_DOWNLOAD_MAX_HEIGHT = 480
_VIDEO_DOWNLOAD_MAX_HEIGHT = 720


def _resolve_url(item: dict) -> str:
    if item["type"] == "youtube":
        return item.get("url") or f"https://www.youtube.com/watch?v={item['id']}"
    return item["url"]


def _file_size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)


@router.callback_query(F.data.startswith("fmt:"))
async def on_format_selected(callback: CallbackQuery, lang: str) -> None:
    try:
        _, fmt, token = callback.data.split(":", 2)
    except ValueError:
        await callback.answer()
        return

    item = store.get(token)
    if item is None:
        if callback.message:
            await callback.message.answer(t(lang, "expired"))
        await callback.answer()
        return

    await callback.answer()

    anchor = callback.message
    if anchor is None:
        return

    url = _resolve_url(item)
    title = item.get("title") or "Media"
    user_id = callback.from_user.id

    if fmt == "mp3":
        await _send_mp3(anchor, lang, url, title, user_id)
    elif fmt == "video":
        await _send_video(anchor, lang, url, title, user_id)
    elif fmt == "round":
        await _send_round_video(anchor, lang, url, title, user_id)


async def _safe_edit(status: Optional[Message], text: str) -> None:
    if status is None:
        return
    try:
        await status.edit_text(text)
    except Exception:
        pass


async def _send_mp3(anchor: Message, lang: str, url: str, title: str, user_id: int) -> None:
    status = await anchor.answer(t(lang, "preparing_mp3"))
    temp_dir = create_user_temp_dir(user_id)

    try:
        mp3_path = await youtube.download_audio(url, str(temp_dir))

        if mp3_path is None or not mp3_path.exists():
            await status.edit_text(t(lang, "download_failed"))
            return

        size_mb = _file_size_mb(mp3_path)
        if size_mb > MAX_FILE_SIZE_MB:
            await status.edit_text(t(lang, "file_too_large", size=round(size_mb, 1)))
            return

        await anchor.answer_audio(
            FSInputFile(mp3_path),
            title=title[:64],
            caption=f"🎵 {title}"[:1024],
        )
        await status.delete()
    except Exception:
        logger.exception("MP3 yuborishda xatolik: %s", url)
        await _safe_edit(status, t(lang, "download_failed"))
    finally:
        cleanup_dir(temp_dir)


async def _send_video(anchor: Message, lang: str, url: str, title: str, user_id: int) -> None:
    status = await anchor.answer(t(lang, "preparing_video"))
    temp_dir = create_user_temp_dir(user_id)

    try:
        video_path = await youtube.download_video(url, str(temp_dir), max_height=_VIDEO_DOWNLOAD_MAX_HEIGHT)

        if video_path is None or not video_path.exists():
            await status.edit_text(t(lang, "download_failed"))
            return

        size_mb = _file_size_mb(video_path)
        if size_mb > MAX_FILE_SIZE_MB:
            await status.edit_text(t(lang, "file_too_large", size=round(size_mb, 1)))
            return

        await anchor.answer_video(
            FSInputFile(video_path),
            caption=f"🎬 {title}"[:1024],
            supports_streaming=True,
        )
        await status.delete()
    except Exception:
        logger.exception("Video yuborishda xatolik: %s", url)
        await _safe_edit(status, t(lang, "download_failed"))
    finally:
        cleanup_dir(temp_dir)


async def _send_round_video(anchor: Message, lang: str, url: str, title: str, user_id: int) -> None:
    status = await anchor.answer(t(lang, "preparing_round"))
    temp_dir = create_user_temp_dir(user_id)

    try:
        source_path = await youtube.download_video(
            url, str(temp_dir), max_height=_ROUND_DOWNLOAD_MAX_HEIGHT
        )

        if source_path is None or not source_path.exists():
            await status.edit_text(t(lang, "download_failed"))
            return

        round_path = temp_dir / "round_note.mp4"
        success = await converter.make_round_video(source_path, round_path)

        if not success or not round_path.exists():
            await status.edit_text(t(lang, "round_failed"))
            return

        size_mb = _file_size_mb(round_path)
        if size_mb > MAX_FILE_SIZE_MB:
            await status.edit_text(t(lang, "file_too_large", size=round(size_mb, 1)))
            return

        await anchor.answer_video_note(
            FSInputFile(round_path),
            length=ROUND_VIDEO_SIZE,
        )
        await status.delete()
    except Exception:
        logger.exception("Dumaloq video yuborishda xatolik: %s", url)
        await _safe_edit(status, t(lang, "round_failed"))
    finally:
        cleanup_dir(temp_dir)
