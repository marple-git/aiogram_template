from typing import List

from sqlalchemy import Column, VARCHAR, BIGINT, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from tgbot.infrastructure.database.models.base import TimedBaseModel


class User(TimedBaseModel):
    telegram_id = Column(BIGINT, nullable=False, autoincrement=False, primary_key=True)
    first_name = Column(VARCHAR(200), nullable=False)
    last_name = Column(VARCHAR(200), server_default=expression.null(), nullable=True)
    username = Column(VARCHAR(200), server_default=expression.null(), nullable=True)

    referrer_id = Column(
        BIGINT,
        ForeignKey("users.telegram_id", ondelete="SET NULL"),
        nullable=True
    )

    referrer: "User" = relationship(
        "User",
        back_populates="referrals",
        lazy="joined",
        uselist=False,
        remote_side=[telegram_id]
    )

    referrals: List["User"] = relationship(
        "User",
        remote_side=[referrer_id],
        back_populates="referrer",
        lazy="joined",
        innerjoin=True,
    )
