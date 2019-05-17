# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/11 17:13
import re

from flask import current_app,session,g
from flask_restful import request
from sqlalchemy.exc import IntegrityError


from models.user import *
from utils.resource import View
from utils.response_code import RET
from .image_code import SmsView
from utils.authentication import authentication
from utils.qiniu_storage import storage

class UserView(View):

    method_decorators = {'get':[authentication,],
                         'put':[authentication,]}

    def get(self):
        """查看个人资料"""
        try:
            user=User.query.get(g.user_id)
        except:
            return {'errno':RET.DBERR,'msg':'服务器异常'}
        user_dict=user.to_dict()
        user_dict['avatar_url']=user_dict['portrait']
        return {'errno':RET.OK,'msg':True,'data':user_dict}

    def post(self):
        """注册"""
        js=request.get_json()
        mobile=js.get('mobile')
        sms_code=js.get('sms_code')
        password1=js.get('password')
        password2=js.get('password2')
        if not all((mobile,sms_code,password1,password2)):
            return {'errno':RET.PARAMERR,'msg':'缺少参数'},400

        if not re.match(r'1[3578]\d{9}',mobile):
            return {'errno':RET.PARAMERR,'msg':'手机号输入错误'},400

        if password1 != password2:
            return {'error':RET.PARAMERR,'msg':'两次密码输入不一致'},400

        try:
            real_code=current_app.redis.get(SmsView.get_sms_key(mobile))
            current_app.redis.delete(SmsView.get_sms_key(mobile))
        except:
            return {'errno':RET.DBERR,'msg':'服务器异常'}

        if sms_code !=real_code:
            return {'errno':RET.PARAMERR,'msg':'验证码错误'}

        user=User(mobile=mobile,name=mobile)
        user.password_hash=password1
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'errno':RET.PARAMERR,'msg':'手机号已被注册'}
        except Exception:
            return {'errno':RET.DBERR,'msg':'服务器异常'}

        return {'errno':RET.OK,'msg':'成功'}

    def put(self):
        user_name=request.get_json().get('name')
        if not user_name:
            return {'errno':RET.PARAMERR,'msg':'用户名不能为空'}

        try:
            User.query.filter_by(id=g.user_id).update({'name':user_name})
            db.session.commit()
        except :
            db.session.rollback()
            return {'errno':RET.DBERR,'msg':'服务器异常'}

        return {'errno':RET.OK,'msg':True,'data':{'name': user_name}}

class SessionView(View):
    """登录视图"""
    method_decorators = {
        'get':[authentication]
    }

    def get(self):
        user=User.query.get(g.user_id)
        if user:
            return {'errno':RET.OK,'msg':'成功','data':{'name':user.name}}
        return {'errno':RET.SESSIONERR,'msg':'false'}

    def post(self):
        js=request.get_json()
        mobile=js.get('mobile')
        pwd=js.get('password')
        print(mobile)
        if not all([mobile,pwd]):
            return {'errno':RET.PARAMERR,'msg':'账号和密码未输入'}
        if not re.match(r'1[34578]\d{9}',mobile):
            return {'errno':RET.PARAMERR,'msg':'请输入正确手机号码'}

        try:
            res=current_app.redis.get(self.login_error_key)
        except:
            pass
        else:
            if res and int(res) >=current_app.config['LOGIN_ACCESS_NUM']:
                return {'errno':RET.LOGINERR,'msg':'密码输入次数过多,请十分钟之后重试'}

        try:
            user=User.query.filter_by(mobile=mobile).first()
        except:
            return {'errno':RET.DBERR,'msg':'服务器错误'}

        if not user or not user.check_password(pwd):
            current_app.redis.incr(self.login_error_key)
            current_app.redis.expire(self.login_error_key,current_app.config['LOGIN_ERROR_TIME'])
            return {'errno':RET.PARAMERR,'msg':'用户或密码错误'}

        session['name']=user.name
        session['id']=user.id
        session['mobile']=user.mobile
        return {'errno':RET.OK,'msg':'登录成功'}

    def delete(self):
        csrf_token=session.get('csrf_token')
        session.clear()
        session['csrf_token']=csrf_token
        return {'errno':RET.OK,'msg':True}

    @property
    def login_error_key(self):
        return f'access_{request.remote_addr}'

class AvatarView(View):

    def post(self):
        avatar=request.files.get('avatar')

        if not avatar:
            return {'errno':RET.PARAMERR,'msg':'请上传图片'}
        try:
            file_name=storage(avatar.read())
        except:
            return {'errno':RET.THIRDERR,'msg':'第三方服务异常'}

        try:
            user=User.query.get(g.user_id)
            user.portrait=f'{current_app.config["QINIU_URL_DOMAIN"]}{file_name}'
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            return {'errno':RET.DBERR,'msg':'服务器异常'}

        return {'errno':RET.OK, 'msg':'保存成功', 'data':{'avatar_url': user.portrait}}


class AuthView(View):
    """实名认证"""

    def get(self):
        try:
            user=User.query.get(g.user_id)
        except:
            return {'errno':RET.DBERR,'msg':'服务器异常'}
        return {'errno':RET.OK, 'errmsg':"OK", 'data':user.to_dict()}

    def post(self):
        req_dict = request.get_json()
        real_name = req_dict.get('real_name')
        id_card = req_dict.get('id_card')

        if not all([real_name,id_card]):
            return {'errno':RET.PARAMERR,'msg':'参数传递错误'}

        if not re.match(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',
                    id_card):
            return {'errno':RET.PARAMERR, 'msg':'身份证号码格式错误'}

        try:
            User.query.filter_by(id=g.user_id).update({'real_name':real_name,'id_card':id_card})
            db.session.commit()
        except Exception as ex:
            raise ex
            db.session.rollback()
            return {'errno':RET.DBERR,'msg':'服务器异常'}
        return {'errno':RET.OK, 'msg':'ok','data':{'real_name':real_name,'id_card':id_card}}
