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

router_time = Router()

class Time(StatesGroup):
    method = State()
    location = State()
    city_name = State()


@router_time.message(F.text == 'Время')
async def time_step_one(msg: Message, state: FSMContext):
    await state.set_state(Time.method)
    await msg.answer('Где?', reply_markup=kb.time)

@router_time.message(Time.method)
async def time_step_two(msg: Message, state: FSMContext):
    await state.update_data(method=msg.text)
    data_time = await state.get_data()
    method = str(data_time['method'])
    if method == "По местоположению":
        await state.update_data(city_name='None')
        await msg.answer('Местоположение', reply_markup=kb.geo)
        await state.set_state(Time.location)

    elif method == "По городу":
        await state.update_data(location='None')
        await state.set_state(Time.city_name)
        await msg.answer('Название города:')

@router_time.message(Time.location)
async def location_time_handler(msg: Message, state: FSMContext):
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
        timezone = data['timezone']

        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        await msg.answer(f"***{datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')}***")
    except:
        await msg.answer("Попробуйте повторить запрос, на этот раз укажите город")

@router_time.message(Time.city_name)
async def time_step_three(msg: Message, state: FSMContext):
    await state.update_data(city_name=msg.text)
    data_time = await state.get_data()
    city_name = str(data_time['city_name'])
    await state.clear()

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        timezone = data['timezone']

        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        await msg.answer(f"***{datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')}***")
    except:
        await msg.answer("Введите другое наименование, пожалуйста ")
