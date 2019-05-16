# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/7 18:37
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager

from ihome.wsgi import create_application,db


app=create_application('dev')
#创建manager脚本命令
manage=Manager(app)
#增加migrate命令,指定Migrations目录存放位置
migrate=Migrate(app,db,'./models/migrations')
manage.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manage.run()


