from pprint import pprint
from lxml import html
import requests

def request_to_yandex():
    str = 'Автомобиль'
    try:
        response = requests.get('https://yandex.ru/search/',
                                params={'text':str})
        root = html.fromstring(response.text)

        result_list = root.xpath("//a[contains(@class,'organic__url')]/@href")
        if result_list:
            for item in result_list:
                pprint(item)
        else:
            print('По вашему заросу ничего не найдено')
    except Exception as e:
        print(e)

request_to_yandex()
