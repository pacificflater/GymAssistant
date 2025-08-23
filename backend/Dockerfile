FROM python:3.9-slim

WORKDIR /app

# Установите системные зависимости для сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    gcc \
    make \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем пользователя для безопасности (опционально)
RUN useradd -m -u 1000 fastapi-user && \
    chown -R fastapi-user:fastapi-user /app
USER fastapi-user

EXPOSE 8000

# Команда запуска (может быть переопределена в docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]