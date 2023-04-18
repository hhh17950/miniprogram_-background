import datetime
import json
from urllib.parse import urlparse

import jwt
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jwt import ExpiredSignatureError
from jwt.algorithms import get_default_algorithms
from loguru import logger

from configs import settings
from exception import MyException
from tools.http_helper import aio_request

security = HTTPBearer()


class User(object):
    def __init__(self, **kwargs):
        self.nbf = None
        self.exp = None
        self.iss = None
        self.aud = None
        self.client_id = None
        self.sub = None
        self.auth_time = None
        self.idp = None
        self.id = None
        self.email = None
        self.role = None
        self.FoundRole = None
        self.scope = None
        self.amr = None
        self.user_name = None
        self.img = None
        self.secret = None

        for k, v in kwargs.items():
            if hasattr(self, k):
                self.__setattr__(k, v)

    def db_save(self):
        return {'user_id': self.id, 'user_email': self.email}


async def get_identify_key():
    """
     生成公钥
    :return:
    """
    # 请求key
    res = await aio_request(settings.identify_jwt)
    key_data = res['keys'][0]
    rsa = get_default_algorithms()[key_data['alg']]
    public_key = rsa.from_jwk(json.dumps(key_data))
    settings.public_key = public_key
    settings.algorithms = key_data['alg']
    logger.info(f"公钥获取成功, public_key={public_key}, algorithms={key_data['alg']}")


def create_access_token(user_id, user_name, secret_key):
    to_encode = {"user_id": user_id, 'user_name': user_name, "secret_key": secret_key}
    expire = datetime.datetime.now() + datetime.timedelta(minutes=settings.token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key)
    return encoded_jwt


def decode_token(token):
    payload = jwt.decode(token,
                         key=settings.public_key,
                         issuer=f'http://{urlparse(settings.identify_jwt).netloc}',
                         algorithms=[settings.algorithms],
                         options={
                             'verify_iss': False,
                             # 'verify_iss': False if settings.env == 'LOCAL' else True,
                             'verify_aud': False}
                         )
    return payload


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
    token = credentials.credentials
    try:
        assert credentials.scheme == 'Bearer'
        payload = decode_token(token)  # options={'verify_signature':False}
        user = User(**payload)
        if not user.id:
            raise MyException('错误的Token')
        return user
    except ExpiredSignatureError:
        raise MyException('Token已过期')
    except Exception as e:
        logger.warning(e)
        raise MyException('错误的Token')
