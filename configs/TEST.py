from configs import env, make_dburi


class Settings:
    env = env
    name = '测试环境'
    # py_fund_mongodb_uri = make_dburi(schema='mongodb', sock_path='172.10.0.18:27018',
    #                                  user_name='root', pwd='ETHQig66tzxoZc+wuIPEUTMVsY')
    # jasper_mongodb_uri = make_dburi(schema='mongodb', sock_path='172.10.0.18:27018',
    #                                 user_name='root', pwd='ETHQig66tzxoZc+wuIPEUTMVsY')  # 数据库版本问题
    # # mongodb = mongodb_url('127.0.0.1:27017')
    # redis_uri = make_dburi(schema='redis', sock_path='172.10.0.18:6379', pwd='MukAzxGMOL2')
    #
    # # api
    # identify_jwt = 'http://identity.matrixone-test.svc/.well-known/openid-configuration/jwks'
    #
    # # cmc
    # cmc_proxy = None
