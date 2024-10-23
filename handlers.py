
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import  Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import user_keyboard
from database import async_session, init_models
# bot.py
from aiogram.types import Message
from aiogram.filters import Command  # Добавляем этот импорт
from sqlalchemy import select

from database import async_session, init_models
from models import User, Vids
from storage import DatabaseStorage
router = Router()

videos = ['vid1', 'vid2', 'vid3']

class MyStates(StatesGroup):
    waiting_for_input = State()

async def add_vids(session: AsyncSession, id_vids: list):
    new_vids = Vids(id_vids=id_vids)
    session.add(new_vids)
    await session.commit()
async def check_vids(session: AsyncSession):
    result = await session.execute(select(Vids))
    vids = result.scalars().all()
    return vids

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await message.answer("Привет! Я бот для просмотра и сохранения видео. Выберите действие:", reply_markup=user_keyboard())

    # Устанавливаем состояние для пользователя
    await state.set_state(MyStates.waiting_for_input)
    await state.set_data({'user_id': message.from_user.id})

    # Проверяем, что состояние и данные сохранены
    current_state = await state.get_state()
    current_data = await state.get_data()

    await message.answer(f"Текущее состояние: {current_state}")
    await message.answer(f"Текущие данные: {current_data}")

@router.message(F.text == "Далее")
async def handle_start_watching(message: Message, state: FSMContext):
    async with async_session() as session:
        # Проверяем, существует ли пользователь
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar()
        if not user:
            # Создаем нового пользователя
            new_user = User(
                telegram_id=message.from_user.id,
                name=message.from_user.full_name
            )
            session.add(new_user)
            await session.commit()

        # Добавляем значения в таблицу Vids
        await add_vids(session, videos)

        # Проверяем записи в таблице Vids
        vids = await check_vids(session)
        for vid in vids:
            await message.answer(f"ID: {vid.id}, Videos: {vid.id_vids}")

        # Проверяем состояние и данные
        current_state = await state.get_state()
        current_data = await state.get_data()

        await message.answer(f"Текущее состояние: {current_state}")
        await message.answer(f"Текущие данные: {current_data}")

    
    