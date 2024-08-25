import asyncio
import logging
import requests
import datetime
from config import API_TOKEN, open_weather_token
from aiogram import Bot, Dispatcher
from handlers import router
from handlers_time import router_time
from handlers_timer import router_timer

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(router_time)
    dp.include_router(router_timer)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())