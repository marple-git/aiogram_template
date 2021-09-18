import asyncio
from sqlalchemy import Column, BigInteger, insert, String, update
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from tgbot.config import load_config
from tgbot.services.database import create_db_session
from tgbot.services.db_base import Base


class User(Base):
    __tablename__ = "users"
    chat_id = Column(BigInteger, primary_key=True)

    @classmethod
    async def get_user(cls, session: AsyncSession, telegram_id: int) -> 'User':
        async with session.begin():
            sql = select(cls).where(cls.chat_id == telegram_id)
            request = await session.execute(sql)
            user: cls = request.scalar()
        return user

    @classmethod
    async def add_user(cls,
                       session: AsyncSession,
                       chat_id: int
                       ) -> 'User':
        async with session.begin():
            sql = insert(cls).values(chat_id=chat_id).returning('*')
            result = await session.execute(sql)
            return result.first()

    async def update_user(self, session: AsyncSession, updated_fields: dict) -> 'User':
        async with session.begin():
            sql = update(User).where(User.chat_id == self.chat_id).values(**updated_fields)
            result = await session.execute(sql)
            return result

    def __repr__(self):
        return f'User (ID: {self.chat_id} - {self.first_name} {self.last_name})'
