# app/core/config.py
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, HttpUrl, Field
from typing import Optional # Используем Optional для необязательных полей с дефолтом

# Настроим Pydantic на чтение из .env файла
# Файл .env должен лежать рядом с docker-compose.yml
# dotenv_path = find_dotenv() # Можно использовать find_dotenv, если .env не в корне
# load_dotenv(dotenv_path)

class Settings(BaseSettings):
    """
    Основной класс конфигурации, читает переменные из .env файла.
    Префиксы не используются, т.к. имена переменных уже уникальны.
    """
    # Для .env файла
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # --- Telegram Bot API Server ---
    telegram_api_id: int = Field(alias='TELEGRAM_API_ID')
    telegram_api_hash: str = Field(alias='TELEGRAM_API_HASH')
    telegram_local: bool = Field(default=True, alias='TELEGRAM_LOCAL') # Важно для локального API

    # --- Aiogram Bot ---
    telegram_token: SecretStr = Field(alias='TELEGRAM_TOKEN')

    # --- Connection Settings ---
    # URL, по которому бот стучится к API (через Nginx)
    telegram_local_server_url: str = Field(default='http://api', alias='TELEGRAM_LOCAL_SERVER_URL')
    # URL, по которому API стучится к боту (имя сервиса бота)
    telegram_webhook_url: str = Field(default='http://bot', alias='TELEGRAM_WEBHOOK_URL')
    # Путь для вебхука
    telegram_webhook_path: str = Field(default='/webhook', alias='TELEGRAM_WEBHOOK_PATH')

    # --- Bot Web Server (aiohttp) ---
    webapp_host: str = Field(default='0.0.0.0', alias='WEBAPP_HOST')
    webapp_port: int = Field(default=80, alias='WEBAPP_PORT')

    # --- Logging ---
    logging_level: str = Field(default='INFO', alias='LOGGING_LEVEL')
    logging_format: str = Field(default="[%(asctime)s] %(levelname)-8s [%(name)s] %(message)s", alias='LOGGING_FORMAT')
    logging_datefmt: str = Field(default="%Y-%m-%d %H:%M:%S", alias='LOGGING_DATEFMT')

    # --- Computed Properties ---
    @property
    def telegram_webhook_full_url(self) -> str:
        """Собирает полный URL для установки вебхука."""
        return f"{self.telegram_webhook_url.rstrip('/')}{self.telegram_webhook_path}"

    @property
    def telegram_api_server(self):
        """Создает объект сервера API для Aiogram."""
        from aiogram.client.telegram import TelegramAPIServer
        return TelegramAPIServer.from_base(self.telegram_local_server_url, is_local=self.telegram_local)

# Создаем единственный экземпляр конфига, который будем импортировать везде
try:
    settings = Settings()
except Exception as e:
    logging.basicConfig(level="INFO") # Базовый логгер, если конфиг не прочитался
    logging.critical(f"CRITICAL ERROR: Could not load settings! Error: {e}", exc_info=True)
    logging.critical("Please check your .env file and environment variables.")
    exit(1) # Завершаем работу, если конфиг не загружен

# Можно добавить проверку обязательных полей тут, если нужно
if not settings.telegram_token.get_secret_value() or \
   not settings.telegram_api_id or \
   not settings.telegram_api_hash:
    logging.basicConfig(level="INFO")
    logging.critical("CRITICAL ERROR: TELEGRAM_TOKEN, TELEGRAM_API_ID, and TELEGRAM_API_HASH must be set in .env!")
    exit(1)