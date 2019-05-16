# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/8 17:06
import datetime
from datetime import date

from sqlalchemy import Column,DateTime,Boolean


class BaseModel(object):

    create_time=Column(DateTime,default=datetime.datetime.now(),comment='创建时间')
    update_time=Column(DateTime,default=datetime.datetime.now(),onupdate=datetime.datetime.now(),
                       comment="修改时间")
    is_active=Column(Boolean,default=True,comment='状态')

    def to_dict(self):
        temp={}
        for c in self.__table__.columns:
            attr=getattr(self, c.name)
            if isinstance(attr,datetime.datetime) or isinstance(attr,date):
                attr=attr.strftime('%Y-%m-%d')
            temp[c.name]=attr
        return temp
