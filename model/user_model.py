#  传入数据库类型  / 接口返回类型
from pydantic import Field, BaseModel

from model import MyBaseModel


class UserItem(BaseModel):
    img: str = Field(None, description="用户头像")
    nike_name: str = Field(None, description="用户名")
    iphone: str = Field(None, description="手机号")


class UserModel(UserItem):
    openid: str = Field(..., description="微信ID")
    secret_key: str = Field(None, description="秘钥信息")
