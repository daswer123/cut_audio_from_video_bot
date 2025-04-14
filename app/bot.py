# app/bot.py
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

# Импортируем наш единый экземпляр настроек
from app.core.config import settings
from app.handlers import main_handlers_router # Импортируем главный роутер

logger = logging.getLogger(__name__)

# 1. Создаем сессию с использованием настроек из конфига
session = AiohttpSession(api=settings.telegram_api_server)

# 2. Создаем экземпляр бота
bot = Bot(
    token=settings.telegram_token.get_secret_value(),
    session=session,
)

# 3. Создаем диспетчер
dp = Dispatcher()

# 4. Определяем асинхронные функции для старта и остановки
async def on_startup(dispatcher: Dispatcher):
    """Действия при старте бота: установка вебхука."""
    logger.warning("Bot starting...")
    logger.info(f"Bot uses API Server: {bot.session.api.base}")
    logger.info(f"Attempting to set webhook to: {settings.telegram_webhook_full_url}")

    try:
        # Сначала удаляем старый вебхук, если он был
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Previous webhook deleted successfully.")

        # Устанавливаем новый вебхук
        webhook_set = await bot.set_webhook(
            url=settings.telegram_webhook_full_url,
            allowed_updates=dispatcher.resolve_used_update_types(), # Только нужные апдейты
            # secret_token=settings.webhook_secret # Если используете секрет
            drop_pending_updates=True # Пропустить старые апдейты
        )

        if webhook_set:
            bot_info = await bot.get_me()
            logger.warning(f"Webhook set successfully for bot @{bot_info.username} (ID: {bot_info.id})")
            logger.info(f"Listening for webhooks at: {settings.telegram_webhook_full_url}")
        else:
            logger.error("Failed to set webhook! Check API server and network.")

    except Exception as e:
        # Ловим и логгируем любые ошибки при установке вебхука
        logger.critical(f"CRITICAL ERROR during webhook setup: {e}", exc_info=True)
        # Возможно, стоит остановить приложение, если вебхук не установился
        # raise

async def on_shutdown():
    """Действия при остановке бота: закрытие сессии."""
    logger.warning("Bot shutting down...")
    # Закрываем сессию бота
    await bot.session.close()
    # Можно удалить вебхук при штатной остановке
    # logger.info("Deleting webhook...")
    # await bot_instance.delete_webhook()
    logger.warning("Bot session closed.")

# 5. Регистрируем роутеры и обработчики жизненного цикла
dp.include_router(main_handlers_router) # Включаем все наши хэндлеры
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

# Экземпляры bot и dp будут импортированы в webhook.py