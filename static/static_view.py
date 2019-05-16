# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/9 9:32
from flask import Blueprint,current_app,make_response
from flask_wtf import csrf

staic=Blueprint('static',__name__)


@staic.route('/<re(r".*"):file_name>',methods=['GET'])
def index(file_name):
    if not file_name:
        file_name='index.html'
    #只能手动拼接路径,因为下方的send_static_file方法会判断'//'是否在该路径中,如果在直接抛异常
    #所有os.path.join()无法使用
    if file_name != 'favicon.ico':
        file_path=f'html/{file_name}'
    else:
        file_path=file_name

    #生成csrf_token值
    csrf_token=csrf.generate_csrf()

    response=make_response(current_app.send_static_file(file_path))
    #response.set_cookie('csrf_token',csrf_token)
    return response
