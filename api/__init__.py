from fastapi import APIRouter
from . import health_router, user_router

api_router = APIRouter()


api_router.include_router(health_router.router, prefix="/health", tags=["健康管理"])
api_router.include_router(user_router.router, prefix="", tags=["用户中心"])



