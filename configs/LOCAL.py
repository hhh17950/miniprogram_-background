from configs import env, make_dburi


class Settings:
    env = env
    name = '本地环境'
    mongodb_uri = make_dburi(schema='mongodb', sock_path='127.0.0.1:27017',
                             user_name='', pwd='')
    redis_uri = make_dburi(schema='redis', sock_path='127.0.0.1:6039', pwd='')

    token_expire_minutes = 10
    algorithms = "HS256"
    secret_key = "ww7777"

    # 小程序相关
    app_id = ""
    app_secret = ""

    # # api
    # identify_jwt = 'https://apit.matrixone.io/identity/.well-known/openid-configuration/jwks'
    #
    # # cmc
    # cmc_proxy = 'http://home.ymccc.xin:10802'
