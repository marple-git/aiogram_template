from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.misc.analytics import log_stat


async def admin_start(message: Message, influx_client):
    await message.reply("Hello, admin!")
    await log_stat(influx_client, message.from_user, message.date, event='Команда admin')


async def no_admin_start(message: Message, influx_client):
    await message.reply("Hello, no admin!")
    await log_stat(influx_client, message.from_user, message.date, event='Команда admin')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["admin"], state="*", is_admin=True)
    dp.register_message_handler(admin_start, commands=["admin"], state="*", is_admin=False)
