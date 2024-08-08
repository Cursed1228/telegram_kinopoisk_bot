from config_data.config import RAPID_API_KEY, BASE_URL
import requests
import json


def check_genre(text):
    url = "https://api.kinopoisk.dev/v1/movie/possible-values-by-field?field=genres.name"

    headers = {
        "accept": "application/json",
        "X-API-KEY": RAPID_API_KEY
    }

    response = requests.get(url, headers=headers)
    genre_dict = json.loads(response.text)

    for genre in genre_dict:
        if genre['name'] == text or genre['slug'] == text:
            return True

    return False


def create_genres_txt():
    url = "https://api.kinopoisk.dev/v1/movie/possible-values-by-field?field=genres.name"

    headers = {
        "accept": "application/json",
        "X-API-KEY": RAPID_API_KEY
    }

    response = requests.get(url, headers=headers)
    genres_list = response.json()

    genres_names = ", ".join([genre["name"] for genre in genres_list])
    return genres_names

