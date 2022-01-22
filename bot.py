import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.errors import register_errors
from tgbot.handlers.start import register_user
from tgbot.infrastructure.database.models.base import DatabaseModel
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.misc.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, session_pool):
    dp.setup_middleware(DatabaseMiddleware(session_pool))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_user(dp)
    register_errors(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env.dist")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    await set_default_commands(bot)

    engine = create_async_engine(
        config.db.construct_sqlalchemy_url(),
        query_cache_size=1200,
        pool_size=100,
        max_overflow=200,
        future=True,
        echo=True
    )

    async with engine.begin() as conn:
        #await conn.run_sync(DatabaseModel.metadata.drop_all)
        await conn.run_sync(DatabaseModel.metadata.create_all)

    # noinspection PyTypeChecker
    sqlalchemy_session_pool = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    register_all_middlewares(dp, sqlalchemy_session_pool)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        await engine.dispose()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
