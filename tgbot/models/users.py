import asyncio
from sqlalchemy import Column, BigInteger, insert, String, update
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from tgbot.config import load_config
from tgbot.services.database import create_db_session
from tgbot.services.db_base import Base


class User(Base):
    __tablename__ = "users"
    telegram_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(length=100))
    last_name = Column(String(length=100), nullable=True)
    username = Column(String(length=100), nullable=True)
    lang_code = Column(String(length=4), default='ru_RU')
    role = Column(String(length=100), default='user')

    @classmethod
    async def get_user(cls, db_session: sessionmaker, telegram_id: int) -> 'User':
        async with db_session() as db_session:
            sql = select(cls).where(cls.telegram_id == telegram_id)
            request = await db_session.execute(sql)
            user: cls = request.scalar()
        return user

    @classmethod
    async def add_user(cls,
                       db_session: sessionmaker,
                       telegram_id: int,
                       first_name: str,
                       last_name: str = None,
                       username: str = None,
                       lang_code: str = None,
                       role: str = None
                       ) -> 'User':
        async with db_session() as db_session:
            sql = insert(cls).values(telegram_id=telegram_id,
                                     first_name=first_name,
                                     last_name=last_name,
                                     username=username,
                                     lang_code=lang_code,
                                     role=role).returning('*')
            result = await db_session.execute(sql)
            await db_session.commit()
            return result.first()

    async def update_user(self, db_session: sessionmaker, updated_fields: dict) -> 'User':
        async with db_session() as db_session:
            sql = update(User).where(User.telegram_id == self.telegram_id).values(**updated_fields)
            result = await db_session.execute(sql)
            await db_session.commit()
            return result

    def __repr__(self):
        return f'User (ID: {self.telegram_id} - {self.first_name} {self.last_name})'
