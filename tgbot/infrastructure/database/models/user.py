from sqlalchemy import Column, BIGINT

from sqlalchemy import Column, BIGINT

from tgbot.infrastructure.database.models.base import DatabaseModel


class User(DatabaseModel):
    __tablename__ = 'users'

    chat_id = Column(BIGINT, nullable=False, autoincrement=False, primary_key=True)
