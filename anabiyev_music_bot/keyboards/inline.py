"""
Anabiyev Music Bot — inline klaviaturalar.
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.texts import t

_MAX_TITLE_LEN = 55


def language_keyboard() -> InlineKeyboardMarkup:
    """Til tanlash uchun inline klaviatura."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbekcha", callback_data="lang:uz")
    builder.button(text="🇬🇧 English", callback_data="lang:en")
    builder.button(text="🇷🇺 Русский", callback_data="lang:ru")
    builder.adjust(1)
    return builder.as_markup()


def search_results_keyboard(
    results: list[dict],
    lang: str,
    tokens: list[str],
) -> InlineKeyboardMarkup:
    """
    YouTube qidiruv natijalari ro'yxati uchun inline klaviatura.

    `results` va `tokens` bir xil uzunlikda va bir xil tartibda bo'lishi kerak
    (results[i] natijasiga tokens[i] tokeni mos keladi).
    """
    builder = InlineKeyboardBuilder()

    for result, token in zip(results, tokens):
        title = result.get("title") or "Nomsiz"
        duration = result.get("duration_text") or ""
        label = f"{title} {duration}".strip()
        if len(label) > _MAX_TITLE_LEN:
            label = label[: _MAX_TITLE_LEN - 1] + "…"
        builder.row(
            InlineKeyboardButton(text=label, callback_data=f"select:{token}")
        )

    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="back:menu")
    )
    return builder.as_markup()


def format_selection_keyboard(token: str, lang: str) -> InlineKeyboardMarkup:
    """MP3 / Video / Round video formatlarini tanlash uchun klaviatura."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_mp3"), callback_data=f"fmt:mp3:{token}"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_video"), callback_data=f"fmt:video:{token}"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_round"), callback_data=f"fmt:round:{token}"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="back:search"),
    )
    return builder.as_markup()
