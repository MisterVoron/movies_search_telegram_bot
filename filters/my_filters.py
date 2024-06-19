from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from lexicon.lexicon import LEXICON_GENRES


class IsGenre(BaseFilter):
    def __init__(self):
         self.genres = LEXICON_GENRES
    
    def __call__(self, message: CallbackQuery) -> bool | dict[str, str]:
        return {genre: message.data} if message.data in self.genres else False
