from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.models.users import User


async def start(m: Message, user: User):
    await m.answer(f'Приветствую, {m.from_user.first_name}.\n'
                   f'Ваш баланс: {user.balance}P')


def register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
