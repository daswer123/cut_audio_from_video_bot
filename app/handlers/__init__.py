# app/handlers/__init__.py
from aiogram import Router
from . import start, echo, video

# Главный роутер для всех хэндлеров
main_handlers_router = Router(name="main-handlers")

# Включаем роутеры из других модулей
main_handlers_router.include_router(start.router)
main_handlers_router.include_router(video.router)  # Добавляем обработчик видео
# main_handlers_router.include_router(echo.router)  # Echo должен быть последним, так как он самый общий

# Экспортируем главный роутер
__all__ = ["main_handlers_router"]