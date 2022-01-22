import datetime
import logging

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted, BadRequest)

from tgbot.misc.analytics import log_stat


async def errors_handler(update: Update, exception, influx_client):
    user = update.message.from_user or update.callback_query.from_user or None
    if user:
        await log_stat(influx_client, user, datetime.datetime.now(), event='Ошибка', error=exception.__class__.__name__)

    if isinstance(exception, CantDemoteChatCreator):
        logging.debug("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logging.debug('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logging.info('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.info('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.debug('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.info(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, CantParseEntities):
        await Update.get_current().message.answer(f'Попало в эррор хендлер. CantParseEntities: {exception.args}')
        return True

    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, BadRequest):
        logging.exception(f'BadRequest: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    logging.exception(f'Update: {update} \n{exception}')


def register_errors(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
