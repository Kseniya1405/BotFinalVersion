import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

router_timer = Router()

# Объявляем, какие именно состояния будут обрабатываться.
class Timer(StatesGroup):
    seconds = State()


@router_timer.message(F.text == 'Таймер')
async def timer_step_one(msg: Message, state: FSMContext):
    """ Запускаем диалог с помощью команды "Таймер". Переводим пользователя в состояние Timer.seconds. """
    await state.set_state(Timer.seconds)
    await msg.answer('Количество секунд:')


@router_timer.message(Timer.seconds)
async def timer_step_two(msg: Message, state: FSMContext):
    """ Сохранить данные в хранилище и запустить таймер."""
    await state.update_data(seconds=msg.text)
    data = await state.get_data()
    try:
        timer_seconds = int(data['seconds'])
    except ValueError:
        await msg.answer('Попробуйте снова, введите целое число, без знаков препинания, букв')

    await state.clear()
    # Создание асинхронного таймера с обратным отсчетом, используя в качестве точки отсчета значение состояния Timer.seconds.
    for count in range(timer_seconds-1, -1, -1):
        if count != 0:
            await asyncio.sleep(1)
        else:
            await msg.answer(f'Ваш таймер в {timer_seconds} секунд закончился')
