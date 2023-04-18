import asyncio
from exception import MyException

from tools.http_helper import aio_request
from .jwt_tools import User
from configs import settings

# 房间
# 所有线索
# 收集线索
# 对话
# 房间玩家
# from core.qrcode_helper import make_code


class WXHelper:
    def __init__(self, app_id=None, app_secret=None, token=''):
        self.app_id = app_id
        self.app_secret = app_secret
        self.token = token
        self.access_token = {}

    async def get_openid(self, code):
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={self.app_id}&secret={self.app_secret}&js_code={code}&grant_type=authorization_code"
        res = await aio_request(url, method="POST")
        return res['openid'], res["secret"]

    async def get_user_info(self, code, img, name) -> User:
        try:
            openid,  secret = await self.get_openid(code)
            user_info = User()
            user_info.id = openid
            user_info.user_name = name
            user_info.img = img
            user_info.secret = secret
            return user_info
        except Exception as e:
            raise MyException(f'获取微信用户信息失败 {e}')


wx_tools = WXHelper(
    app_id=settings.app_id,
    app_secret=settings.app_secret,
    token=settings.app_token
)

# wx_tools = WXHelper(appid='wx79041d8625ec9aa8', secret='c0021e35348e6b177ecaccda8b816ed4', token='ymc4399')

if __name__ == '__main__':
    # auth_url = f'https://open.weixin.qq.com/connect/oauth2/authorize?appid={wx_tools.appid}&redirect_uri={settings.redirect_url}&response_type=code&scope=snsapi_userinfo#wechat_redirect'
    # image_data = make_code(auth_url, 300, 300)  # 二维码大小
    # image_data.save('123.png')
    asyncio.run(wx_tools.get_openid('083UMqFa135S5D0wppJa1n5giw1UMqFL'))
