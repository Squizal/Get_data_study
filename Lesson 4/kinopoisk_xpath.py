# from bs4 import BeautifulSoup as bs
# from bs4 import BeautifulStoneSoup
# mai
# from pprint import pprint
# main_link = 'https://www.kinopoisk.ru'
# html = requests.get(main_link+'/afisha/new/city/458/').text
# parsed_html=bs(html,'lxml')
#
#
# films_block = parsed_html.find('div',{'class':'filmsListNew'})
# # films_list = films_block.find_all('div',{'class':'item'})
# films_list = films_block.findChildren(recursive=False)
#
# films = []
# for film in films_list:
#     film_data={}
#     main_info = film.find('div',{'class':'name'}).findChild()
#     film_name = main_info.getText()
#     film_link = main_link + main_info['href']
#     genre = film.findAll('div',{'class':'gray'})[1].getText().replace(' ','')[9:]
#     rating = film.find('span',{'class':['rating_ball_grey','rating_ball_green','rating_ball_red']}).getText()
#     film_data['name'] = film_name
#     film_data['genre'] = genre
#     film_data['link'] = film_link
#     film_data['rating'] = rating
#     films.append(film_data)
#
# pprint(films)

from pprint import pprint
from lxml import html
import requests
main_link = 'https://www.kinopoisk.ru'
response = requests.get(main_link+'/afisha/new/city/1/').text
root = html.fromstring(response)

# films_block = root.xpath("//div[contains(@class,'filmsListNew')]")
films = root.xpath("//div[@class='item']")
print(films)


for film in films:
    name = film.xpath(".//div[@class='name']/a/text()")
    hrefs = film.xpath('.//a[contains (@class,"film-link")]/@href')[0]
    genre = film.xpath('.//div[@class="gray"][last()]/text()')
    rating = film.xpath('.//div[@class="rating"]/span/text()')
    pprint(hrefs)


# name = root.xpath("//div[@class='name']/a/text()")
# hrefs = film.xpath('.//a[contains (@class,"film-link")]/@href')[0]
# print(hrefs)


