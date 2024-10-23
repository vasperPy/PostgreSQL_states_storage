
# bot.py
from handlers import router as user_router 
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command  # Добавляем этот импорт
from sqlalchemy import select
from storage import DatabaseStorage
from database import async_session, init_models
from models import User

API_TOKEN = 'YOURTOKEN'
storage = DatabaseStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)
dp.include_router(user_router) 

async def main():
    await init_models()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
