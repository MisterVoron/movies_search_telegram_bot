from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON


router = Router()


@router.message()
async def process_other_message(message: Message):
    await message.answer(
        text=LEXICON['other_message']
    )
