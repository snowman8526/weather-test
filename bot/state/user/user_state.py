from aiogram.fsm.state import StatesGroup, State


class ReuseCityState(StatesGroup):
    city = State()

class WeatherState(StatesGroup):
    weather = State()
