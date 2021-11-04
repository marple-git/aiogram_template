from typing import Dict, Any

from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.models.users import User


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data: Dict, *args: Any) -> None:
        session_maker: sessionmaker = obj.bot['session_maker']
        session: AsyncSession = session_maker()
        user = User(session)
        telegram_user: types.User = obj.from_user
        user_info = await user.get_user(telegram_id=telegram_user.id)
        if not user_info:
            user_info = await user.add_user(telegram_user.id)

        data['user'] = user
        data['user_info'] = user_info
        data['session'] = session

    async def post_process(self, obj, data: Dict, *args: Any) -> None:
        if session := data.get("session", None):
            session: AsyncSession
            await session.close()
