import requests
from bs4 import BeautifulSoup

def fetch_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ')
        return text.strip()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""
