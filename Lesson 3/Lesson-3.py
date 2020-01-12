# Домашнее задание
# 1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или
# через аргументы) с сайта superjob.ru и hh.ru. Приложение должно анализировать несколько страниц
# сайта(также вводим через input или аргументы). Получившийся список должен содержать в себе
# минимум:
# *Наименование вакансии
# *Предлагаемую зарплату (отдельно мин. и и отдельно макс.)
# *Ссылку на саму вакансию
# *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение. Данная структура должна
# быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью
# dataFrame через pandas.

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
import json


link_parent = 'https://www.superjob.ru'
link_action = '/vacancy/search/'
link_params = '?keywords='
link_vacancy = input('Введите интересуемую должность: ').replace(' ', '%20')
work = True
main_link = link_parent + link_action + link_params + link_vacancy
vacancies = []

# Запускаем цикл сбора информации с первой по последнюю страницу
while work is True:

    html = requests.get(main_link).text
    parsed_html = bs(html, 'html.parser')

    # Проверка адекватности запроса
    vacancy_adequacy = parsed_html.find('div', {'class': '_3mfro PlM3e _2JVkc _2VHxz _3LJqf'})
    if vacancy_adequacy == None:
        work = True
    elif vacancy_adequacy.getText() == 'По заданным параметрам нет подходящих вакансий':
        print('Выбранная должность никому не нужна')
        break

    vacancies_main_block = parsed_html.find('div', {'class': '_1ID8B'})
    vacancies_list = vacancies_main_block.findAll('div', {'class': 'f-test-vacancy-item'})

# Вытаскиеваем данные по каждой вакансии
    for vacancy in vacancies_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()

# Ищем минимальную и максимальную зарплату
        vacancy_salary = vacancy.find('span', {'class': 'f-test-text-company-item-salary'}).getText().replace(' ₽', '').replace('\xa0', ' ')
        if vacancy_salary == 'По договорённости':
            vacancy_salary_min = 0
            vacancy_salary_max = 'null'
            vacancy_salary = 'null'
        elif vacancy_salary[0:2] == 'от':
            vacancy_salary_min = vacancy_salary.replace(' ', '').replace('от', '')
            vacancy_salary_max = 'null'
            vacancy_salary = 'min'

        elif vacancy_salary[0:2] == 'до':
            vacancy_salary_min = 0
            vacancy_salary_max = vacancy_salary.replace(' ', '').replace('до', '')
            vacancy_salary = 'max'

        else:
            vacancy_salary = vacancy_salary.replace(' 0', '0').split(' ')
            vacancy_salary_min = int(vacancy_salary[0])
            vacancy_salary_max = int(vacancy_salary[-1])
            vacancy_salary = 'min-max'

        vacancy_link = link_parent + vacancy.find('a', {'class': 'icMQ_'})['href']

# Создаём требуемый список
#        vacancy_data['_id'] = vacancy_link
        vacancy_data['name'] = vacancy_name
        vacancy_data['salary_min'] = vacancy_salary_min
        vacancy_data['salary_max'] = vacancy_salary_max
        vacancy_data['link'] = vacancy_link
        vacancy_data['main_link'] = link_parent
        vacancies.append(vacancy_data)

# Проверяем наличие следующей страницы
    next_button = parsed_html.findAll('span', {'class': '_3IDf-'})[-2].getText()
    if next_button == 'Дальше':
        main_link = link_parent + parsed_html.find('a', {'class': 'f-test-link-Dalshe'})['href']
    else:
        work = False

#pprint(pd.DataFrame(vacancies))

# Импортируем в базу данных вакансии
from pymongo import MongoClient
client = MongoClient('mongodb://127.0.0.1:27017')

db = client['vacancies_db']
vdata = db.vacancies_data

# Вставка всех данных в базу
#vdata.insert_many(vacancies)

# Запись и обновление данных с функцией проверки на повторы
def new_vacancy():
    for vacancy in vacancies:
        vdata.update_one({'link': vacancy['link']},
                         {'$set': vacancy},
                         upsert=True)

# Вывод данных по фильтру "минимальная заработная плата выше:" gt_min_salary
def show_gt_min_salary(gt_min_salary):
    objects = vdata.find({'$or': [{'salary_min': {'$gt': gt_min_salary}},
                                  {'salary_max': {'$gt': gt_min_salary}}]})
    for obj in objects:
        pprint(obj)

new_vacancy()
show_gt_min_salary(30000)