from aiogram import Dispatcher, Router, F
from aiogram.dispatcher.filters.command import CommandStart
from aiogram.types import Message

from tgbot.infrastructure.database.database_context import DatabaseContext
from tgbot.infrastructure.database.models.user import User


router = Router()


@router.message(CommandStart(), F.chat.type == 'private', state='*')
async def user_start(m: Message, user_db: DatabaseContext[User], user_info: User):
    if not user_info:
        await user_db.add(chat_id=m.from_user.id)
    await m.answer('Привет!')
