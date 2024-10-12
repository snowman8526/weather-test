from typing import List

from click import command

from .models import UsersDb, session, City, LogUser
from datetime import datetime as dt


async def get_user(id_telegram: int):
    return session.query(UsersDb).filter(UsersDb.id_telegram == id_telegram).first()

async def add_user_db(id_telegram: int):
    new_user = UsersDb(id_telegram=id_telegram)
    session.add(new_user)
    session.commit()


async def add_city(city: str,
                   id_city: int,
                   temp: int,
                   humidity: int,
                   wind_speed: int,
                   perceived_temp: int,
                   description_weather: str,
                   date: dt):
    new_city = City(name=city,
                    id_city=id_city,
                    temp=temp,
                    humidity=humidity,
                    wind_speed=wind_speed,
                    perceived_temp=perceived_temp,
                    description_weather=description_weather,
                    date=date)
    session.add(new_city)
    session.commit()

async def get_city(city: str) -> City:
    return session.query(City).filter(City.name == city).first()

async def update_city(city: str,
                   temp: int,
                   humidity: int,
                   wind_speed: int,
                   perceived_temp: int,
                   description_weather: str):
    session.query(City).filter(City.name == city).update(temp=temp,
                                                         humidity=humidity,
                                                         wind_speed=wind_speed,
                                                         perceived_temp=perceived_temp,
                                                         description_weather=description_weather)
    session.commit()

async def update_user(id_telegram: int, city: str):
    session.query(UsersDb).filter(UsersDb.id_telegram == id_telegram).update({'city':city})
    session.commit()

async def login_user(id_user: int, command: str, answer: str):
    new_log = LogUser(id_user=id_user,
                      command=command,
                      answer=answer)
    session.add(new_log)
    session.commit()



