# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД
# Минимум один сайт, максимум - все три

from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)

db = client['lenta_news']
lenta_news = db.lenta_news
lenta_news.drop()

url = 'https://lenta.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

source = "lenta.ru"

fishing = []

items = dom.xpath('//a[contains(@class, "topnews")]')

for item in items:
    fish = {}
    title = item.xpath('.//*[contains(@class, "card-mini__title") or contains(@class, "card-big__title")]/text()')
    link = item.xpath('.//div[contains(@class, "_text") or contains(@class,"card-big__image-wrap")]/../@href')
    # date = ''.join(link)[6:16]
    date = item.xpath('.//time[contains(@class, "_date")]/text()')

    fish['title'] = ' '.join(title)
    fish['link'] = 'https://lenta.ru'+''.join(link)
    fish['date'] = date
    fish['source'] = source

    fishing.append(fish)

    try:
        lenta_news.insert_one(fish)
    except:
        pass

pprint(fishing)

