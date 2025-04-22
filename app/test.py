import os
from dotenv import load_dotenv
load_dotenv()
import requests


base_url = "https://api.cloudflare.com/client/v4/zones/0aaf98017c4590413e8480c430c44cc9/settings/ssl"
headers = {
    "X-Auth-Email": os.getenv('CLOUDFLARE_EMAIL'),
    "X-Auth-Key": os.getenv('CLOUDFLARE_API_KEY'),
    "Content-Type": "application/json"
}

params = {
    "value": "full"
}

response = requests.patch(
    url=base_url,
    headers=headers,
    json=params
)

response.raise_for_status()

data = response.json()
print(data)