from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand('start', 'Старт'),
            BotCommand('privacy', 'Приватность?'),
            BotCommand('help', 'Помогите'),
            BotCommand('settings', 'Настроек нет'),
            BotCommand('other', 'Чет еще'),
        ]
    )
