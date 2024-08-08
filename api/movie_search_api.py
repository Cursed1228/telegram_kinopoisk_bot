from config_data.config import RAPID_API_KEY, BASE_URL
import requests
import json


def search_by_name(name, limit=10):
    url = f'{BASE_URL}movie/search?page=1&limit={limit}&query={name}'

    headers = {
        "accept": "application/json",
        "X-API-KEY": RAPID_API_KEY
    }

    response = requests.get(url, headers=headers)
    result = json.loads(response.text)

    return result






