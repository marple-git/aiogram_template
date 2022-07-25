from typing import Dict, Any, Callable, Awaitable, Union

from aiogram import BaseMiddleware, types
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.infrastructure.database.database_context import DatabaseContext
from tgbot.infrastructure.database.models.user import User


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Union[Message, CallbackQuery],
                       data: Dict[str, Any]) -> None:
        session_maker = data['session_maker']
        session: AsyncSession = session_maker()
        user_db = DatabaseContext(session, query_model=User)

        telegram_user: types.User = event.from_user
        chat_type = event.chat.type if isinstance(event, Message) else event.message.chat.type

        if chat_type not in ['supergroup', 'private', 'group']:
            return

        user_info = await user_db.get_one(User.chat_id == telegram_user.id)

        data['user_db'] = user_db
        data['user_info'] = user_info

        result = await handler(event, data)
        return result
