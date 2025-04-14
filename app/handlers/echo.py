# app/handlers/echo.py
import logging
from aiogram import Router, F
from aiogram.types import Message

logger = logging.getLogger(__name__)
router = Router(name="echo-handler")

# Этот хэндлер будет ловить все сообщения, кроме команд
# F.text проверяет, что сообщение текстовое (можно добавить другие типы)
@router.message(F.text)
async def handle_echo(message: Message):
    """Обработчик для повторения сообщения пользователя."""
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text
    logger.info(f"Received message from {user_name} (ID: {user_id}): {text}")

    try:
        # Пытаемся скопировать сообщение обратно
        await message.send_copy(chat_id=message.chat.id)
        logger.info(f"Sent copy back to {user_name} (ID: {user_id})")
    except TypeError:
        # Если send_copy не сработал (например, для некоторых системных сообщений)
        logger.warning(f"Could not copy message type for user {user_id}. Replying with text.")
        await message.reply("Не могу скопировать этот тип сообщения, но я его получил!")
    except Exception as e:
        logger.error(f"Error sending copy to {user_id}: {e}")
        await message.reply("Ой, что-то пошло не так при отправке копии.")

# Можно добавить хэндлеры для других типов контента, если нужно
# @router.message(F.photo)
# async def handle_photo_echo(message: Message):
#     await message.reply("Классное фото!")

# @router.message(F.sticker)
# async def handle_sticker_echo(message: Message):
#     await message.reply("👍")