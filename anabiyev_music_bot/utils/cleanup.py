"""
Anabiyev Music Bot — vaqtinchalik fayllarni boshqarish.

Har bir foydalanuvchi/har bir jarayon uchun alohida (unique) papka
yaratiladi, shunda bir nechta foydalanuvchi bir vaqtda ishlaganda
fayllar bir-biriga aralashmaydi. Jarayon tugagach papka butunlay
o'chiriladi.
"""

import logging
import shutil
import uuid
from pathlib import Path

from config import TEMP_DIR

logger = logging.getLogger(__name__)


def create_user_temp_dir(user_id: int) -> Path:
    """
    Berilgan foydalanuvchi uchun unique vaqtinchalik papka yaratadi.

    Papka nomi user_id va tasodifiy uuid'dan iborat bo'lib, bir xil
    foydalanuvchi bir vaqtda bir nechta so'rov yuborsa ham ular
    to'qnashmaydi.
    """
    dir_name = f"{user_id}_{uuid.uuid4().hex}"
    path = Path(TEMP_DIR) / dir_name
    path.mkdir(parents=True, exist_ok=True)
    return path


def cleanup_dir(path: Path) -> None:
    """Berilgan papkani (va ichidagi barcha fayllarni) xavfsiz o'chiradi."""
    try:
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
    except Exception:
        logger.exception("Vaqtinchalik papkani tozalashda xatolik: %s", path)


def safe_remove_file(path: Path) -> None:
    """Bitta faylni xavfsiz o'chiradi (mavjud bo'lmasa e'tibor bermaydi)."""
    try:
        if path.exists():
            path.unlink()
    except Exception:
        logger.exception("Faylni o'chirishda xatolik: %s", path)
