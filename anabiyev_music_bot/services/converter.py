"""
Anabiyev Music Bot — media konvertatsiya servisi (FFmpeg orqali).

Barcha chaqiriqlar `asyncio.create_subprocess_exec` orqali bajariladi,
shuning uchun event loop bloklanmaydi (FFmpeg alohida process sifatida
ishlaydi).
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional

from config import ROUND_VIDEO_MAX_SECONDS, ROUND_VIDEO_SIZE, SHAZAM_SAMPLE_SECONDS

logger = logging.getLogger(__name__)


async def _run(args: list[str], timeout: int = 120) -> tuple[bool, str]:
    """Berilgan komandani ishga tushiradi va (muvaffaqiyat, stderr) qaytaradi."""
    try:
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            _, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            logger.error("Komanda timeout bo'ldi: %s", " ".join(args))
            return False, "timeout"

        stderr_text = stderr.decode(errors="ignore") if stderr else ""

        if process.returncode != 0:
            logger.error("Komanda muvaffaqiyatsiz (%s): %s", process.returncode, stderr_text[-500:])
            return False, stderr_text

        return True, stderr_text
    except FileNotFoundError:
        logger.error("Dastur topilmadi: %s. FFmpeg o'rnatilganini tekshiring.", args[0])
        return False, "ffmpeg not found"
    except Exception:
        logger.exception("Komandani ishga tushirishda xatolik: %s", " ".join(args))
        return False, "unknown error"


async def get_duration_seconds(input_path: Path) -> Optional[float]:
    """ffprobe orqali media fayl uzunligini (soniyada) qaytaradi."""
    args = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(input_path),
    ]
    try:
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await asyncio.wait_for(process.communicate(), timeout=30)
        text = stdout.decode(errors="ignore").strip()
        return float(text) if text else None
    except Exception:
        logger.exception("Media uzunligini aniqlashda xatolik: %s", input_path)
        return None


async def extract_audio_sample(
    input_path: Path,
    output_path: Path,
    seconds: int = SHAZAM_SAMPLE_SECONDS,
) -> bool:
    """
    Kiruvchi media (voice/audio/video) fayldan Shazam uchun mos
    audio namunasini (mono, 44100Hz, WAV) chiqaradi.
    """
    args = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-t", str(seconds),
        "-ac", "1",
        "-ar", "44100",
        "-vn",
        str(output_path),
    ]
    success, _ = await _run(args)
    return success and output_path.exists() and output_path.stat().st_size > 0


async def make_round_video(
    input_path: Path,
    output_path: Path,
    size: int = ROUND_VIDEO_SIZE,
    max_seconds: int = ROUND_VIDEO_MAX_SECONDS,
) -> bool:
    """
    Kiruvchi videoni Telegram "video note" (dumaloq video) formatiga
    moslaydi: kvadrat kadr, cheklangan davomiylik, H.264/AAC kodlash.
    """
    crop_filter = (
        f"crop='min(iw,ih)':'min(iw,ih)',scale={size}:{size}"
    )
    args = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-t", str(max_seconds),
        "-vf", crop_filter,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        "-pix_fmt", "yuv420p",
        str(output_path),
    ]
    success, _ = await _run(args, timeout=180)
    return success and output_path.exists() and output_path.stat().st_size > 0


async def extract_audio_from_video_for_round(
    input_path: Path,
) -> bool:
    """Video faylda audio trek mavjudligini tekshiradi (round video uchun ixtiyoriy)."""
    args = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=index",
        "-of", "csv=p=0",
        str(input_path),
    ]
    try:
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await asyncio.wait_for(process.communicate(), timeout=30)
        return bool(stdout.decode(errors="ignore").strip())
    except Exception:
        return False
