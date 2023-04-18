from typing import Dict

import pytz
from bson import CodecOptions
from loguru import logger
from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient


class AioMongodbManager:
    def __init__(self):
        self.mongodb_pool: Dict[str, AsyncIOMotorClient] = {}

    def setup_pool(self, mongodb_url, name: str = None):
        if name not in self.mongodb_pool:
            logger.debug(f'新创建Mongodb连接池 [{mongodb_url}] [{name}]')
        else:
            logger.warning(f'Mongodb连接池 [{name}] 被覆盖创建')
        self.mongodb_pool[name] = AsyncIOMotorClient(mongodb_url)
        return self.mongodb_pool[name]

    def get_client(self, name, db, collect) -> AgnosticCollection:
        if name not in self.mongodb_pool:
            raise Exception(f'not set mongodb pool {name}')

        return self.mongodb_pool[name][db][collect].with_options(
            codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.UTC))
