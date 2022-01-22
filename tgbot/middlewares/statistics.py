from typing import Dict, Any

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject


class InfluxMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["update"]

    def __init__(self, influx_client):
        self.influx_client = influx_client
        super().__init__()

    async def pre_process(self, obj: TelegramObject, data: Dict, *args: Any) -> None:
        data["influx_client"] = self.influx_client

