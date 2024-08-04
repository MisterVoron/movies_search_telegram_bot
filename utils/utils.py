from peewee import ModelBase
from database.db import Movie, HistoryMovie


def _convert_list_in_string(lst: list[dict[str, str]]) -> str:
    result = ''
    for item in lst:
        result += item['name'] + ', '
    return result[:-2]


def photo_caption(movie: dict, history: ModelBase) -> str:
    movie_model, _ = Movie.get_or_create(
        name=movie['name'],
        description=movie['description'],
        rating=float(movie['rating']['kp']),
        year=int(movie['year']),
        genres=_convert_list_in_string(movie['genres']),
        age=int(movie['ageRating']),
        poster=movie['poster']['url']
    )
    HistoryMovie.get_or_create(history=history, movie=movie_model)
    
    return str(movie_model)
