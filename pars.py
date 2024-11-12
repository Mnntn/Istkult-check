import xml.etree.ElementTree as ET
import requests

# Скачивание и парсинг sitemap.xml по URL
sitemap_url = 'https://istkult.ru/sitemap.xml'
try:
    response = requests.get(sitemap_url)
    response.raise_for_status()  # Проверка успешности запроса
    root = ET.fromstring(response.content)  # Парсим XML из содержимого ответа
except requests.RequestException as e:
    print(f"Ошибка при загрузке sitemap: {e}")
    exit()

# Пространство имен для XML
namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Ключевые слова для поиска (без учета регистра)
keywords = ["ytong", "xella", "ютонг"]

# Функция для проверки содержимого страницы
def check_keywords_in_page(url, keywords):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text.lower()
            return any(keyword in content for keyword in keywords)
    except requests.RequestException as e:
        print(f"Ошибка при запросе страницы {url}: {e}")
    return False

# Поиск страниц, содержащих ключевые слова
matching_urls = []

for url in root.findall(".//ns:loc", namespaces=namespaces):
    page_url = url.text
    if check_keywords_in_page(page_url, keywords):
        matching_urls.append(page_url)

# Вывод найденных URL
print("Страницы, содержащие ключевые слова:")
for url in matching_urls:
    print(url)

