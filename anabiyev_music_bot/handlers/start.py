"""
Anabiyev Music Bot — /start, til tanlash va asosiy menyu handlerlari.
"""

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from config import SUPPORTED_LANGUAGES
from database import db
from keyboards.inline import language_keyboard
from keyboards.reply import main_menu_keyboard
from utils.texts import all_variants, t

logger = logging.getLogger(__name__)

router = Router(name="start")


@router.message(Command("start"))
async def cmd_start(message: Message, lang: str) -> None:
    saved_lang = await db.get_user_language(message.from_user.id)

    if saved_lang is None:
        await message.answer(t(lang, "choose_language"), reply_markup=language_keyboard())
        return

    await message.answer(t(saved_lang, "welcome"), reply_markup=main_menu_keyboard(saved_lang))


@router.callback_query(F.data.startswith("lang:"))
async def on_language_selected(callback: CallbackQuery, lang: str) -> None:
    new_lang = callback.data.split(":", 1)[1]
    if new_lang not in SUPPORTED_LANGUAGES:
        await callback.answer()
        return

    await db.set_user_language(callback.from_user.id, new_lang)

    if callback.message:
        await callback.message.edit_text(t(new_lang, "language_set"))
        await callback.message.answer(
            t(new_lang, "welcome"), reply_markup=main_menu_keyboard(new_lang)
        )

    await callback.answer()


@router.message(F.text.in_(all_variants("btn_language")))
async def on_language_button(message: Message, lang: str) -> None:
    await message.answer(t(lang, "choose_language"), reply_markup=language_keyboard())


@router.message(F.text.in_(all_variants("btn_help")))
async def on_help_button(message: Message, lang: str) -> None:
    await message.answer(t(lang, "help_text"))


@router.message(Command("help"))
async def cmd_help(message: Message, lang: str) -> None:
    await message.answer(t(lang, "help_text"))
