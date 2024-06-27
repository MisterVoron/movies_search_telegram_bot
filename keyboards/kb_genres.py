from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_GENRES


def genres_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for button, text in LEXICON_GENRES.items():
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button
        ))
    
    kb_builder.row(*buttons, width=3)

    return kb_builder.as_markup()
