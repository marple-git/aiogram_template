from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.misc.analytics import log_stat


async def bot_echo(message: types.Message, influx_client):
    text = [
        "Эхо без состояния.",
        "Сообщение:",
        message.text
    ]

    await message.answer('\n'.join(text))
    await log_stat(influx_client, message.from_user, message.date,
                   event='Не распознано')


async def bot_echo_all(message: types.Message, state: FSMContext, influx_client):

    state_name = await state.get_state()
    text = [
        f'Эхо в состоянии {hcode(state_name)}',
        'Содержание сообщения:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text))
    await log_stat(influx_client, message.from_user, message.date,
                   event=f'Не распознано: {state_name}')


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
