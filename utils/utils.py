from peewee import ModelBase
from database.db import Movie


def _convert_list_in_string(lst: list[dict[str, str]]) -> str:
    result = ''
    for item in lst:
        result += item['name'] + ', '
    return result[:-2]


def photo_caption(movie: dict, search: ModelBase) -> str:
    movie_model = Movie.create(
        search=search,
        name=movie['name'],
        description=movie['description'],
        rating=float(movie['rating']['kp']),
        year=int(movie['year']),
        genres=_convert_list_in_string(movie['genres']),
        age=int(movie['ageRating']),
        poster=movie['poster']['url']
    )
    
    return str(movie_model)
