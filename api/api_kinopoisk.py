import requests
from config_data.config import API_KEY


url = 'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit={}&query={} {}'
headers = {
    "accept": "application/json",
    "X-API-KEY": API_KEY
}


def movie_search(name: str, genre: str, limit: int):
    return requests.get(url=url.format(limit, name, genre), headers=headers).json()


def movie_by_rating():
    pass


def low_budget_movie():
    pass


def low_budget_movie():
    pass


def high_budget_movie():
    pass


def history():
    pass
