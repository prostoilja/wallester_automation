# Использование официального образа Playwright от Microsoft
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Сначала копируем зависимости для кэширования слоев
COPY requirements.txt .

# Установка зависимостей и браузера Chromium
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install --with-deps chromium

# Копируем остальные файлы проекта
COPY . .

# Установка переменной окружения, чтобы Python видел модули в /app
ENV PYTHONPATH=/app

# Команда для запуска тестов при старте контейнера
CMD ["pytest", "tests/test_api_auth.py", "-v"]