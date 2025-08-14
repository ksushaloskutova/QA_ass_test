import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

AI_PROGRAM_URL = "https://abit.itmo.ru/program/master/ai"
AI_PRODUCT_PROGRAM_URL = "https://abit.itmo.ru/program/master/ai_product"
PDF_URLS = [
    "https://api.itmo.su/constructor-ep/api/v1/static/programs/10033/plan/abit/pdf",       # AI
    "https://api.itmo.su/constructor-ep/api/v1/static/programs/10130/plan/abit/pdf",       # AI Product
]

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
