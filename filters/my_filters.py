from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


genres: list[str] = ['action', 'drama', 'comedy', 'mystery', 'melodrama', 'fantasy',
                     'biography', 'humor', 'horror', 'adventure', 'science fiction', 
                     'history', 'thriller', 'western', 'romance', 'anime']


class IsGenre(BaseFilter):
    def __init__(self):
         self.genres = genres
    
    def __call__(self, message: CallbackQuery) -> bool | dict[str, str]:
        return {genre: message.data} if message.data in genres else True
