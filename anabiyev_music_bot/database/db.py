"""
Anabiyev Music Bot — database qatlami.

SQLite (aiosqlite) orqali foydalanuvchilarni va ularning
tanlagan tilini saqlaydi.
"""

import logging

import aiosqlite

from config import DATABASE_PATH, DEFAULT_LANGUAGE

logger = logging.getLogger(__name__)

_CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    username    TEXT,
    full_name   TEXT,
    language    TEXT,
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

_CREATE_SEARCH_LOG_TABLE = """
CREATE TABLE IF NOT EXISTS search_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    query       TEXT NOT NULL,
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


async def init_db() -> None:
    """Database va kerakli jadvallarni yaratadi (agar mavjud bo'lmasa)."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(_CREATE_USERS_TABLE)
        await db.execute(_CREATE_SEARCH_LOG_TABLE)
        await db.commit()
    logger.info("Database tayyor: %s", DATABASE_PATH)


async def ensure_user(user_id: int, username: str | None, full_name: str | None) -> None:
    """Foydalanuvchi mavjud bo'lmasa, uni database'ga qo'shadi."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name
            """,
            (user_id, username, full_name),
        )
        await db.commit()


async def get_user_language(user_id: int) -> str | None:
    """Foydalanuvchining saqlangan tilini qaytaradi (yoki None, agar tanlanmagan bo'lsa)."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT language FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row and row[0]:
                return row[0]
            return None


async def set_user_language(user_id: int, language: str) -> None:
    """Foydalanuvchi tilini saqlaydi."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?",
            (language, user_id),
        )
        await db.commit()


async def get_language_or_default(user_id: int) -> str:
    """Til tanlanmagan bo'lsa ham har doim bitta til qaytaradi."""
    lang = await get_user_language(user_id)
    return lang or DEFAULT_LANGUAGE


async def log_search(user_id: int, query: str) -> None:
    """Qidiruv so'rovini tarixga yozadi (statistik/keyingi optimizatsiya uchun)."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO search_history (user_id, query) VALUES (?, ?)",
            (user_id, query),
        )
        await db.commit()
