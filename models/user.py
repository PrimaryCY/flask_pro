# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/8 17:06
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import Column,Integer,String,SmallInteger
from sqlalchemy_utils import ChoiceType
from sqlalchemy_mptt import BaseNestedSets

from ihome.wsgi import db
#from manage import db
from .basemodel import BaseModel

class User(db.Model,BaseModel):
    """用户表"""
    __tablename__='user'

    USER_SEX=(
        (0,'women'),
        (1,'man'),
        (2,'secrecy')
    )

    id=Column(Integer,primary_key=True,comment='ID')
    name=Column(String(32),unique=True,comment='用户昵称')
    password=Column(String(128),comment='密码')
    mobile=Column(String(11),unique=True,comment='手机号码')
    real_name=Column(String(10),comment='真实姓名')
    #python manage.py db migrate 对string长度修改不敏感需要自己手动修改数据库表
    id_card=Column(String(18),unique=True,comment='身份证号')
    portrait=Column(String(256),comment='头像')
    age=Column(SmallInteger,comment='年龄')
    sex=Column(ChoiceType(USER_SEX,Integer()),comment='性别')

    houses=db.relationship('House',backref="user",lazy='dynamic')
    #order=db.relationship('订单表名',backref="user",lazy='dynamic')

    def __repr__(self):
        return self.name

    @property
    def password_hash(self):
        raise AttributeError('only setter attribute')

    @password_hash.setter
    def password_hash(self,value):
        self.password=generate_password_hash(value)

    def check_password(self,pwd):
        return check_password_hash(self.password,pwd)

    def to_flask_dict(self):
        """将对象转换为字典数据"""
        user_dict = {
            "user_id": self.id,
            "name": self.name,
            "mobile": self.mobile,
            "avatar": self.portrait if self.portrait else "",
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return user_dict

class Address(BaseModel,BaseNestedSets,db.Model):
    """用户地址"""
    __tablename__='user_address'

    id=Column(Integer,primary_key=True,comment='ID')
    name=Column(String(64),comment='地名')
    house=db.relationship('House',lazy='dynamic',backref='area')

    def __repr__(self):
        return self.name

