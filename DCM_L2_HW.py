# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия (можно указать статично для hh - hh.ru, для superjob - superjob.ru)
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

import requests
from bs4 import BeautifulSoup as bS
#from pprint import pprint
import pandas as pd
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
url = 'https://hh.ru'
params = {'items_on_page': '20',
              'text': 'переводчик',
              'page': '0'}

total_pages = 100

vacancies = []

for page in range(0, total_pages+1):
    params['page'] = page

    response = requests.get(url+'/search/vacancy', params=params, headers=headers)
    dom = bS(response.text, 'html.parser')

    vacancies_list = dom.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_redesigned'})

    for vacancy in vacancies_list:
        vacancy_data = {}

        name = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).getText().replace(u'\xa0', u' ')  #название вакансии

        link = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).get('href') #ссылка на вакансию

        try:                                            #зарплата - сначала проверка, что указана
             salary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"}).getText().replace(u'\xa0', u'').replace(u'\u202f', u'')
        except:
             salary = None

        if salary == None:
            min_salary = None
            max_salary = None
            currency = None
        else:
            salary_prep1 = re.sub('–', '', salary)          # исключить прочерки
            salary_prep2 = re.split(r'\s+', salary_prep1)   # разбить по пробелам (всегда будет три позиции в списке: от-число-валюта, до-число-валюта, число-число-валюта)
            if salary_prep2[0] == 'от':
                min_salary = salary_prep2[1]
                max_salary = None
            elif salary_prep2[0] == 'до':
                min_salary = None
                max_salary = salary_prep2[1]
            else:
                min_salary = salary_prep2[0]
                max_salary = salary_prep2[1]

            currency = salary_prep2[2]

        try:                                            # не везде указан работодатель
             employer = vacancy.find('div', {'class': "vacancy-serp-item__meta-info-company"}).getText().replace(u'\xa0', u' ')
        except:
             employer = None

        vacancy_data['name'] = name
        vacancy_data['link'] = link
        vacancy_data['min_salary'] = min_salary
        vacancy_data['max_salary'] = min_salary
        vacancy_data['currency'] = currency
        vacancy_data['employer'] = employer
        vacancy_data['site_name'] = 'hh.ru'

        vacancies.append(vacancy_data)

df = pd.DataFrame(vacancies)
df.to_csv('vacancies.csv', encoding="utf-8-sig")
print (df.shape)
print (df.head())