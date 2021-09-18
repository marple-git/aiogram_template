from sqlalchemy import Column, BigInteger, insert, String, update, Boolean, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from tgbot.services.db_base import Base


class User(Base):
    __tablename__ = "users"
    chat_id = Column(BigInteger, primary_key=True)
    username = Column(String(length=100), nullable=True)
    balance = Column(Integer, default=0)
    admin = Column(Boolean, default=False)

    @classmethod
    async def get_user(cls, session: AsyncSession, chat_id: int) -> 'User':
        async with session.begin():
            sql = select(cls).where(cls.chat_id == chat_id)
            request = await session.execute(sql)
            user: User = request.scalar()
        return user

    @classmethod
    async def add_user(cls,
                       session: AsyncSession,
                       chat_id: int,
                       username: str = None,
                       ) -> 'User':
        async with session.begin():
            sql = insert(cls).values(chat_id=chat_id,
                                     username=username).returning('*')
            result = await session.execute(sql)
            return result.first()

    async def update_user(self, session: AsyncSession, updated_fields: dict) -> 'User':
        async with session.begin():
            sql = update(User).where(User.chat_id == self.chat_id).values(**updated_fields)
            result = await session.execute(sql)
            return result

    def __repr__(self):
        return f'User (ID: {self.chat_id} - {self.username} {self.balance})'
