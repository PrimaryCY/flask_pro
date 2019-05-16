# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/7 19:20

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_cors import CORS

from ihome import settings
from utils.django_util import import_string
from utils.converters import ReConverters
from static.static_view import staic

#数据库实例
db=SQLAlchemy()

#补充csrftoken验证,防止跨站攻击
csrf=CSRFProtect()

#修改session
session=Session()

#允许跨域访问
cors=CORS()



def create_application(env='dev'):
    app = Flask(settings.BASE_DIR)

    app_setting=settings.SETTING_MAPPING.get(env)
    assert app_setting,(
        f'{env}该配置文件不存在!'
    )

    # 导入app配置
    #app.config.from_object(app_setting)
    app_setting.init_app(app)

    db.init_app(app)

    session.init_app(app)
    #r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
    cors.init_app(app,resources='*',supports_credentials=True)
    #csrf.init_app(app)

    # 注册通用转换器
    app.url_map.converters['re'] = ReConverters

    #加载蓝图,
    # 'API_URL_VERSION_ROOT'目录文件
    # "API_URL_VERSION" 路由前缀
    bule_print=import_string('.'.join([app.config['API_URL_VERSION_ROOT'],'urls','blue']))
    app.register_blueprint(bule_print,url_prefix=f'/{app.config["API_URL_VERSION"]}')


    #注册静态文件视图
    app.register_blueprint(staic,url_prefix='')
    print(app.url_map)

    app.app_context().push()
    return app


if __name__ == '__main__':
    app=create_application()
    app.run()



