# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/7 18:42
import os
import redis
BASE_DIR=os.path.dirname(os.path.dirname(__file__))

class BaseSetting(object):
    #sqlalchemy连接数据库
    SQLALCHEMY_DATABASE_URI= 'mysql://root:oracle@192.168.187.136:3306/flask_ihome?charset=utf8'
    #sqlalchemy测试数据库
    TEST_SQLALCHEMY_DATABASE_URI= 'mysql://root:oracle@192.168.187.136:3306/flask_test?charset=utf8'
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False
    #数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）。
    SQLALCHEMY_POOL_SIZE = 10
    #可以省去db.session.commit()的操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True

    REDIS_HOST='192.168.187.136'
    REDIS_PORT=6379

    #session过期时间
    PERMANENT_SESSION_LIFETIME=7*24*60*60
    #session保存地点
    SESSION_TYPE='redis'
    #是否为cookie设置签名来保护数据不被更改，默认是False；如果设置True,那么必须设置flask的secret_key参数；
    SESSION_USE_SIGNER=True
    SECRET_KEY='21312321312sdadwewq'
    #在所有的会话键之前添加前缀，对于不同的应用程序可以使用不同的前缀；默认“session:”，
    # 即保存在redis中的键的名称前都是以“session:”开头；
    SESSION_KEY_PREFIX='ihome'
    #设置session该连接哪个redis，其是一个连接对象
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=3)

    #解决flask_restful返回时中文字符变成unicode编码问题
    RESTFUL_JSON = dict(ensure_ascii=False)

    #自定义配置文件
    COMMON_REDIS=redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=4,decode_responses=True)
    API_URL_VERSION='api/v1.0'
    API_URL_VERSION_ROOT='API_V1_0'

    #图片验证码保存时间
    VERIFY_CODE_EXPIRE=5*60
    #短信验证码保存时常
    SMS_CODE_EXPIRE = 5 * 60
    #登录失败锁定时常
    LOGIN_ERROR_TIME=600
    #登录失败次数
    LOGIN_ACCESS_NUM=5
    #七牛域名
    QINIU_URL_DOMAIN = 'http://pp9g22fmy.bkt.clouddn.com/'

    @classmethod
    def init_app(cls,app):
        try:
            from ihome import local_setting
            for setting in dir(local_setting):
                if setting.isupper():
                    setattr(cls, setting, getattr(local_setting, setting))
        except ImportError:
            pass
        app.config.from_object(cls)
        app.redis=app.config['COMMON_REDIS']


class DevSetting(BaseSetting):
    DEBUG=True

    REDIS_HOST = '192.168.187.136'
    REDIS_PORT = 6379


class ProductionSetting(BaseSetting):
    REDIS_HOST = None
    REDIS_PORT = None
    DEBUG=False


class TestSetting(BaseSetting):
    SQLALCHEMY_DATABASE_URI ='mysql://root:oracle@192.168.187.136:3306/flask_test?charset=utf8'
    TESTING=True



SETTING_MAPPING={
    'dev':DevSetting,
    'pro':ProductionSetting
}
