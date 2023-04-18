from fastapi import APIRouter, Depends
from motor.core import AgnosticCollection
from pymongo import ReturnDocument

from dependencies import get_user_collect
from model import Response
from model.user_model import UserItem
from tools.jwt_tools import create_access_token
from tools.wx_helper import wx_tools

router = APIRouter()


@router.post('/login', response_model=Response[str])
async def login(
        code: str,
        user_item: UserItem,
        collect: AgnosticCollection = Depends(get_user_collect)
):
    open_id, secret = await wx_tools.get_openid(code=code)
    user = await collect.find_one_and_update(
        {"openid": open_id},
        {"$set": {**user_item.dict(), **{"openid": open_id, "secret": secret}}}
        , upsert=True, return_document=ReturnDocument.AFTER)
    token = create_access_token(user_id=user["open_id"], user_name=user["nike_name"], secret_key=user["secret_key"])
    response = Response(data=token)
    return response
