"""
Anabiyev Music Bot — global middleware.

Har bir kelayotgan Message/CallbackQuery uchun:
* foydalanuvchini database'da mavjudligini ta'minlaydi;
* uning tilini aniqlab, handler'ga `lang` argumenti sifatida uzatadi.

Bu har bir handler ichida bir xil kodni takrorlashning oldini oladi.
"""

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from database import db
from config import DEFAULT_LANGUAGE

logger = logging.getLogger(__name__)


class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = None
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user

        if user is not None:
            try:
                await db.ensure_user(user.id, user.username, user.full_name)
                lang = await db.get_language_or_default(user.id)
            except Exception:
                logger.exception("LanguageMiddleware: db bilan ishlashda xatolik")
                lang = DEFAULT_LANGUAGE
            data["lang"] = lang
        else:
            data["lang"] = DEFAULT_LANGUAGE

        return await handler(event, data)


class ErrorLoggingMiddleware(BaseMiddleware):
    """Har qanday handler xatoligini ushlab, botni to'xtatmaydi."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception:
            logger.exception("Handler ichida kutilmagan xatolik yuz berdi")

            try:
                lang = data.get("lang", DEFAULT_LANGUAGE)
                from utils.texts import t

                if isinstance(event, Message):
                    await event.answer(t(lang, "generic_error"))
                elif isinstance(event, CallbackQuery):
                    if event.message:
                        await event.message.answer(t(lang, "generic_error"))
                    await event.answer()
            except Exception:
                logger.exception("Xatolik haqida foydalanuvchiga xabar berishda ham xatolik")

            return None
