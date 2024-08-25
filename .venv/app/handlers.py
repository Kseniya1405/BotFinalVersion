from aiogram import types, F, Router
from aiogram.types import Message, location
from aiogram.filters import Command, CommandStart
import requests
import datetime
from config import API_TOKEN, open_weather_token
import keyboard as kb
import asyncio
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_location import SendLocation

router = Router()

class Weather(StatesGroup):
    method = State()
    location = State()
    city_name = State()

@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer("Выберите категорию меню",
                     reply_markup=kb.main)
@router.message(F.text == 'меню')
async def menu_handler(msg: Message):
    await msg.answer("Выберите категорию меню",
                     reply_markup=kb.main)
@router.message(F.text == 'Меню')
async def menu_handler(msg: Message):
    await msg.answer("Выберите категорию меню",
                     reply_markup=kb.main)

####
@router.message(F.text == 'Погода')
async def weather_step_one(msg: Message, state: FSMContext):
    await state.set_state(Weather.method)
    await msg.answer('Где?', reply_markup=kb.weather)

@router.message(Weather.method)
async def weather_step_two(msg: Message, state: FSMContext):
    await state.update_data(method=msg.text)
    data_weather = await state.get_data()
    method = str(data_weather['method'])
    if method == "По местоположению":
        await state.update_data(city_name='None')
        await msg.answer('Местоположение', reply_markup=kb.geo)
        await state.set_state(Weather.location)

    elif method == "По городу":
        await state.update_data(location='None')
        await state.set_state(Weather.city_name)
        await msg.answer('Название города:')


@router.message(Weather.location)
async def location_handler(msg: Message, state: FSMContext):
    await state.update_data(location=msg.location)
    latitude = msg.location.latitude
    longitude = msg.location.longitude
    await state.clear()
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # df = pd.json_normalize(data)
        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']

        await msg.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                         f"Погода в городе {city}\nТемпература: {cur_weather}C°\n"
                         f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст."
                         )
    except:
        await msg.answer("Попробуйте повторить запрос, на этот раз укажите город")


@router.message(Weather.city_name)
async def weather_step_three(msg: Message, state: FSMContext):
    await state.update_data(city_name=msg.text)
    data_weather = await state.get_data()
    city_name = str(data_weather['city_name'])
    await state.clear()
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
    #df = pd.json_normalize(data)
        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']

        await msg.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                f"Погода в городе {city}\nТемпература: {cur_weather}C°\n"
                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст."
                )
    except:
        await msg.answer("Введите другое наименование, пожалуйста ")


