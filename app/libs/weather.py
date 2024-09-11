import datetime

import requests
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import libs.keyboard as kb
from config.config import open_weather_token


router = Router()

# Объявляем, какие именно состояния будут обрабатываться.
class Weather(StatesGroup):
    method = State()
    location = State()
    city_name = State()


@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer("Выберите категорию меню",
                     reply_markup=kb.main)


@router.message(F.text.lower() == 'меню')
async def menu_handler(msg: Message):
    await msg.answer("Выберите категорию меню",
                     reply_markup=kb.main)


@router.message(F.text == 'Погода')
async def weather_step_one(msg: Message, state: FSMContext):
    """ Запускаем диалог с помощью команды "Погода". Переводим пользователя в состояние Weather.method. """
    await state.set_state(Weather.method)
    await msg.answer('Где?', reply_markup=kb.weather)


@router.message(Weather.method)
async def weather_step_two(msg: Message, state: FSMContext):
    """ Сохранить данные в хранилище и перейти к следующему шагу.

    У состояния Weather.method может быть только два значения 'По местоположению' и 'По городу'.
    """
    await state.update_data(method=msg.text)
    data_weather = await state.get_data()
    method = str(data_weather['method'])
    if method == "По местоположению":
        """ Если у Weather.method значение 'По местоположению', то обновляем значение Weather.city_name и переходим к следующему шагу. """
        await state.update_data(city_name='None')
        await msg.answer('Местоположение', reply_markup=kb.geo)
        await state.set_state(Weather.location)

    elif method == "По городу":
        """ Если у Weather.method значение 'По городу', то обновляем значение Weather.location и переходим к следующему шагу. """
        await state.update_data(location='None')
        await state.set_state(Weather.city_name)
        await msg.answer('Название города:')


@router.message(Weather.location)
async def location_handler(msg: Message, state: FSMContext):
    """ Обновляем значение Weather.location , получаем и обрабатываем геопозицию, выводим погоду. """
    await state.update_data(location=msg.location)
    latitude = msg.location.latitude
    longitude = msg.location.longitude
    await state.clear()
    try:
        # Делаем запрос с сайта.
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']

        # Выводим время пользователя, погоду в указанном городе с температурой, влажностью и давлением.
        await msg.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                         f"Погода в городе {city}\nТемпература: {cur_weather}C°\n"
                         f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст."
                         )
    except AttributeError:
        await msg.answer("Попробуйте повторить запрос, на этот раз укажите город")


@router.message(Weather.city_name)
async def weather_step_three(msg: Message, state: FSMContext):
    """ Обновляем значение Weather.city_name , получаем название города, выводим погоду. """
    await state.update_data(city_name=msg.text)
    data_weather = await state.get_data()
    city_name = str(data_weather['city_name'])
    await state.clear()
    try:
        # Делаем запрос с сайта.
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']

        # Выводим время пользователя, погоду в указанном городе с температурой, влажностью и давлением.
        await msg.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                f"Погода в городе {city}\nТемпература: {cur_weather}C°\n"
                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст."
                )
    except KeyError:
        await msg.answer("Введите другое наименование, пожалуйста ")


