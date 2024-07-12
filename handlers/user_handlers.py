from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON
from states.states import FSMSearchScript, FSMSearchScriptRating
from filters.my_filters import IsGenre, IsRating
from keyboards.kb_genres import genres_kb
from keyboards.pagination_kb import create_pagination_keyboard
from api.api_kinopoisk import movie_search, movie_by_rating
from database.db import users, User, History, Search, Movie
from utils.utils import photo_caption
from peewee import IntegrityError
from datetime import date


router = Router()


@router.message(CommandStart())
async def process_command_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name


    try:
        User.create(user_id=message.from_user.id, name=message.from_user.first_name)
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
    storage = await state.get_data()
    user = User.get(User.user_id == message.from_user.id)
    user.position = 1
    user.save()
    history, _ = History.get_or_create(user=user, date=date.today())
    search, _ = Search.get_or_create(history=history, name=storage['name'], genre=storage['genre'], limit=int(storage['limit']))
    await state.clear()
    info = movie_search(name=storage['name'],
                        genre=storage['genre'],
                        limit=storage['limit'])
    movie = info['docs'][0]
    caption = photo_caption(search=search, movie=movie)
    if storage['limit'] == 1:
        await bot.send_photo(message.chat.id, movie['poster']['url'], caption=caption, parse_mode='HTML')
    else:
        for movie in info['docs']:
            photo_caption(search=search, movie=movie)
        await bot.send_photo(message.chat.id, movie['poster']['url'],
                             caption=caption, parse_mode='HTML',
                             reply_markup=create_pagination_keyboard(
                                page=user.position,
                                limit=(Search.select().join(History).join(User)
                                .where(User.user_id == message.from_user.id)
                                .order_by(Search.id.desc()).get().limit)
                             ))


@router.message(StateFilter(FSMSearchScript.limit))
async def warning_not_genre(message: Message):
    await message.answer(
        text=LEXICON['warning_limit']
    )


@router.callback_query(F.data.in_({'backward', 'forward'}))
async def process_backward_forward_press(callback: CallbackQuery, bot: Bot):
    if callback.data == 'backward':
        user = User.get(User.user_id == callback.from_user.id)
        user.position -= 1
        user.save()
    else:
        user = User.get(User.user_id == callback.from_user.id)
        user.position += 1
        user.save()
    position = User.get(User.user_id == callback.from_user.id).position
    caption = Movie.get(Movie.id == position)
    await bot.send_photo(callback.message.chat.id, str(caption.poster),
                             caption=str(caption), parse_mode='HTML',
                             reply_markup=create_pagination_keyboard(
                                page=position,
                                limit=(Search.select().join(History).join(User)
                                .where(User.user_id == callback.from_user.id)
                                .order_by(Search.id.desc()).get().limit)
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
    user_id = message.from_user.id
    users[user_id] = await state.get_data()
    await state.clear()
    info = movie_by_rating(rating=users[user_id]['rating'],
                        limit=users[user_id]['limit'])
    movie = info['docs'][0]
    if users[user_id]['limit'] == 1:
        caption = photo_caption(movie)
        await bot.send_photo(message.chat.id, movie['poster']['url'], caption=caption, parse_mode='HTML')
    else:
        users[user_id]['position'] = 0
        users[user_id]['movies'] = info['docs']
        caption = photo_caption(movie)
        await bot.send_photo(message.chat.id, movie['poster']['url'],
                             caption=caption, parse_mode='HTML',
                             reply_markup=create_pagination_keyboard(
                                page=users[message.from_user.id]['position'],
                                limit=users[message.from_user.id]['limit']
                             ))



        