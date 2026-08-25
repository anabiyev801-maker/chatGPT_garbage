"""
Anabiyev Music Bot — Shazam orqali qo'shiq aniqlash handlerlari.

Voice, audio, video yoki video-note (dumaloq video) sifatida kelgan
xabarlardan audio namuna olinadi, Shazam orqali qo'shiq aniqlanadi va
topilgan natija YouTube'dan qidiriladi.
"""

import logging

from aiogram import F, Router
from aiogram.types import Message

from keyboards.inline import format_selection_keyboard
from services import converter, recognizer, youtube
from utils.cleanup import cleanup_dir, create_user_temp_dir
from utils.store import store
from utils.texts import t

logger = logging.getLogger(__name__)

router = Router(name="shazam")

_AUDIO_VIDEO_MIME_PREFIXES = ("audio/", "video/")
_MIN_DURATION_SECONDS = 1


def _extract_target(message: Message):
    """Xabardan (file_id, duration, taxminiy kengaytma) ni ajratib oladi."""
    if message.voice:
        return message.voice.file_id, message.voice.duration, ".ogg"
    if message.audio:
        return message.audio.file_id, message.audio.duration, ".mp3"
    if message.video:
        return message.video.file_id, message.video.duration, ".mp4"
    if message.video_note:
        return message.video_note.file_id, message.video_note.duration, ".mp4"
    if message.document and message.document.mime_type:
        if message.document.mime_type.startswith(_AUDIO_VIDEO_MIME_PREFIXES):
            return message.document.file_id, None, ""
    return None, None, None


@router.message(F.voice | F.audio | F.video | F.video_note | F.document)
async def on_media_for_recognition(message: Message, lang: str) -> None:
    file_id, duration, ext = _extract_target(message)

    if file_id is None:
        # Bu holat faqat document turi audio/video bo'lmaganda yuz beradi
        # (masalan, oddiy PDF yoki rasm fayli yuborilganda) — e'tibor bermaymiz.
        return

    if duration is not None and duration < _MIN_DURATION_SECONDS:
        await message.answer(t(lang, "media_too_short"))
        return

    status = await message.answer(t(lang, "listening"))
    temp_dir = create_user_temp_dir(message.from_user.id)

    try:
        input_path = temp_dir / f"input{ext or '.bin'}"
        await message.bot.download(file_id, destination=input_path)

        sample_path = temp_dir / "sample.wav"
        extracted = await converter.extract_audio_sample(input_path, sample_path)

        if not extracted:
            await status.edit_text(t(lang, "recognize_failed"))
            return

        recognized = await recognizer.recognize_song(sample_path)

        if recognized is None:
            await status.edit_text(t(lang, "recognize_failed"))
            return

        artist = recognized["artist"]
        title = recognized["title"]
        query = f"{artist} {title}".strip() or title

        results = await youtube.search_youtube(query, limit=5)

        if not results:
            await status.edit_text(
                t(lang, "recognized_no_youtube", artist=artist or "?", title=title)
            )
            return

        best = results[0]
        token = store.put(
            {
                "type": "youtube",
                "id": best["id"],
                "url": best["url"],
                "title": best["title"],
            }
        )

        header = t(lang, "recognized", artist=artist or "?", title=title)
        footer = t(lang, "choose_format", title=best["title"])
        await status.edit_text(
            f"{header}\n\n{footer}",
            reply_markup=format_selection_keyboard(token, lang),
        )
    except Exception:
        logger.exception("Shazam aniqlash jarayonida xatolik")
        try:
            await status.edit_text(t(lang, "recognize_failed"))
        except Exception:
            pass
    finally:
        cleanup_dir(temp_dir)
