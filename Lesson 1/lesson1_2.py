import requests
import json
import pprint

# Передача ключа через заголовок
headers = {'Authorization':'aa38a129-d651-484e-b46a-a7e83f248b5b'}

# Прямая передача ключа
# my_apikey = 'aa38a129-d651-484e-b46a-a7e83f248b5b'

main_link = 'https://api.rasp.yandex.net/v3.0/search/'
start_city = 'c20674'
end_city = 'c213'

link = f'{main_link}?from={start_city}&to={end_city}'

response = requests.get(link)

if response.ok:
    time.sleep(1)
    data = json.loads(response.text)
#    pprint(data)
    for stations in data:
        print(f"Номера марщрутов из пункта назначения:")
        print("- " + str(stations['number']))
