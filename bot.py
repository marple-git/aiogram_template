import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import load_config
from tgbot.handlers import start
from tgbot.infrastructure.database.models.base import DatabaseModel
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.misc.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


def setup_scheduler_jobs(scheduler: AsyncIOScheduler):
    pass


def register_all_middlewares(dp):
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())


def register_all_filters(dp: Dispatcher):
    pass


def register_all_handlers(dp: Dispatcher):
    routers = [start.router]
    for router in routers:
        dp.include_router(router)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()

    dp['config'] = config

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
    dp['session_maker'] = sqlalchemy_session_pool

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()
        await engine.dispose()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
