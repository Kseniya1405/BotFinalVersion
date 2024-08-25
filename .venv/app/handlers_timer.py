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

router_timer = Router()

class Timer(StatesGroup):
    seconds = State()

@router_timer.message(F.text == 'Таймер')
async def timer_step_one(msg: Message, state: FSMContext):
    await state.set_state(Timer.seconds)
    await msg.answer('Количество секунд:')

@router_timer.message(Timer.seconds)
async def timer_step_two(msg: Message, state: FSMContext):
    await state.update_data(seconds=msg.text)
    data = await state.get_data()
    try:
        timer_seconds = int(data['seconds'])
    except:
        await msg.answer('Попробуйте снова, введите целое число, без знаков препинания, букв')

    await state.clear()
    for count in range(timer_seconds-1, -1, -1):
        if count != 0:
            await asyncio.sleep(1)
        else:
            await msg.answer(f'Ваш таймер в {timer_seconds} секунд закончился')


