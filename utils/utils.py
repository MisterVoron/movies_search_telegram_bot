def convert_list_in_string(lst: list[dict[str, str]]) -> str:
    result = ''
    for item in lst:
        result += item['name'] + ', '
    return result[:-2]


def photo_caption(movie: dict) -> str:
    return '<b>{name}</b>\n<i>{description}</i>\nРейтинг: <b>{rate}</b>\
            \nГод: {year}\n{genre}\n<u>{age}+</u>'.format(
            name=movie['name'],
            description=movie['description'],
            rate=movie['rating']['kp'],
            year=movie['year'],
            genre=convert_list_in_string(movie['genres']),
            age=movie['ageRating']
        )