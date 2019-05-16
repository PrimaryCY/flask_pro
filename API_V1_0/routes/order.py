# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/16 9:56
import datetime

from flask import g,request,current_app
from sqlalchemy.orm.exc import NoResultFound
from alipay import AliPay

from utils.resource import View
from utils.response_code import RET
from models.houses import *
from models.order import *


class OrderView(View):

    def get(self):
        """查看订单"""
        role = request.args.get('role', 'custom')
        try:
            if role == 'landlord':
                houses = House.query.filter_by(user_id=g.user_id).all()
                house_ids = [house.id for house in houses]
                orders = Order.query.filter(Order.house_id.in_(house_ids))
            else:
                orders = Order.query.filter_by(user_id=g.user_id).all()
        except:
            return {'errno':RET.DBERR,'msg':'数据库错误'}

        if orders:
            orders_data=[i.to_dict() for i in orders]
            return {'errno':RET.OK,'msg':True,'data':orders_data}
        return {'errno':RET.NODATA,'msg':'无返回数据'}




    def post(self):
        """创建订单"""
        user_id = g.user_id
        req_dict = request.get_json()
        house_id = req_dict.get('house_id')
        start_date = req_dict.get('start_date')
        end_date = req_dict.get('end_date')

        if not all([house_id,start_date,end_date]):
            return {'errno':RET.PARAMERR,'msg':'传入的参数错误'}

        try:
            house=House.query.filter(House.id==1).one()
        except NoResultFound:
            return {'errno':RET.PARAMERR,'msg':'参数传递错误'}
        except Exception:
            return {'errno':RET.DBERR,'msg':'数据库查询错误'}

        try:
            start_date=datetime.datetime.strptime(start_date,'%Y-%m-%d')
            end_date=datetime.datetime.strptime(end_date,'%Y-%m-%d')
            assert start_date<=end_date
        except Exception:
            return {'errno':RET.PARAMERR,'msg':'预订日期参数传递错误'}

        if user_id==house.user_id:
            return {'errno':RET.PARAMERR,'msg':'房东不能预定自己的房屋'}

        try:
            order_count=Order.query.filter(Order.house_id==house_id,
                                           Order.begin_date<=end_date,
                                           Order.end_date>=start_date).count()
        except:
            return {'errno':RET.PARAMERR,'msg':'参数传递错误'}

        if order_count>0:
            return {'errno':RET.PARAMERR,'msg':'房间已被预订'}

        days=(end_date-start_date+datetime.timedelta(1)).days
        amount=house.price * days

        try:
            order=Order(user_id=user_id, house_id=house_id, begin_date=start_date, end_date=end_date,
                      house_price=house.price, days=days, amount=amount)
            db.session.add(order)
        except:
            db.session.rollback()
            return {'errno':RET.DBERR,'msg':'网络错误,请重试'}

        return {'errno':RET.OK,'msg':'成功'}


class CommentView(View):
    """添加评论"""

    def put(self,order_id):
        js=request.get_json()
        comment=js.get('comment','')

        try:
            order=Order.query.filter(Order.id == order_id, Order.user_id ==g.user_id,
                                   Order.status == 'WAIT_COMMENT').one()
        except NoResultFound:
            return {'errno':RET.NODATA,'msg':'没有此订单'}
        except Exception:
            return {'errno':RET.DBERR,'msg':'数据库错误'}
        try:
            order.comment=comment
            house=order.house
            house.order_count+=1
            db.session.add(house)
            db.session.add(order)
            db.session.commit()
        except:
            db.session.rollback()
            return {'errno':RET.DBERR,'msg':'数据库错误'}
        return {'errno':RET.OK,'msg':True}



class AlipayView(View):

    def post(self,order_id):
        try:
            order=Order.query.filter(Order.id==order_id).one()
        except NoResultFound:
            return {'errno':RET.NODATA,'msg':'不存在此订单'}
        except Exception:
            return {'errno':RET.DBERR,'msg':'数据库错误'}

        alipay_client=AliPay(
            appid=current_app.config['ALIPAY_APP_ID'],
            app_notify_url=None,
            app_private_key_path=current_app.config['ALIPAY_APP_PRIVATE_KEY_PATH'],
            alipay_public_key_path=current_app.config['ALIPAY_ALIPAY_PUBLIC_KEY_PATH'],
            sign_type="RSA2",
            debug=True,
        )

        res=alipay_client.api_alipay_trade_wap_pay(
            out_trade_no=order.id,
            total_amount=str(order.amount/100),
            subject="flask_project",
            return_url=current_app.config['ALIPAY_RETURN_URL']
        )

        pay_url=current_app.config['ALIPAY_URL_PREFIX']+res
        return {'errno':RET.OK,'msg':True,'data':{'pay_url':pay_url}}



class OrderStatusView(View):

    def put(self,order_id):
        req_dict = request.get_json()

        user_id = g.user_id
        action = req_dict.get('action')
        reason = req_dict.get('reason', '')

        if not all([action, order_id]) or action not in ['accept', 'reject']:
            return {'errno':RET.NODATA, 'msg':'参数错误'}

        try:
            order = Order.query.filter(Order.id == order_id, Order.status == 'WAIT_ACCEPT').first()
            house = order.house
        except Exception as e:
            current_app.logger.error(e)
            return {'errno':RET.DBERR, 'msg':'数据库异常'}

        if user_id != house.user_id:
            return {'errno':RET.DBERR, 'msg':'操作无效'}

        if action == 'accept':
            order.status = 'WAIT_PAYMENT'
        else:
            order.status = 'REJECTED'
            order.comment = reason
        try:
            db.session.add(order)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return {'errno':RET.DBERR, 'msg':'数据库异常'}
        else:
            return {'errno':RET.OK, "msg":'OK'}

