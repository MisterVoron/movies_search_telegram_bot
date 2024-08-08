from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON
from states.states import FSMSearchScript, FSMSearchScriptRating, FSMSearchScriptLimit
from filters.my_filters import IsGenre, IsRating
from keyboards.kb_genres import genres_kb
from keyboards.pagination_kb import create_pagination_keyboard
from api.api_kinopoisk import movie_search, movie_by_rating, low_budget_movie, high_budget_movie
from database.db import User, History, Movie, HistoryMovie
from utils.utils import photo_caption
from peewee import IntegrityError
from datetime import datetime


router = Router()


@router.message(CommandStart())
async def process_command_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name


    try:
        User.create(user_id=user_id, name=user_name)
        await message.answer(
            text=LEXICON['/start']
        )
    except IntegrityError:
        await message.answer(
            text=LEXICON['again_/start'].format(user_name)
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
    

@router.message(Command(commands='history'))
async def process_command_history(message: Message):
    result = ''
    for history in History.select():
        result += f'{history.date.strftime('%d.%m.%Y %H:%M:%S')} {history.command}\n'
    await message.answer(
        text=result
    )
    

@router.message(Command(commands='movie_search'), StateFilter(default_state))    
async def process_command_movie_search(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON['/movie_search']
    )
    await state.set_state(FSMSearchScript.name)


@router.message(StateFilter(FSMSearchScript.name), F.text)
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text=LEXICON['genres'],
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
        text=LEXICON['limit']
    )
    await state.set_state(FSMSearchScript.limit)


@router.message(StateFilter(FSMSearchScript.genre))
async def warning_not_genre(message: Message):
    await message.answer(
        text=LEXICON['warning_genre']
    )


@router.message(StateFilter(FSMSearchScript.limit), F.text.isdigit())
async def process_limit_sent(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(limit=int(message.text))
    user_id = message.from_user.id
    storage = await state.get_data()
    await state.clear()
    user = User.get(User.user_id == user_id)
    user.pg_position = 0
    user.save()
    history, _ = History.get_or_create(user=user, date=datetime.today(), command='/movie_search')
    history.limit = storage['limit']
    history.save()
    info = movie_search(name=storage['name'],
                        genre=storage['genre'],
                        limit=storage['limit'])

    movie = info['docs'][0]
    caption = photo_caption(movie=movie, history=history)
    if storage['limit'] == 1:
        await bot.send_photo(user_id, movie['poster']['url'], caption=caption, parse_mode='HTML')
    else:
        for film in info['docs']:
            photo_caption(movie=film, history=history)
        await bot.send_photo(user_id, movie['poster']['url'],
                             caption=caption, parse_mode='HTML',
                             reply_markup=create_pagination_keyboard(
                                page=user.pg_position + 1,
                                limit=storage['limit']
                             ))


@router.message(StateFilter(FSMSearchScript.limit))
async def warning_not_limit(message: Message):
    await message.answer(
        text=LEXICON['warning_limit']
    )


@router.callback_query(F.data.in_({'backward', 'forward'}))
async def process_backward_forward_press(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    user = User.get(User.user_id == user_id)
    limit = History.select().order_by(History.id.desc()).limit(1).get().limit
    if callback.data == 'backward':
        user.pg_position -= 1
    else:
        user.pg_position += 1
    
    user.save()
    position = user.pg_position
    sub_query_date = History.select().order_by(History.id.desc()).limit(1).get().date
    movies = list(Movie.select().join(HistoryMovie).join(History).where(History.date == sub_query_date))

    await bot.send_photo(user_id, str(movies[position].poster),
                             caption=str(movies[position]), parse_mode='HTML',
                             reply_markup=create_pagination_keyboard(
                                page=position + 1,
                                limit=limit
                             ))
    await callback.answer()


@router.message(Command(commands='movie_by_rating'), StateFilter(default_state))
async def process_movie_by_rating_command(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON['/movie_by_rating']
    )
    await state.set_state(FSMSearchScriptRating.rating)
    

@router.message(StateFilter(FSMSearchScriptRating.rating), IsRating())
async def process_rating_sent(message: Message, state: FSMContext):
    await state.update_data(rating=message.text)
    await message.answer(
        text=LEXICON['limit']
    )
    await state.set_state(FSMSearchScriptRating.limit)


@router.message(StateFilter(FSMSearchScriptRating.rating))
async def warning_not_rating(message: Message):
    await message.answer(
        text=LEXICON['warning_rating']
    )


@router.message(StateFilter(FSMSearchScriptRating.limit), F.text.isdigit())
async def process_limit_sent(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(limit=int(message.text))
    storage = await state.get_data()
    await state.clear()
    user_id = message.from_user.id
    limit = storage['limit']
    info = movie_by_rating(rating=storage['rating'], limit=limit)
    user = User.get(User.user_id == user_id)
    user.pg_position = 0
    user.save()
    history, _ = History.get_or_create(user=user, date=datetime.today(), command='/movie_by_rating', limit=limit)
    movie = info['docs'][0]
    caption = photo_caption(movie=movie, history=history)
    if storage['limit'] == 1:
        await bot.send_photo(user_id, movie['poster']['url'], caption=caption, parse_mode='HTML')
    else:
        for film in info['docs']:
            photo_caption(movie=film, history=history)
        await bot.send_photo(user_id, movie['poster']['url'],
                             caption=caption, parse_mode='HTML',
                             reply_markup=create_pagination_keyboard(
                                page=user.pg_position + 1,
                                limit=limit
                             ))


@router.message(StateFilter(FSMSearchScriptRating.limit))
async def warning_not_limit(message: Message):
    await message.answer(
        text=LEXICON['warning_limit']
    )


@router.message(Command(commands=['low_budget_movie', 'high_budget_movie']), StateFilter(default_state))
async def process_low_budget_movie_command(message: Message, state: FSMContext):
    await state.update_data(command=message.text)
    await message.answer(
        text=LEXICON['limit']
    )
    await state.set_state(FSMSearchScriptLimit.limit)

    
@router.message(StateFilter(FSMSearchScriptLimit.limit), F.text.isdigit())
async def process_limit_sent(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(limit=int(message.text))
    storage = await state.get_data()
    await state.clear()
    user_id = message.from_user.id
    limit = storage['limit']

    if storage['command'] == 'low_budget_movie':
        info = low_budget_movie(limit=limit)
        command = '/low_budget_movie'
    else:
        info = high_budget_movie(limit=limit)
        command = '/high_budget_movie'

    user = User.get(User.user_id == user_id)
    user.pg_position = 0
    user.save()
    history, _ = History.get_or_create(user=user, date=datetime.today(), command=command, limit=limit)
    movie = info['docs'][0]
    caption = photo_caption(movie=movie, history=history)
    if storage['limit'] == 1:  
        await bot.send_photo(user_id, movie['poster']['url'], caption=caption, parse_mode='HTML')
    else:
        for film in info['docs']:
            photo_caption(movie=film, history=history)
        await bot.send_photo(user_id, movie['poster']['url'],
                             caption=caption, parse_mode='HTML',
                             reply_markup=create_pagination_keyboard(
                                page=user.pg_position + 1,
                                limit=limit
                             ))


@router.message(StateFilter(FSMSearchScriptLimit.limit))
async def warning_not_limit(message: Message):
    await message.answer(
        text=LEXICON['warning_limit']
    )
