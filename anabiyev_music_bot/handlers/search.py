"""
Anabiyev Music Bot — matn xabarlarini qayta ishlash: qidiruv va linklar.

Bu yerda eng muhim mantiq: foydalanuvchi yuborgan matn URL bo'lsa,
u to'g'ridan-to'g'ri link sifatida qayta ishlanadi (qidiruv so'roviga
aylantirilmaydi). Aks holda YouTube qidiruvi bajariladi.
"""

import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from database import db
from keyboards.inline import format_selection_keyboard, search_results_keyboard
from services import youtube
from utils.store import store
from utils.texts import t

logger = logging.getLogger(__name__)

router = Router(name="search")


@router.message(F.text & ~F.text.startswith("/"))
async def on_text_message(message: Message, lang: str) -> None:
    text = message.text.strip()

    if youtube.is_url(text):
        await _handle_url(message, lang, text)
    else:
        await _handle_search(message, lang, text)


async def _handle_url(message: Message, lang: str, url: str) -> None:
    platform = youtube.get_platform(url)
    if platform is None:
        await message.answer(t(lang, "unsupported_link"))
        return

    status_message = await message.answer(t(lang, "link_processing"))

    info = await youtube.get_info(url)

    if info is None:
        await status_message.edit_text(t(lang, "link_failed"))
        return

    token = store.put(
        {
            "type": "direct",
            "url": info.get("webpage_url") or url,
            "title": info.get("title") or "Media",
        }
    )

    title = info.get("title") or "Media"
    await status_message.edit_text(
        t(lang, "choose_format", title=title),
        reply_markup=format_selection_keyboard(token, lang),
    )


async def _handle_search(message: Message, lang: str, query: str) -> None:
    status_message = await message.answer(t(lang, "searching"))

    try:
        await db.log_search(message.from_user.id, query)
    except Exception:
        logger.exception("Qidiruv tarixini yozishda xatolik")

    results = await youtube.search_youtube(query)

    if not results:
        await status_message.edit_text(t(lang, "no_results"))
        return

    tokens = []
    for result in results:
        token = store.put(
            {
                "type": "youtube",
                "id": result["id"],
                "url": result["url"],
                "title": result["title"],
            }
        )
        tokens.append(token)

    await status_message.edit_text(
        t(lang, "choose_track"),
        reply_markup=search_results_keyboard(results, lang, tokens),
    )


@router.callback_query(F.data.startswith("select:"))
async def on_track_selected(callback: CallbackQuery, lang: str) -> None:
    token = callback.data.split(":", 1)[1]
    item = store.get(token)

    if item is None:
        if callback.message:
            await callback.message.edit_text(t(lang, "expired"))
        await callback.answer()
        return

    title = item.get("title") or "Media"

    if callback.message:
        await callback.message.edit_text(
            t(lang, "choose_format", title=title),
            reply_markup=format_selection_keyboard(token, lang),
        )
    await callback.answer()


@router.callback_query(F.data == "back:search")
async def on_back_to_search(callback: CallbackQuery, lang: str) -> None:
    if callback.message:
        await callback.message.edit_text(t(lang, "back_to_search"))
    await callback.answer()


@router.callback_query(F.data == "back:menu")
async def on_back_to_menu(callback: CallbackQuery, lang: str) -> None:
    if callback.message:
        await callback.message.edit_text(t(lang, "back_to_search"))
    await callback.answer()
