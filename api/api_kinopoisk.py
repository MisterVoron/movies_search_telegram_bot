import requests
from config_data.config import API_KEY


url = 'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit='
 

headers = {
    "accept": "application/json",
    "X-API-KEY": API_KEY
}


def movie_search(name: str, genre: str, limit: int):
    return requests.get(url=f'{url}{limit}&query={name} {genre}', headers=headers).json()


def movie_by_rating(rating: str, limit: int):
    return requests.get(url=f'{url}{limit}&rating.imdb={rating}', headers=headers).json()


def low_budget_movie(limit: int):
    return requests.get(url=f'{url}{limit}&budget.value=1000', headers=headers).json()


def high_budget_movie(limit: int):
    return requests.get(url=f'{url}{limit}&budget.value=6666666', headers=headers).json()
