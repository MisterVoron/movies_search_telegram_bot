from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons]
    )
    return kb_builder.as_markup()

def create_pagination_keyboard(page: int, limit: int):
    middle_button = f'{page}/{limit}'
    if page == 1:
        return pagination_keyboard(middle_button, 'forward')
    elif 1 < page < limit:
        return pagination_keyboard('backward', middle_button, 'forward')
    else:
        return pagination_keyboard('backward', middle_button)