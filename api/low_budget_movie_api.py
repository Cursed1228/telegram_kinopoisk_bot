from config_data.config import RAPID_API_KEY, BASE_URL
import requests
import json


def low_budget_movie(limit=10, genre=None):
    if genre:
        url = f'{BASE_URL}movie?page=1&limit={limit}&&budget.value=0-150000&genres.name={genre.lower()}'
    else:
        url = f'{BASE_URL}movie?page=1&limit={limit}&&budget.value=0-150000'

    headers = {
        "accept": "application/json",
        "X-API-KEY": RAPID_API_KEY
    }

    response = requests.get(url, headers=headers)
    result = json.loads(response.text)

    return result
