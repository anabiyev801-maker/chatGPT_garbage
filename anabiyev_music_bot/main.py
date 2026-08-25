"""
Anabiyev Music Bot — asosiy ishga tushirish fayli.

Ishga tushirish:
    python main.py
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, setup_logging
from database import db
from handlers import download, search, shazam, start
from middlewares import ErrorLoggingMiddleware, LanguageMiddleware

logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging()
    logger.info("Anabiyev Music Bot ishga tushmoqda...")

    await db.init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Middleware'lar — har bir Message/CallbackQuery uchun ishlaydi
    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())
    dp.message.middleware(ErrorLoggingMiddleware())
    dp.callback_query.middleware(ErrorLoggingMiddleware())

    # Routerlar — tartib muhim: aniqroq filtrlar avval, umumiy matn
    # handler (search) oxirroqda turadi
    dp.include_router(start.router)
    dp.include_router(shazam.router)
    dp.include_router(search.router)
    dp.include_router(download.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
