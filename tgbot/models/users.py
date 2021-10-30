from sqlalchemy import Column, BigInteger, insert, update, String
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.services.db_base import Base


class User(Base):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    __tablename__ = "users"
    chat_id = Column(BigInteger, primary_key=True)
    description = Column(String)

    async def get_user(self, telegram_id: int) -> 'User':
        async with self.session.begin():
            sql = select(User).where(User.chat_id == telegram_id)
            request = await self.session.execute(sql)
            user: User = request.scalar()
        return user

    async def add_user(self,
                       chat_id: int
                       ) -> 'User':
        async with self.session.begin():
            sql = insert(User).values(chat_id=chat_id).returning('*')
            result = await self.session.execute(sql)
            return result.first()

    async def update_user(self, chat_id: int, updated_fields: dict) -> 'User':
        async with self.session.begin():
            sql = update(User).where(User.chat_id == chat_id).values(**updated_fields)
            result = await self.session.execute(sql)
            return result

    def __repr__(self):
        return f'User (ID: {self.chat_id})'
