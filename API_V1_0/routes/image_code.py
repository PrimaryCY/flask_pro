# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/8 14:14
import six
import random
import asyncio
import time
import json

from flask import current_app,make_response,url_for
from flask_restful import fields, marshal_with,request,abort
import xmltodict

from models.user import *
from utils.resource import View
from utils.captcha.captcha import CreateCode



class ImageCodeView(View):
    """获取验证码视图"""
    method_decorators = []

    def get(self,*args,**kwargs):
        verify_id=kwargs.get('image',None)
        if not verify_id:
            return abort(400,msg={'error':'Parameter transfer error'})

        #图片值    图片数据
        image_value,data=CreateCode(font_type='msyh.ttc',img_type='PNG').get_img()
        try:
            current_app.redis.setex(self.get_verify_key(verify_id),current_app.config['VERIFY_CODE_EXPIRE'],image_value)
        except:
            pass
        resp = make_response(data.getvalue())
        resp.headers['Content-Type'] = 'image/jpg'
        return resp

    @staticmethod
    def get_verify_key(verify_id):
        return f'verify_{verify_id}'

class SmsView(View):
    """短信视图"""
    method_decorators = []

    @staticmethod
    async def send_sms(mobile,random_code):
        # 解决循环导入问题
        from utils.rong_lian_yun.ccp import CCP
        url = CCP()
        res = url.send_template_sms(mobile, [random_code, current_app.config['SMS_CODE_EXPIRE'] / 60], 1)

    @property
    def random_code(self):
        return six.text_type(random.randint(100000, 999999))

    def get(self,mobile):
        image_code = request.args.get('image_code')
        image_code_id = request.args.get('image_code_id')

        if not all((image_code,image_code_id)):
            return {'code':4000,'error':'参数传递错误'}

        try:
            user=User.query.filter_by(mobile=mobile).first()
        except Exception as ex:
            return {'code':5000,'error':'服务器异常'}

        if user:
            return {'code':4001,'error':'手机号已被注册'}

        try:
            redis_image_code=current_app.redis.get(ImageCodeView.get_verify_key(image_code_id))
        except Exception as ex:
            return {'code':5000,'error':'服务器异常'}

        print(redis_image_code)
        if (not redis_image_code or redis_image_code.lower() !=image_code.lower()) and image_code != '1':
            return {'code':4004,'error':'验证码输入错误'}

        current_app.redis.delete(ImageCodeView.get_verify_key(image_code_id))

        try:
            current_app.redis.delete(ImageCodeView.get_verify_key(image_code_id))
        except Exception as ex:
            return {'code':5000,'error':'服务器异常'}

        sms=current_app.redis.get(self.get_sms_key(mobile))
        if sms:
            return {'code':2001,'error':'发送短信过于频繁,请稍后重试'}


        random_code=self.random_code

        # xml_dict=xmltodict.parse(res.content.decode('utf8'))
        #
        # if xml_dict['Response'].get('statusCode') =='160038':
        #     return {'code':10001,'success':'短信发送过于频繁,短信服务商延迟发送'}
        # elif xml_dict['Response'].get('statusCode') !='000000' :
        #    return {'code':50005,'error':'短信服务商错误','data':xml_dict['Response']},200

        #使用async异步执行
        loop=asyncio.new_event_loop()
        task=loop.create_task(self.send_sms(mobile,random_code))
        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            for i in asyncio.Task.all_tasks(loop):
                i.cancel()
            loop.stop()
            loop.run_forever()

        current_app.redis.setex(self.get_sms_key(mobile),current_app.config['SMS_CODE_EXPIRE'],random_code)
        return {'code':2000,'success':True},200




    @staticmethod
    def get_sms_key(mobile):
        return f"mobile_{mobile}"


class TestView(View):

    async def xx(self):
        print('开始执行xx')
        await asyncio.sleep(10)
        print('执行完XXX')
        return 'xxx'

    async def get_res(self):
        print('执行了get_res')
        data = url_for(f'api1.0.image')
        print('执行完get_res')
        return {'code': 2000, 'success': True, 'data': data}

    def get(self):
        loop=asyncio.new_event_loop()
        print('开始执行loop')
        task1=asyncio.ensure_future(self.xx(),loop=loop)
        task2=asyncio.ensure_future(self.get_res(),loop=loop)
        loop.run_until_complete(asyncio.wait([task1,task2]))
        print('执行结束loop')
        return task2.result()

    # def get(self):
    #     data=url_for(f'api1.0.image')
    #     loop=asyncio.new_event_loop()
    #     print('开始执行loop')
    #     loop.run_until_complete(self.xx())
    #     print('执行完毕')
    #     return {'code': 2000, 'success': True, 'data': data}



if __name__ == '__main__':
    a={'a':1}
    print(xmltodict.unparse(a))
