# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Устанавливаем системные зависимости:
# build-essential - для сборки C-расширений (uvloop, ujson)
# curl, netcat-openbsd - для healthcheck и отладки сети внутри контейнера
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    netcat-openbsd \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости Python
# Используем --no-cache-dir для уменьшения размера слоя
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY ./app ./app

# Указываем команду для запуска приложения
# Запускаем основной модуль app, который вызовет webhook.py -> run_webhook()
CMD ["python3", "-m", "app"]