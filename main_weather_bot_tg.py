import datetime
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import tg_bot_token, open_weather_token


class WeatherBot:
    def __init__(self, tg_bot_token, open_weather_token):
        self.bot = Bot(token=tg_bot_token)
        self.dp = Dispatcher(self.bot)
        self.open_weather_token = open_weather_token
        self.code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

    async def start_command(self, message: types.Message):
        await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды!")

    async def get_weather(self, message: types.Message):
        try:
            r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={message.text}"
                             f"&appid={self.open_weather_token}&units=metric")
            data = r.json()

            city = data["name"]
            cur_weather = data["main"]["temp"]

            weather_description = data["weather"][0]["main"]
            if weather_description in self.code_to_smile:
                wd = self.code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно, не пойму что там за погода!"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

            await message.reply(
                f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
                f"Продолжительность дня: {length_of_the_day}\n"
                f"***Хорошего дня!***"
            )
        except:
            await message.reply("\U00002620 Проверьте название города \U00002620")

    def register_handlers(self):
        self.dp.register_message_handler(self.start_command, commands=["start"])
        self.dp.register_message_handler(self.get_weather)

    def start(self):
        executor.start_polling(self.dp)


if __name__ == '__main__':
    bot = WeatherBot(tg_bot_token, open_weather_token)
    bot.register_handlers()
    bot.start()
