# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/12 19:08
from sqlalchemy import Column,ForeignKey,Integer

from ihome.wsgi import db
#from manage import db
from .basemodel import BaseModel

#房屋设施中间表
house_facility = db.Table(
    'houses_facility',
    Column('house_id',Integer,ForeignKey('house_info.id'),primary_key=True),
    Column('facility_id',Integer,ForeignKey('facility_info.id'),primary_key=True)
)


class House(BaseModel, db.Model):
    """房屋信息"""

    __tablename__ = "house_info"

    id = db.Column(db.Integer, primary_key=True)  # 房屋编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # 房屋主人的用户编号
    area_id = db.Column(db.Integer, db.ForeignKey("user_address.id"), nullable=False)  # 归属地的区域编号
    title = db.Column(db.String(64), nullable=False)  # 标题
    price = db.Column(db.Integer, default=0)  # 单价，单位：分
    address = db.Column(db.String(512), default="")  # 地址
    room_count = db.Column(db.Integer, default=1)  # 房间数目
    acreage = db.Column(db.Integer, default=0)  # 房屋面积
    unit = db.Column(db.String(32), default="")  # 房屋单元， 如几室几厅
    capacity = db.Column(db.Integer, default=1)  # 房屋容纳的人数
    beds = db.Column(db.String(64), default="")  # 房屋床铺的配置
    deposit = db.Column(db.Integer, default=0)  # 房屋押金
    min_days = db.Column(db.Integer, default=1)  # 最少入住天数
    max_days = db.Column(db.Integer, default=0)  # 最多入住天数，0表示不限制
    order_count = db.Column(db.Integer, default=0)  # 预订完成的该房屋的订单数
    index_image_url = db.Column(db.String(256), default="")  # 房屋主图片的路径
    images=db.relationship('HouseImage',backref='house',
                           lazy='dynamic',cascade='all')
    facility=db.relationship('Facility',secondary=house_facility,
                             backref='house',lazy='dynamic',cascade='all')
    orders=db.relationship('Order',backref='house')

    def __str__(self):
        return self.title

    def to_full_dict(self):
        """将详细信息转换为字典数据"""
        house_dict = {
            "hid": self.id,
            "user_id": self.user_id,
            "user_name": self.user.name,
            "user_avatar": self.user.portrait if self.user.portrait else "",
            "title": self.title,
            "price": '%.2f' % float(self.price / 100),
            "address": self.address,
            "room_count": self.room_count,
            "acreage": self.acreage,
            "unit": self.unit,
            "capacity": self.capacity,
            "beds": self.beds,
            "deposit": '%.2f' % float(self.deposit / 100),
            "min_days": self.min_days,
            "max_days": self.max_days,
        }

        # 房屋图片
        img_urls = []
        for image in self.images:
            img_urls.append(image.url)
        house_dict["img_urls"] = img_urls

        # 房屋设施
        facilities = []
        for facility in self.facility:
            facilities.append(facility.id)
        house_dict["facilities"] = facilities

        # # 评论信息
        # comments = []
        # orders = Order.query.filter(Order.house_id == self.id, Order.status == "COMPLETE", Order.comment != None) \
        #     .order_by(Order.update_time.desc()).limit(constants.HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS)
        # for order in orders:
        #     comment = {
        #         "comment": order.comment,  # 评论的内容
        #         "user_name": order.user.name if order.user.name != order.user.mobile else "匿名用户",  # 发表评论的用户
        #         "ctime": order.update_time.strftime("%Y-%m-%d %H:%M:%S")  # 评价的时间
        #     }
        #     comments.append(comment)
        # house_dict["comments"] = comments
        return house_dict

    def to_basic_dict(self):
        d = {
            'house_id': self.id,
            'title': self.title,
            'area_id': self.area.name,
            'price': '%.2f' % float(self.price / 100),
            'create_time': self.create_time.strftime('%Y-%m-%d'),
            'index_url':  self.index_image_url,
            "room_count": self.room_count,
            "order_count": self.order_count,
            "address": self.address,
            "user_avatar": self.user.portrait if self.user.portrait else "",
        }
        return d


class Facility(BaseModel,db.Model):
    """住房设施"""
    __tablename__='facility_info'

    id=Column(Integer,primary_key=True)
    name=Column(db.String(64),comment='设施名称',nullable=False)

    def __str__(self):
        return self.name


class HouseImage(BaseModel,db.Model):
    """住房图片"""
    __tablename__='house_image'

    id=Column(Integer,primary_key=True)
    house_id=Column(Integer,ForeignKey('house_info.id'),nullable=False,comment='房屋')
    url=Column(db.String(512),comment='图片链接',nullable=False)

    def __str__(self):
        return self.url
