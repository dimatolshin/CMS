import os
from dotenv import load_dotenv
load_dotenv()
import requests

base_url = "https://api.cloudflare.com/client/v4/zones"
headers = {
    "X-Auth-Email": os.getenv('CLOUDFLARE_EMAIL'),
    "X-Auth-Key": os.getenv('CLOUDFLARE_API_KEY'),
    "Content-Type": "application/json"
}

params = {
    "name": f"1win-official1.buzz",
}

response = requests.get(
    url=base_url,
    headers=headers,
    params=params
)

response.raise_for_status()  # Проверка на ошибки

data = response.json()
print(data['result'][0]['id'])