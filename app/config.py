import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

AI_PROGRAM_URL = "https://abit.itmo.ru/program/master/ai"
AI_PRODUCT_PROGRAM_URL = "https://abit.itmo.ru/program/master/ai_product"

# PDF-файлы учебных планов по программам
PDF_URLS = {
    "ai": "https://api.itmo.su/constructor-ep/api/v1/static/programs/10033/plan/abit/pdf",  # AI
    "ai_product": "https://api.itmo.su/constructor-ep/api/v1/static/programs/10130/plan/abit/pdf",  # AI Product
}

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
