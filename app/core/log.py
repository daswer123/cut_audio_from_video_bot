# app/core/log.py
import logging
from .config import settings # Импортируем готовый экземпляр конфига

def setup_logging():
    """Настраивает базовую конфигурацию логирования."""
    logging.basicConfig(
        level=settings.logging_level.upper(), # Убедимся, что уровень в верхнем регистре
        format=settings.logging_format,
        datefmt=settings.logging_datefmt,
    )
    # Настроим логгер aiohttp немного тише, чтобы не спамил DEBUG сообщениями
    logging.getLogger('aiohttp.access').setLevel(logging.WARNING)
    logging.getLogger('aiohttp.client').setLevel(logging.WARNING)
    logging.getLogger('aiohttp.internal').setLevel(logging.WARNING)
    logging.getLogger('aiohttp.server').setLevel(logging.WARNING)
    logging.getLogger('aiohttp.web').setLevel(logging.WARNING)

    # Логгер Aiogram тоже можно настроить
    logging.getLogger('aiogram').setLevel(settings.logging_level.upper())