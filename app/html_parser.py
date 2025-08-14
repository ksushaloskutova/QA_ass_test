import requests
import pdfplumber
from io import BytesIO

def fetch_pdf_text(url: str) -> str:
    print(f"📄 Загружаю PDF с {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()

        with pdfplumber.open(BytesIO(response.content)) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'

        print(f"✅ PDF загружен. Длина текста: {len(text)} символов.")
        return text.strip()

    except Exception as e:
        print(f"❌ Ошибка загрузки PDF: {e}")
        return ''
