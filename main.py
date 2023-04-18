import traceback

import pytz
import uvicorn
from apscheduler.triggers import interval
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from api import api_router
from configs import settings
from db import register_mongodb, register_redis
from exception import MyException
from model import ErrorResponse
from tools.jwt_tools import get_identify_key
from tools.scheduler import create_scheduler

if settings.env != 'LOCAL':
    openapi_prefix = '/pyfund'
    debug = False
else:
    openapi_prefix = ''
    debug = True

app = FastAPI(docs_url='/swagger', openapi_prefix=openapi_prefix, debug=debug)


@app.exception_handler(MyException)
async def not_fund_exception_handler(request: Request, exc: MyException):
    return JSONResponse(ErrorResponse(message=str(exc), status=exc.status).dict())


@app.exception_handler(AssertionError)
async def assert_exception_handler(request: Request, exc: AssertionError):
    return JSONResponse(ErrorResponse(message=str(exc), status=status.HTTP_400_BAD_REQUEST).dict())


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    请求参数验证异常
    :param request: 请求头信息
    :param exc: 异常对象
    :return:
    """
    # 日志记录异常详细上下文
    return JSONResponse(ErrorResponse(message='参数错误 ' + str(exc), status=status.HTTP_400_BAD_REQUEST).dict())


@app.exception_handler(Exception)
async def sys_exception_handler(request: Request, exc: Exception):
    logger.error(f"全局异\n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    return JSONResponse(
        ErrorResponse(message='系统异常' + f' {str(exc)}' if settings.name in ['本地环境', "测试环境"] else '',
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR).dict())


@app.on_event('startup')
async def startup():
    # 鉴权中心获取公钥
    # await get_identify_key()
    # 挂载 mongodb
    register_mongodb(app)
    # 挂载redis
    # register_redis(app)
    # 添加路由
    app.include_router(api_router)

    # 添加定时任务
    app.state.scheduler = create_scheduler(settings.mongodb_uri)
    # cmc_price = CMCPrice(app.state.mongodb_manager)
    # await cmc_price.init()

    # app.state.scheduler.add_job(
    #     cmc_price.update_scheduler_task,
    #     id='ohlcv_update_task',
    #     trigger=interval.IntervalTrigger(hours=1, minutes=10, timezone=pytz.UTC),
    #     jobstore='memory',
    #     misfire_grace_time=600 * 3
    # )

    # app.state.scheduler.add_job(
    #     update_staking_bill_status_task,
    #     args=(BeaconChaService(), app.state.mongodb_manager,),
    #     id='update_staking_bill_status',
    #     trigger=interval.IntervalTrigger(minutes=1, timezone=pytz.UTC),
    #     jobstore='memory',
    #     misfire_grace_time=20
    # )

    # if settings.env == 'LOCAL':
    #     return
    app.state.scheduler.start()

    app.state.scheduler.print_jobs()


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
