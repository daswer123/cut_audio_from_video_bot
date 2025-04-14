# app/handlers/start.py
import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

logger = logging.getLogger(__name__)
router = Router(name="start-handler")

@router.message(CommandStart())
async def handle_start(message: Message):
    """Обработчик команды /start."""
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logger.info(f"User {user_name} (ID: {user_id}) started the bot.")
    await message.answer(
        f"Привет, {hbold(user_name)}!\n\n"
        f"Я бот для извлечения аудио из видео. Просто отправь мне видеофайл, "
        f"и я извлеку из него аудио, сожму до 128kbps и отправлю тебе обратно."
    )