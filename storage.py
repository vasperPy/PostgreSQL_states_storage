from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import StateStorage
from database import async_session
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey
from typing import Dict, Any, Optional
from aiogram.fsm.state import State

class DatabaseStorage(BaseStorage):
    async def close(self) -> None:
        pass

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        async with async_session() as session:
            result = await session.execute(
                select(StateStorage).where(StateStorage.key == str(key))
            )
            state_record = result.scalar()
            if state_record:
                state_record.state = state.state if isinstance(state, State) else state
            else:
                state_record = StateStorage(key=str(key), state=state.state if isinstance(state, State) else state)
                session.add(state_record)
            await session.commit()

    async def get_state(self, key: StorageKey) -> Optional[str]:
        async with async_session() as session:
            result = await session.execute(
                select(StateStorage).where(StateStorage.key == str(key))
            )
            state_record = result.scalar()
            return state_record.state if state_record else None

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        async with async_session() as session:
            result = await session.execute(
                select(StateStorage).where(StateStorage.key == str(key))
            )
            state_record = result.scalar()
            if state_record:
                state_record.data = data
            else:
                state_record = StateStorage(key=str(key), data=data)
                session.add(state_record)
            await session.commit()

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        async with async_session() as session:
            result = await session.execute(
                select(StateStorage).where(StateStorage.key == str(key))
            )
            state_record = result.scalar()
            return state_record.data if state_record else {}
