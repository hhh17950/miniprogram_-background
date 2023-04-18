from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials
from motor.core import AgnosticCollection

from configs import settings
from db import AioRedisManager
from db.mongodb_helper import AioMongodbManager
from tools import jwt_tools
from starlette.requests import Request

from tools.jwt_tools import User


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(jwt_tools.security)) -> User:
    if settings.env == 'LOCAL':
        return User(id='659092a5-df9e-43fd-b51d-79d4c7ff09ad', email='local_test@qq.com')
    return jwt_tools.get_current_user(credentials)


def get_mongodb_manager(request: Request) -> AioMongodbManager:
    return request.app.state.mongodb_manager


def get_redis_manager(request: Request) -> AioRedisManager:
    return request.app.state.redis_manager


def get_scheduler(request: Request) -> AsyncIOScheduler:
    return request.app.state.scheduler


# 获取特定的mongodb集合
def get_user_collect(mongodb_manager: AioMongodbManager = Depends(get_mongodb_manager)) -> AgnosticCollection:
    return mongodb_manager.get_client(name='mini_program', db='mini_program', collect='user')


# 获取redis Client
def get_cmc_price_redis(redis_manager: AioRedisManager = Depends(get_redis_manager)) -> AioRedisManager:
    return redis_manager.get_client(name='cmc_price')
