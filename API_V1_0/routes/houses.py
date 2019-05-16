# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/12 13:48
import random
import datetime
import json
import re

from flask import current_app,session,g
from flask_restful import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from models.user import *
from models.houses import *
from models.order import *
from utils.resource import View
from utils.response_code import RET
from utils.qiniu_storage import storage
from utils.django_util import model_to_dict


class AreaView(View):
    method_decorators = []

    def GBK2312(self):
        """
        生成随机中文字符
        :return: 返回10个随机中文字符集
        """
        all_str=[]
        for i in range(10):
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xfe)
            val = f'{head:x}{body:x}'
            one_str = bytes.fromhex(val).decode('gb18030')
            all_str.append(one_str)
        return ''.join(all_str)

    def get(self):
        lis=[]
        for i in range(10):
            max_id=db.session.query(func.max(Address.id)).scalar()
            min_id=db.session.query(func.min(Address.id)).scalar()
            par_addr=Address.query.get(random.randint(min_id,max_id))
            addr=Address(name=f'{i}{self.GBK2312()}',parent=par_addr)

            #addr = Address(name=f'{i}{self.GBK2312()}')
            lis.append(addr)

            # Address.query.delete()
        try:
            db.session.add_all(lis)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        def js(node):
            """增加自定义字段"""
            return {'name':node.name}

        data = Address.get_tree(session=db.session, json=True, json_fields=js)

        return {'errno':RET.OK, 'msg':'OK', 'data':data}


class HouseView(View):

    def get(self,**kwargs):
        if not kwargs.get('house_id'):
            return self.list()
        return self.retrieve(kwargs)

    def retrieve(self,kwargs):
        """房源详情页"""
        house_id=kwargs.get('house_id')
        user_id = session.get('id', '-1')
        if not house_id:
            return {'errno':RET.PARAMERR, 'msg':'缺少参数'}

        try:
            house=House.query.get(house_id)
            user=User.query.get(user_id)
        except Exception as ex:
            #raise ex
            return {'errno':RET.DBERR,'msg':'数据库异常'}
        if not house or not user:
            return {'errno':RET.PARAMERR,'msg':'房屋不存在'}

        return {'errno':RET.OK,'msg':True,'data':{'house':house.to_full_dict(),'user':user.to_flask_dict()}}


    def list(self):
        """查看个人房源"""
        try:
            user=User.query.get(g.user_id)
        except:
            return {'errno':RET.DBERR,'msg':'服务器异常'}

        res=[]
        for house in user.houses.all():
            dict=house.to_dict()
            dict['area']=house.area.name
            res.append(dict)
        return {'errno':RET.OK,'msg':True,'data':{'houses':res}}

    def post(self):
        """创建房源"""
        house_data = request.get_json()
        title = house_data.get('title')
        price = house_data.get('price')
        area_id = house_data.get('area_id')
        address = house_data.get('address')
        room_count = house_data.get('room_count')
        unit = house_data.get('unit')
        acreage = house_data.get('acreage')
        capacity = house_data.get('capacity')
        beds = house_data.get('beds')
        deposit = house_data.get('deposit')
        min_days = house_data.get('min_days')
        max_days = house_data.get('max_days')

        if not all([title, price, area_id, address, room_count, unit,
                    acreage, capacity, beds, deposit, min_days, max_days]):
            return {'errno':RET.PARAMERR, 'msg':'缺少参数'}

        # 判断价格、押金格式是否正确
        try:
            price = int(float(price) * 100)
            deposit = int(float(deposit) * 100)
        except Exception as e:
            current_app.loggere.error(e)
            return {'errno':RET.PARAMERR, 'msg':'请输入正确的价格，数字类型，最多2位小数'}

        # 保存房屋信息
        house = House(
            user_id=g.user_id,
            area_id=area_id,
            title=title,
            price=price,
            address=address,
            room_count=room_count,
            unit=unit,
            acreage=acreage,
            capacity=capacity,
            beds=beds,
            deposit=deposit,
            min_days=min_days,
            max_days=max_days,
        )

        facility=house_data.get('facility',[])
        if facility:
            try:
                facility=Facility.query.filter(Facility.id.in_(facility)).all()
            except:
                db.session.rollback()
                return {'errno':RET.DBERR,'msg':'数据库操作异常'}

        house.facility=facility
        try:
            db.session.add(house)
            db.session.commit()
        except:
            db.session.rollback()
            return {'errno':RET.DBERR,'msg':'服务器异常'}

        return  {'errno':RET.OK, 'msg':'创建成功', 'data':{'house_id': house.id}}


