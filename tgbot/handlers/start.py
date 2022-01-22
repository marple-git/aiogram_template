from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.infrastructure.database.database_context import DatabaseContext
from tgbot.infrastructure.database.models.user import User


async def user_start(message: Message, user_db: DatabaseContext[User]):
    if not await user_db.exists(User.telegram_id == message.from_user.id):
        await user_db.add(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.first_name,
            username=message.from_user.username,
        )
    users_count = await user_db.count()
    await message.answer(
        "\n".join(
            [
                f'Привет, {message.from_user.full_name}!',
                f'Кол-во человек в базе: {users_count}',
            ])
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
