"""
Anabiyev Music Bot — vaqtinchalik xotira (in-memory) do'koni.

Telegram inline tugmalarining `callback_data` maydoni 64 baytdan
oshmasligi kerak, shuning uchun uzun narsalarni (YouTube video ID,
to'liq URL, sarlavha va h.k.) to'g'ridan-to'g'ri callback_data ichiga
yozish o'rniga, biz ularni shu yerda qisqa token ostida saqlaymiz.

Bu oddiy LRU (eng eski kirim birinchi o'chiriladi) do'kon bo'lib,
xotira cheksiz o'sib ketmasligi uchun maksimal hajmga ega.
"""

import secrets
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Optional

_MAX_ITEMS = 1000
_TTL_SECONDS = 3600  # 1 soat


@dataclass
class _Entry:
    data: dict[str, Any]
    created_at: float = field(default_factory=time.time)


class TokenStore:
    """Oddiy thread-unsafe (lekin asyncio single-thread uchun yetarli) LRU do'kon."""

    def __init__(self, max_items: int = _MAX_ITEMS, ttl_seconds: int = _TTL_SECONDS):
        self._max_items = max_items
        self._ttl_seconds = ttl_seconds
        self._data: "OrderedDict[str, _Entry]" = OrderedDict()

    def put(self, data: dict[str, Any]) -> str:
        """Ma'lumotni saqlaydi va unga mos qisqa tokenni qaytaradi."""
        self._evict_if_needed()

        token = secrets.token_urlsafe(6)  # ~8 belgi
        while token in self._data:
            token = secrets.token_urlsafe(6)

        self._data[token] = _Entry(data=data)
        self._data.move_to_end(token)
        return token

    def get(self, token: str) -> Optional[dict[str, Any]]:
        """Token bo'yicha ma'lumotni qaytaradi (yoki None, agar topilmasa/muddati tugagan bo'lsa)."""
        entry = self._data.get(token)
        if entry is None:
            return None

        if time.time() - entry.created_at > self._ttl_seconds:
            del self._data[token]
            return None

        self._data.move_to_end(token)
        return entry.data

    def _evict_if_needed(self) -> None:
        # Muddati o'tganlarni tozalash
        now = time.time()
        expired = [
            key for key, entry in self._data.items()
            if now - entry.created_at > self._ttl_seconds
        ]
        for key in expired:
            del self._data[key]

        # Hali ham juda ko'p bo'lsa, eng eskilarini o'chirish
        while len(self._data) >= self._max_items:
            self._data.popitem(last=False)


# Butun ilova bo'ylab bitta umumiy do'kon
store = TokenStore()
