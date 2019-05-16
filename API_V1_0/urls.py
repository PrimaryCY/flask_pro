# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/9 21:39
from flask import Blueprint
from flask_restful import Api

from .routes.image_code import ImageCodeView,SmsView,TestView
from .routes.passport import UserView,SessionView,AvatarView,AuthView
from .routes.houses import AreaView,HouseView,HouseImageView,HouseIndexView,HouseListView
from .routes.order import OrderView,CommentView,AlipayView,OrderStatusView

blue=Blueprint('api1.0',__name__)

api=Api(app=blue)


# endpoint是用来给url_for反转url的时候指定的。如果不写endpoint，那么将会使用视图的名字的小写来作为endpoint。
# 例如;
# 我们在下面没有指定endpoint参数，那么url_for进行反转时，就需要使用蓝图名+视图类的小写来获取对应的url地址
# urlfor('api1.0.userview')
api.add_resource(ImageCodeView,'/image_codes','/image_codes/<re("(.*)"):image>',endpoint="image")
api.add_resource(SmsView,'/sms_codes/<re(r"1[3579]\d{9}"):mobile>')
api.add_resource(TestView,'/test')
api.add_resource(UserView,'/user')
api.add_resource(SessionView,'/session')
api.add_resource(AvatarView,'/user/avatar')
api.add_resource(AuthView,'/user/auth')
api.add_resource(AreaView,'/areas')
api.add_resource(HouseView,'/houses/info','/user/houses','/houses/<re(r".*"):house_id>')
api.add_resource(HouseImageView,'/houses/image')
api.add_resource(HouseIndexView,'/houses/index')
api.add_resource(HouseListView,'/houses')
api.add_resource(OrderView,'/orders')
api.add_resource(CommentView,'/orders/<int:order_id>/comment')
api.add_resource(AlipayView,'/orders/<int:order_id>/payment')
api.add_resource(OrderStatusView,'/orders/<int:order_id>/status')

