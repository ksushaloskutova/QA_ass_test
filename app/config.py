import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

HTML_URLS = [
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://ru.wikipedia.org/wiki/Python"
]

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
