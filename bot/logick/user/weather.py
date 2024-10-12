import requests
import datetime

from db.db_commands import get_city, update_city, add_city


async def get_weather(city_name: str):
    now = datetime.datetime.now()
    city = await get_city(city_name)
    if city:
        if city.date >= now.date() + datetime.timedelta(hours=6):
            return city
        elif city.date < now.date() + datetime.timedelta(hours=6):
            url = (f'https://api.openweathermap.org/data/2.5/weather?id={city.id_city}'
                   f'&units=metric&lang=ru&appid=7c2d87268b0552ce184ed0973ab1078c')
            response = requests.get(url).json()
            await update_city(city=response.name,
                              temp=response['main']['temp'],
                              humidity=response['main']['humidity'],
                              wind_speed=response['wind']['speed'],
                              perceived_temp=response['main']['feels_like'],
                              description_weather=response['weather'][0]['description'],
                              date=now.date())
            city = await get_city(city_name)
            return city
        else:
            return None
    else:
        url = (f'https://api.openweathermap.org/data/2.5/weather?q={city_name}'
               f'&units=metric&lang=ru&appid=7c2d87268b0552ce184ed0973ab1078c')
        response = requests.get(url).json()
        if response['cod'] == '404':
            return None
        else:
            await add_city(city=response['name'],
                            id_city=response['id'],
                            temp=response['main']['temp'],
                            humidity=response['main']['humidity'],
                            wind_speed=response['wind']['speed'],
                            perceived_temp=response['main']['feels_like'],
                            description_weather=response['weather'][0]['description'],
                            date=now.date())
            city = await get_city(city_name)
            return city
