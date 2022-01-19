#ДЗ 1
# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.


#Используются два API watchmode.com (сервис поиска фильмов):
# - запрос актера по ID (ID актеров взяты из просмотра кода к странице актера)
# - запрос на фильм по ID (ID наугад)

import requests
import json


api_key = 'YMXnErZp4lPTyJAMzoO9RxUU3Qt2Uwm6s2CaAWoA'

actorID = ['7110004', '49005', '643489', '930405']
for i in actorID:
    url1 = f'https://api.watchmode.com/v1/person/{i}?apiKey={api_key}'
    response_people = requests.get(url1)
    people_data = response_people.json()
    print(f"Информация об актере с ID {i}: имя {people_data.get('full_name')} дата рождения {people_data.get('date_of_birth')}")
    with open("actors_info.json", 'a') as actor_info:
        json.dump(people_data, actor_info, indent=2)

#movie_id = '345534'
movie_id = '171410'
url2 = f'https://api.watchmode.com/v1/title/{movie_id}/details/?apiKey={api_key}'
response_movies = requests.get(url2)
movies_data = response_movies.json()
print(f"Фильм {movies_data.get('title')} снят в {movies_data.get('year')} году.")
with open("movie_info.json", 'a') as movie_info:
    json.dump(movies_data, movie_info, indent=2)

