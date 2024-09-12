import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import API_TOKEN
from libs.weather import router
from libs.time import router_time
from libs.timer import router_timer


async def main():
    """ Здесь создается объект бота, cоздается объект диспетчера.

    Запускаем бот в режиме опроса(polling), удаляем webhook, регулярно проверяем наличие новых обновлений от Tg с указанными типами обновлений.
    """
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)   # Этот метод добавляет маршрутизатор (router) в диспетчер.
    dp.include_router(router_time)   # Этот метод добавляет маршрутизатор (router_time) в диспетчер.
    dp.include_router(router_timer)   # Этот метод добавляет маршрутизатор (router_timer) в диспетчер.
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    # Hастраиваем базовую конфигурацию для модуля логирования, устанавливает уровень логирования на INFO.
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())   # Запускаем асинхронную функцию main().
