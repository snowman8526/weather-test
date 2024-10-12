from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from bot.db.db_commands import update_user, get_city, login_user, get_user, add_user_db
from bot.keyboard.user.user_keyboard import user_keyboard
from bot.loader import bot
from bot.logick.user.weather import get_weather
from bot.state.user.user_state import ReuseCityState, WeatherState

router = Router(name=__name__)


@router.message(Command('weather'))
@router.message(Command('start'))
async def user_start(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user:
        if user.city == None:
            await state.set_state(ReuseCityState.city)
            await message.reply('Назовите свой город', reply_markup=ReplyKeyboardRemove())
        else:
            markup = await user_keyboard(user)
            await message.reply('Показать погоду?', reply_markup=markup)
    else:
        await add_user(message, state)


@router.message(ReuseCityState.city)
async def city(message: Message, state: FSMContext):
    if message.text == '' or message.text == ' ':
        await message.reply('Такого города нет попробуйте ещё раз')
    else:
        city = await get_weather(message.text)
        if city == None:
            await message.reply(f'Города {message.text} нет попробуйте ещё раз')
            user = await get_user(message.from_user.id)
            await login_user(id_user=user.id,
                             command='Смена города',
                             answer=f'Города {message.text} нет попробуйте ещё раз')
        else:
            await update_user(message.from_user.id, city.name)
            await state.clear()
            await message.reply('Город изменён', reply_markup=ReplyKeyboardRemove())
            user = await get_user(message.from_user.id)
            await login_user(id_user=user.id, command='Смена города', answer='Город изменён')
            await print_weather(message, state)


@router.message(WeatherState.weather)
@router.message(F.text.lower().contains('погода в'))
async def print_weather(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user:
        markup = await user_keyboard(user)
        city = await get_city(user.city)
        text = f'Температура в городе {city.name} {city.temp}°C \n'\
                f'Ощущается как {city.perceived_temp}°C\n' \
                f'{city.description_weather}\n'\
                f'Влажность воздуха {city.humidity} %\n'\
                f'Скорость ветра {city.wind_speed} м/с\n'
        await message.reply(text,
                            reply_markup=markup)
        await login_user(id_user=user.id, command=f'погода в {city.name}', answer=text)
    else:
        await any_user(message)

async def add_user(message: Message, state: FSMContext):
    await add_user_db(message.from_user.id)
    await state.set_state(ReuseCityState.city)
    await bot.send_message(message.from_user.id, 'Назовите свой город', reply_markup=ReplyKeyboardRemove())

@router.message()
async def any_user(message: Message, state: FSMContext):
    print('1')
    await bot.send_message(message.from_user.id, 'Вы ввели чтото не правильное попробуйте сначала /weather',
                               reply_markup=ReplyKeyboardRemove())

