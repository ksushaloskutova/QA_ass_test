import requests
import pdfplumber
from io import BytesIO
import re

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


def parse_course_data(text: str) -> list[dict]:
    """Парсит текст учебного плана в структуру данных.

    Ожидается, что каждая строка текста может содержать название дисциплины,
    упоминание семестра и признак обязательности. Функция извлекает эти данные
    и возвращает их в виде списка словарей.

    Пример возвращаемой структуры::

        [
            {
                "discipline": "Математика",
                "semester": 1,
                "is_mandatory": True,
            },
            ...
        ]

    Поскольку формат исходных PDF может различаться, функция использует
    простейшие эвристики: ищет в строке номер семестра и ключевое слово
    «обязател» для определения обязательности.
    """

    courses = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        sem_match = re.search(r"семестр\s*(\d+)", line, re.IGNORECASE)
        if sem_match:
            name = line[: sem_match.start()].strip(" -–")
            is_mandatory = "обязател" in line.lower()

            try:
                semester = int(sem_match.group(1))
            except ValueError:
                continue

            courses.append(
                {
                    "discipline": name,
                    "semester": semester,
                    "is_mandatory": is_mandatory,
                }
            )

    return courses
