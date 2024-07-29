from aiogram.fsm.state import State, StatesGroup


class FSMSearchScript(StatesGroup):
    name = State()
    genre = State()
    limit = State()


class FSMSearchScriptRating(StatesGroup):
    rating = State()
    limit = State()
    

class FSMSearchScriptLimit(StatesGroup):
    command = State()
    limit = State()
    