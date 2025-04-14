# app/__main__.py
import logging
# Сначала настраиваем логирование
from app.core.log import setup_logging
setup_logging()

# Теперь импортируем остальное, чтобы логи уже работали
from app.webhook import run_webhook

# Получаем логгер для этого модуля *после* настройки
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Application starting...")
    try:
        run_webhook() # Запускаем веб-сервер с вебхуком
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Application stopped by user (KeyboardInterrupt/SystemExit).")
    except Exception as e:
        # Ловим вообще все необработанные исключения на верхнем уровне
        logger.critical(f"Unhandled critical exception during runtime: {e}", exc_info=True)
    finally:
        logger.info("Application finished.")