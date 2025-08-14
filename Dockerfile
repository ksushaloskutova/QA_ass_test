FROM python:3.10-slim

# Обновим pip
RUN pip install --upgrade pip

# Установим системные зависимости
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем файлы
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install langchain-community
RUN pip install langchain-huggingface

COPY app/ .
COPY .env .

# Установим переменные окружения
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}

CMD ["python", "-m", "main"]
