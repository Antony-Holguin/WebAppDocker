import requests
import json

api_key = 'acc_7662f0a8946e193'
api_secret = 'a4fd9dfd9b8e12dcc25bea247246483f'
image_url = 'https://www.havolinedeportivo.com/wp-content/uploads/2022/03/Hinchas-Ecuador.jpeg'
langs = 'en,es'

response = requests.get(
    'https://api.imagga.com/v2/tags?image_url=%s&language=%s' % (
        image_url, langs),
    auth=(api_key, api_secret)
)
data = response.json()

for tag in data["result"]["tags"]:
    print(tag)

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)
