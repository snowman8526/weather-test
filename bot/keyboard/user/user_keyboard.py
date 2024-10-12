from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.db.models import UsersDb


async def user_keyboard(user: UsersDb):

    keyboard = [
        [
            KeyboardButton(text=f'Погода в {user.city}'),
        ],
        [
            KeyboardButton(text='Поменять город'),

        ],
        [
            KeyboardButton(text='/location')
        ]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


