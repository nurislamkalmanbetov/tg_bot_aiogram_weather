import requests
import datetime
from pprint import pprint
from config import open_weather_token


class Weather:
    def __init__(self, city, token):
        self.city = city
        self.token = token
        self.code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

    def get_weather_data(self):
        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.token}&units=metric"
            )
            data = r.json()
            pprint(data)

            self.cur_weather = data["main"]["temp"]

            self.weather_description = data["weather"][0]["main"]
            if self.weather_description in self.code_to_smile:
                self.wd = self.code_to_smile[self.weather_description]
            else:
                self.wd = "Посмотри в окно, не пойму что там происходит"

            self.humidity = data["main"]["humidity"]
            self.pressure = data["main"]["pressure"]
            self.wind = data["wind"]["speed"]
            self.sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            self.sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            self.lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

        except Exception as ex:
            print(ex)
            print("Проверьте название города: ")

    def display_weather(self):
        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"погода в городе: {self.city}\nТемпература: {self.cur_weather}C°{self.wd}\n"
              f"Влажнось: {self.humidity}\т Давление: {self.pressure} мм.рт.ст\nВетер: {self.wind} метр в секунду\n"
              f"Восход солнца: {self.sunrise_timestamp}\nПродолжительность дня: {self.lenght_of_the_day}\n"
              f"Хорошего дня!")

    def get_weather(self):
        self.get_weather_data()
        self.display_weather()


def main():
    city = input("Введие город: ")
    weather = Weather(city, open_weather_token)
    weather.get_weather()


if __name__ == "__main__":
    main()