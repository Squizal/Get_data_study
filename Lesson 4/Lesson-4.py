from pymongo import MongoClient
from pprint import pprint
from lxml import html
from datetime import datetime, timedelta
import requests

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['newsdb']
ndata = db.newsdb


def get_html(url):  # Запрос по адресу
    main_link = url
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    header = {'User-Agent': user_agent}
    response = requests.get(main_link, headers=header).text
    return(html.fromstring(response))


def insert_new(data):  # Вставка новых данных с проверкой на повторы
    for news in data:
        ndata.update_one({'link': news['link']},
                         {'$set': news},
                         upsert=True)


def mailru_news():
    main_link = 'https://mail.ru'
    news_site = get_html(main_link)

    news_all = news_site.xpath("//div[@class='news-item__inner']")
    news_data = []

    for news in news_all:
        news_export = {}
        title = news.xpath("./a[last()]/text()")
        hrefs = news.xpath("./a[last()]/@href")
        hrefs = hrefs[0].split('?')[0]
        inside_news = get_html(hrefs)
        news_date = inside_news.xpath('//span[@datetime]/@datetime')
        news_export['source'] = main_link
        news_export['title'] = title[0].replace(u'\xa0', u' ')
        news_export['link'] = hrefs
        news_export['date'] = datetime.strptime(news_date[0], '%Y-%m-%dT%H:%M:%S%z')
        news_data.append(news_export)
    return(news_data)


def lenta_ru():
    main_link = 'http://m.lenta.ru'
    news_site = get_html(main_link)

    news_all = news_site.xpath("//div[@class='main-page__top']//li")
    news_data = []

    for news in news_all:
        news_export = {}
        title = news.xpath(".//div[@class='card-mini__title']/text()")
        hrefs = news.xpath(".//a/@href")
        hrefs = main_link + hrefs[0]
        inside_news = get_html(hrefs)
        news_date = inside_news.xpath("//time[@class='common-head__info-text']/text()")
        news_export['source'] = main_link
        news_export['title'] = title[0].replace(u'\xa0', u' ')
        news_export['link'] = hrefs
        news_export['date'] = news_date[0]
        news_data.append(news_export)
    return(news_data)


insert_new(mailru_news())
insert_new(lenta_ru())

pprint(mailru_news())
pprint(lenta_ru())






