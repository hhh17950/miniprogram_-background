import os
from urllib.parse import quote_plus


def make_dburi(schema, sock_path, user_name='', pwd=''):
    user_name = quote_plus(user_name) if user_name else ''
    pwd = quote_plus(pwd) if pwd else ''
    if user_name or pwd:
        return f"{schema}://{user_name}:{pwd}@{sock_path}"
    else:
        return f"{schema}://{sock_path}"


# 获取环境变量
env = os.getenv("MATRIXONE_ENVIRONMENT", "LOCAL")
if env == 'LOCAL':
    from configs.LOCAL import Settings
elif env == 'S':
    from configs.S import Settings
elif env == 'TEST':
    from configs.TEST import Settings
else:
    raise Exception(f'not support ENVIRONMENT {env}')
settings = Settings()
