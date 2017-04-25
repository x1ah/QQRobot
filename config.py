# coding: utf-8

# 存储日志至本地
STORE_LOG = True

# 存储日志文件绝对路径
LOG_NAME = '/tmp/QQRobot.log'

# celery 配置
class CeleryConfig(object):
    BROKER_URL = 'redis://127.0.0.1:6379/5'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/6'

