from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.misc.analytics import log_stat


async def help_command(message: Message, influx_client):
    await message.reply('Вызвана команда Help')
    await log_stat(
        influx_client, message.from_user, message.date, event='Команда Help'
    )


async def privacy_command(message: Message, influx_client):
    await message.reply('Вызвана команда Privacy')
    await log_stat(
        influx_client, message.from_user, message.date, event='Команда Privacy'
    )


async def settings_command(message: Message, influx_client):
    await message.reply('Вызвана команда Settings')
    await log_stat(
        influx_client, message.from_user, message.date, event='Команда Settings'
    )


def register_commands(dp: Dispatcher):
    dp.register_message_handler(help_command, commands=["help"])
    dp.register_message_handler(privacy_command, commands=["privacy"])
    dp.register_message_handler(settings_command, commands=["settings"])
