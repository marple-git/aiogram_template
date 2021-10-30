from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.users import User


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        session = obj.bot['db']
        user = User(session)
        telegram_user: types.User = obj.from_user
        user_info = await user.get_user(telegram_id=telegram_user.id)
        if not user_info:
            user_info = await user.add_user(telegram_user.id)

        data['user'] = user
        data['user_info'] = user_info
