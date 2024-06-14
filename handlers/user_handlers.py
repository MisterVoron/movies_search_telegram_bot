from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from lexicon.lexicon import LEXICON
from states.states import FSMSearchScript


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
        text=LEXICON['script_answer_1']
    )
    await state.set_state(FSMSearchScript.genre)


@router.message(StateFilter(FSMSearchScript.name))
async def warning_not_name(message: Message):
    await message.answer(
        text=LEXICON['warning_name']
    )
















        