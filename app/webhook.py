# app/webhook.py
import logging
from aiohttp import web
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

# Импортируем настроенные экземпляры бота и диспетчера из app.bot
from app.bot import bot, dp
# Импортируем экземпляр настроек
from app.core.config import settings

logger = logging.getLogger(__name__)

def run_webhook():
    """Настраивает и запускает веб-сервер aiohttp для приема вебхуков."""
    logger.info("Initializing aiohttp application...")
    app = web.Application()

    # Создаем обработчик вебхуков Aiogram
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        # secret_token=settings.webhook_secret # Если используется секрет
    )

    # Регистрируем обработчик в приложении aiohttp по пути из конфига
    logger.info(f"Registering webhook handler at path: {settings.telegram_webhook_path}")
    webhook_requests_handler.register(app, path=settings.telegram_webhook_path)

    # Связываем жизненный цикл Aiogram (on_startup, on_shutdown из bot.py)
    # с событиями запуска/остановки aiohttp
    logger.info("Setting up Aiogram lifecycle integration with aiohttp...")
    # Передаем и dp, и bot, так как они могут быть нужны в on_startup/on_shutdown
    setup_application(app, dp, bot=bot)

    # Запускаем веб-сервер
    logger.warning(f"Starting aiohttp web server on http://{settings.webapp_host}:{settings.webapp_port}")
    web.run_app(
        app,
        host=settings.webapp_host,
        port=settings.webapp_port,
        access_log=logging.getLogger("aiohttp.access"), # Используем стандартный логгер
        print=None, # Отключаем стандартный баннер aiohttp
    )