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

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libfontconfig1 \
    libxss1 \
    libasound2 \
    libxtst6 \
    fonts-liberation \
    libappindicator3-1 \
    libxrandr2 \
    libxdamage1 \
    xdg-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY app/ .
COPY .env .

# Установим переменные окружения
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}

CMD ["python", "-m", "main"]
