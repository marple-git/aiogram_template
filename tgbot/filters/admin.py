from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, config: Config) -> bool:
        return message.from_user.id in config.tg_bot.admin_ids
