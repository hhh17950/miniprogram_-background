import json

import httpx
from loguru import logger

from exception import MyException


async def aio_request(url, method='GET', json_res=True, **kwargs):
    try:
        async with httpx.AsyncClient(proxies=kwargs.pop("proxies", None)) as client:
            method = method.upper()
            response = await client.request(method=method, url=url, **kwargs)
            res = response.content
            if json_res:
                res = json.loads(res)
            logger.info(f'请求成功 [{method}] [{url}]')
            return res
    except Exception as e:
        logger.error(f'请求失败 [{method}] [{url}] [{e}]')
        raise MyException(message=str(e))
