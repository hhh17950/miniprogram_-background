from typing import Dict

from loguru import logger
from redis import asyncio as aioredis


class AioRedisManager:
    def __init__(self):
        self.redis_pool: Dict[str, aioredis.ConnectionPool] = {}
        self.maxsize = 10

    def setup_pool(self, redis_url, *, db, name: str = None) -> aioredis.Redis:
        """
               :param redis_url: redis://[[username]:[password]]@localhost:6379/0
               :param db: 库
               :param name: 设置连接名称
               :return:
               """
        addr = redis_url.split("@")[1]
        name = name or f'{addr}/{db}'
        if name not in self.redis_pool:
            logger.debug(f'新创建Redis连接池 [{addr}] [{name}:{db}]')
        else:
            logger.warning(f'Redis连接池 [{name}] 被覆盖创建')
            # await self.redis_pool[name].disconnect()
        self.redis_pool[name] = aioredis.ConnectionPool.from_url(
            url=f'{redis_url}/{db}',
            max_connections=self.maxsize,
            encoding='UTF-8',
            decode_responses=True)
        return aioredis.Redis(connection_pool=self.redis_pool[name])

    def get_client(self, name) -> aioredis.Redis:
        if name not in self.redis_pool:
            raise Exception(f'not set redis pool {name}')
        return aioredis.Redis(connection_pool=self.redis_pool[name])

    async def close(self):
        for name, pool in self.redis_pool.items():
            await pool.disconnect()
        self.redis_pool = {}


if __name__ == '__main__':
    redis_manager = AioRedisManager()
    redis_manager.setup_pool(DefaultSettings.REDIS_URL, db=5, name='stock')
    conn = redis_manager.get_client('stock')
    data = conn.get('stocks')
    print(data)