class HouseImageView(View):

    def post(self):
        """上传房屋图片"""
        image=request.files.get('house_image')
        house_id=request.form.get('house_id')

        if not all([image,house_id]):
            return {'errno':RET.PARAMERR,'msg':'参数填写错误'}

        try:
            house=House.query.get(house_id)
        except:
            return {'errno':RET.DBERR,'msg':'服务器异常'}
        if not house:
            return {'errno':RET.PARAMERR,'msg':'房屋不存在'}

        image=image.read()
        try:
            res=storage(image)
        except:
            return {'errno':RET.UNKOWNERR,'msg':'第三方服务异常'}
        else:
            image_url=f'{current_app.config["QINIU_URL_DOMAIN"]}{res}'
            if not house.index_image_url:
                house.index_image_url=image_url
                db.session.add(house)

            house_image=HouseImage(url=image_url,house_id=house_id)

            try:
                db.session.add(house_image)
                db.session.commit()
            except:
                db.session.rollback()
                return {'errno': RET.DBERR, 'msg': '服务器异常'}
            return {'errno':RET.OK,'msg':'保存成功', 'data':{'img_url': image_url}}


class HouseIndexView(View):

    def get(self):
        """首页轮播图页"""
        try:
            houses=House.query.filter(House.index_image_url!='').order_by(House.order_count.desc()).limit(5)
        except:
            return {'errno':RET.DBERR,'msg':'服务器异常'}

        if not houses:
            return {'errno':RET.NODATA,'msg':'无数据'}
        data=[i.to_basic_dict() for i in houses]

        return {'errno':RET.OK,'msg':True,'data':data}


class HouseListView(View):

    def get(self):
        start_date = request.args.get('sd', '')
        end_date = request.args.get('ed', '')
        area_id = request.args.get('aid', '')
        sort_key = request.args.get('sk', 'new')
        page = request.args.get('p')

        filter_params=[]
        try:
            if start_date:
                start_date=datetime.datetime.strptime(start_date,'%Y-%m-%d')
                filter_params.append(Order.end_date >= start_date)
            if end_date:
                end_date=datetime.datetime.strptime(end_date,'%Y-%m-%d')
                filter_params.append(Order.begin_date <=end_date)
            if start_date and end_date:
                assert start_date<end_date
        except :
            return {'errno':RET.PARAMERR,'msg':'日期参数传入错误'}


        try:
            page=int(page)
        except:
            page=1

        fina_filter = []
        if area_id:
            try:
                area=Address.query.get(area_id)
            except :
                return {'errno':RET.DBERR,'msg':'数据库异常'}
            if not area:
                return {'errno':RET.PARAMERR,'msg':'地区不存在'}
            fina_filter.append(House.area_id==area_id)

        try:
            not_in_house_ids=db.session.query(Order.house_id).filter(*filter_params).scalar()
            print(not_in_house_ids)
        except  Exception as e:
            raise e
            return {'errno':RET.PARAMERR,'msg':'数据库查询错误'}

        if not isinstance(not_in_house_ids,(list,tuple)):
            not_in_house_ids=[not_in_house_ids]

        if not_in_house_ids:
            fina_filter.append(House.id.notin_(not_in_house_ids))


        # 排序
        if sort_key == 'booking':  # 入住最多
            house_query = House.query.filter(*fina_filter).order_by(House.order_count.desc())
        elif sort_key == 'price-inc':  # 价格从低到高
            house_query = House.query.filter(*fina_filter).order_by(House.price)
        elif sort_key == 'price-des':  # 价格从高到低
            house_query = House.query.filter(*fina_filter).order_by(House.price.desc())
        else:  # new  默认 从新到旧
            house_query = House.query.filter(*fina_filter).order_by(House.create_time.desc())

        try:
            #                               当前页数  每页数量    自动错误输出
            paginate=house_query.paginate(page=page, per_page=2, error_out=False)
        except Exception as e:
            raise e
            return {'errno':RET.DBERR,'msg':'数据库错误'}

        house_data=[i.to_basic_dict() for i in paginate.items]
        all_page_num=paginate.pages

        return {'errno':RET.OK, 'msg':'OK',
                'data':{'total_page': all_page_num, 'houses': house_data, 'current_page': page}
                }






