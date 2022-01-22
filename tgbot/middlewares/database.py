from typing import Dict, Any

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.infrastructure.database.database_context import DatabaseContext
from tgbot.infrastructure.database.models.user import User


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, session_pool):
        self.session_pool = session_pool
        super().__init__()

    async def pre_process(self, obj: TelegramObject, data: Dict, *args: Any) -> None:
        session: AsyncSession = self.session_pool()
        data["user_db"] = DatabaseContext(session, query_model=User)
        data["session"] = session

    async def post_process(self, obj: TelegramObject, data: Dict, *args: Any) -> None:
        if session := data.get("session", None):
            session: AsyncSession
            await session.close()
