from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON
from states.states import FSMSearchScript
from filters.my_filters import IsGenre
from keyboards.kb_genres import genres_kb
from api.api_kinopoisk import movie_search
from database.db import users


router = Router()


@router.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(
        text=LEXICON['/start']
    )


@router.message(Command(commands='help'))
async def process_command_help(message: Message):
    await message.answer(
        text=LEXICON['/help']
    )


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_command_cancel(message: Message):
    await message.answer(
        text=LEXICON['/cancel']
    )


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_command_cancel_in_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=LEXICON['/cancel_in_state']
    )
    

@router.message(Command(commands='movie_search'), StateFilter(default_state))    
async def process_command_movie_search(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON['movie_search']
    )
    await state.set_state(FSMSearchScript.name)


@router.message(StateFilter(FSMSearchScript.name), F.text)
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text=LEXICON['script_answer_1'],
        reply_markup=genres_kb()
    )
    await state.set_state(FSMSearchScript.genre)


@router.message(StateFilter(FSMSearchScript.name))
async def warning_not_name(message: Message):
    await message.answer(
        text=LEXICON['warning_name']
    )


@router.callback_query(StateFilter(FSMSearchScript.genre), IsGenre())
async def process_genre_sent(callback: CallbackQuery, state: FSMContext, genre: str):
    await state.update_data(genre=genre)
    await callback.message.delete()
    await callback.message.answer(
        text=LEXICON['script_answer_2']
    )
    await state.set_state(FSMSearchScript.limit)


@router.message(StateFilter(FSMSearchScript.genre))
async def warning_not_genre(message: Message):
    await message.answer(
        text=LEXICON['warning_genre']
    )


@router.message(StateFilter(FSMSearchScript.limit), F.text.isdigit())
async def process_limit_sent(message: Message, state: FSMContext):
    await state.update_data(limit=int(message.text))
    users[message.from_user.id] = await state.get_data()
    await message.answer(
        text=movie_search(name=users[message.from_user.id]['name'],
                          genre=users[message.from_user.id]['genre'],
                          limit=users[message.from_user.id]['limit'])
    )







        