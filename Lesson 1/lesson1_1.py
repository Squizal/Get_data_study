from pprint import pprint
import requests
import json

git_user = input("Введите имя пользователя на github: ")
git_link = "https://api.github.com/users/" + git_user + "/repos"

response = requests.get(git_link)

if response.ok:
    data = json.loads(response.text)
#    pprint(data)
    print(f"Публичные репозитории пользователя {git_user}:")
    for user_repos in data:
        print("- " + str(user_repos['name']))