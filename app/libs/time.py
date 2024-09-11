import datetime

import requests
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import libs.keyboard as kb
from config.config import open_weather_token

router_time = Router()

# Объявляем, какие именно состояния будут обрабатываться.
class Time(StatesGroup):
    method = State()
    location = State()
    city_name = State()


@router_time.message(F.text == 'Время')
async def time_step_one(msg: Message, state: FSMContext):
    """ Запускаем диалог с помощью команды "Время". Переводим пользователя в состояние Time.method. """
    await state.set_state(Time.method)
    await msg.answer('Где?', reply_markup=kb.time)


@router_time.message(Time.method)
async def time_step_two(msg: Message, state: FSMContext):
    """ Сохранить данные в хранилище и перейти к следующему шагу.

    У состояния Time.method может быть только два значения 'По местоположению' и 'По городу'.
    """
    await state.update_data(method=msg.text)
    data_time = await state.get_data()
    method = str(data_time['method'])
    if method == "По местоположению":
        """ Если у Time.method значение 'По местоположению', то обновляем значение Time.city_name и переходим к следующему шагу. """
        await state.update_data(city_name='None')
        await msg.answer('Местоположение', reply_markup=kb.geo)
        await state.set_state(Time.location)

    elif method == "По городу":
        """ Если у Time.method значение 'По городу', то обновляем значение Time.location и переходим к следующему шагу. """
        await state.update_data(location='None')
        await state.set_state(Time.city_name)
        await msg.answer('Название города:')


@router_time.message(Time.location)
async def location_time_handler(msg: Message, state: FSMContext):
    """ Обновляем значение Time.location , получаем и обрабатываем геопозицию, выводим время. """
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
        timezone = data['timezone']

        # Создаем объект временной зоны, который соответствует смещению, заданному переменной timezone.
        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        # Выводим время данной временной зоны в указанном формате.
        await msg.answer(f"***{datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')}***")
    except AttributeError:
        await msg.answer("Попробуйте повторить запрос, на этот раз укажите город")


@router_time.message(Time.city_name)
async def time_step_three(msg: Message, state: FSMContext):
    """ Обновляем значение Time.city_name , получаем название города, выводим время. """
    await state.update_data(city_name=msg.text)
    data_time = await state.get_data()
    city_name = str(data_time['city_name'])
    await state.clear()
    try:
        # Делаем запрос с сайта.
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        timezone = data['timezone']

        # Создаем объект временной зоны, который соответствует смещению, заданному переменной timezone.
        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        # Выводим время данной временной зоны в указанном формате.
        await msg.answer(f"***{datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')}***")
    except KeyError:
        await msg.answer("Введите другое наименование, пожалуйста ")
