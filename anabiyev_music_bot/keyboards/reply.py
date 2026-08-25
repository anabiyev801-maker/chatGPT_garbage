"""
Anabiyev Music Bot — doimiy (reply) klaviaturalar.
"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from utils.texts import t


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Asosiy menyu — har doim foydalanuvchi ekranining pastida turadi."""
    keyboard = [
        [KeyboardButton(text=t(lang, "btn_help"))],
        [KeyboardButton(text=t(lang, "btn_language"))],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
