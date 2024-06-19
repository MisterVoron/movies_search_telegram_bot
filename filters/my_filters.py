from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from lexicon.lexicon import LEXICON_GENRES


class IsGenre(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, str]:
        return {'genre': callback.data} if callback.data in LEXICON_GENRES else False
