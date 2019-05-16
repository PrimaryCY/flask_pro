# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/14 16:10
import datetime

from ihome.wsgi import db
#from manage import db
from .basemodel import BaseModel

class Order(BaseModel, db.Model):
    """订单"""

    __tablename__ = "order_info"

    id = db.Column(db.Integer, primary_key=True)  # 订单编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # 下订单的用户编号
    house_id = db.Column(db.Integer, db.ForeignKey("house_info.id"), nullable=False)  # 预订的房间编号
    begin_date = db.Column(db.DateTime, nullable=False)  # 预订的起始时间
    end_date = db.Column(db.DateTime, nullable=False)  # 预订的结束时间
    days = db.Column(db.Integer, nullable=False)  # 预订的总天数
    house_price = db.Column(db.Integer, nullable=False)  # 房屋的单价
    amount = db.Column(db.Integer, nullable=False)  # 订单的总金额
    trade_no=db.Column(db.String(256))#支付宝订单id
    status = db.Column(  # 订单的状态
        db.Enum(
            "WAIT_ACCEPT",  # 待接单,
            "WAIT_PAYMENT",  # 待支付
            "PAID",  # 已支付
            "WAIT_COMMENT",  # 待评价
            "COMPLETE",  # 已完成
            "CANCELED",  # 已取消
            "REJECTED"  # 已拒单
        ),
        default="WAIT_ACCEPT", index=True)
    comment = db.Column(db.Text)  # 订单的评论信息或者拒单原因


    def to_dict(self):
        d = {
            'order_id': self.id,
            'user_id': self.user_id,
            'house_id': self.house_id,
            'begin_date': datetime.datetime.strftime(self.begin_date, '%Y-%m-%d'),
            'end_date': datetime.datetime.strftime(self.end_date, '%Y-%m-%d'),
            'days': self.days,
            'house_price': '%.2f' % float(self.house_price / 100),
            'amount': '%.2f' % float(self.amount / 100),
            'status': self.status,
            'ctime': datetime.datetime.strftime(self.create_time, '%Y-%m-%d'),
            'title': self.house.title,
            'img_url': self.house.index_image_url,
            'comment':self.comment
        }
        # status = {
        #     "WAIT_ACCEPT": 0,
        #     "WAIT_PAYMENT": 1,
        #     "PAID": 2,
        #     "WAIT_COMMENT": 3,
        #     "COMPLETE": 4,
        #     "CANCELED": 5,
        #     "REJECTED": 6
        # }
        # d['status'] = status[self.status]

        return d
