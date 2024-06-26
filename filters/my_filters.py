from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON_GENRES


class IsGenre(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, str]:
        return {'genre': LEXICON_GENRES[callback.data]} if callback.data in LEXICON_GENRES else False


class IsRating(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.isdigit() or ''.join(map(str.strip, test.split('-'))).replace('.', '').isdigit()
        