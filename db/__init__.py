from loguru import logger

from configs import settings
from db.mongodb_helper import AioMongodbManager
from db.redis_helper import AioRedisManager


def register_mongodb(app):
    mongodb_manager = AioMongodbManager()
    mongodb_manager.setup_pool(settings.mongodb_uri, 'mini_program')
    # mongodb_manager.setup_pool(settings.jasper_mongodb_uri, 'jasper')
    app.state.mongodb_manager = mongodb_manager


def register_redis(app):
    redis_manager = AioRedisManager()
    logger.info(settings.redis_uri)
    redis_manager.setup_pool(settings.redis_uri, db=3, name='cmc_price')
    app.state.redis_manager = redis_manager
