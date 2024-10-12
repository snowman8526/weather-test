import logging
import locale

from loader import dp, bot

from hendlers import router as hendlers_router

locale.setlocale(locale.LC_ALL, '')
logging.basicConfig(level=logging.INFO)


dp.include_router(hendlers_router)

if __name__ == '__main__':
    dp.run_polling(bot)#, skip_updates=True)
