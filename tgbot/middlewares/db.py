from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from tgbot.models.users import User
from aiogram import types


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        db_session = obj.bot.get('db')
        telegram_user: types.User = obj.from_user
        user = await User.get_user(session=db_session, telegram_id=telegram_user.id)
        if not user:
            user = await User.add_user(db_session, telegram_user.id)

        data['user'] = user
