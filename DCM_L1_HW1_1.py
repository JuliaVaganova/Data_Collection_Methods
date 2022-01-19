#ДЗ 1
# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint

#Запроc на имя пользователя GitHub (задание проверила на своем - JuliaVaganova)
username = input('Введите имя пользователя GitHub: ')

#из документации к API GitHub для получения списка репозиториев пользователя:
url = f'https://api.github.com/users/{username}/repos'

response = requests.get(url)
j_data = response.json()

#Вывод на экран для проверки
#pprint(type(j_data))

#Сохранение json-вывода в файл .json
with open("user_repos.json", 'a') as user_repos_file:
    #user_repos_file.write(str(j_data))
    json.dump(j_data, user_repos_file, sort_keys=False, indent=4)

#Вывод на экран "очищенного" списка репозиториев
# результат: Список репозитoриев пользователя JuliaVaganova ['project', 'python', 'PythonLibs', 'Python_Lessons',
# 'Repo_GITHUB']):
repo_list = [i['name'] for i in j_data]
print(f"Список репозитoриев пользователя {username} {repo_list}")
