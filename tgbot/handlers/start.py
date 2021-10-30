from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.models.users import User


async def start(m: Message, user_info: User):
    await m.answer(f'Привет, товарищ!\nВаше описание: {user_info.description}')


async def set_description(m: Message, user: User):
    args = m.get_args()
    await user.update_user(m.chat.id, {'description': args})
    await m.reply('Описание было успешно изменено!')


def register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(set_description, commands=['set_description'])
