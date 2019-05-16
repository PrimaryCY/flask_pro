# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/10 22:31
# coding:utf-8
import datetime
import base64
import hashlib
import requests

from manage import app

class CCP(object):
    # #主账号Token
    # accountToken="bc7e520ddb054393968b9258fc4c3f8d"
    # # 主帐号
    # accountSid = '8aaf07086a961c7a016aa164bf030a9d'
    # #应用ID
    # appId ="8aaf07086a961c7a016aa164bf510aa3"
    #
    # BASE_URL='https://app.cloopen.com:8883'

    accountToken=app.config['ACCOUNT_TOKEN']
    # 主帐号
    accountSid = app.config['ACCOUNT_SID']
    #应用ID
    appId =app.config['APP_ID']

    BASE_URL=app.config['BASE_URL']


    def generic_url(self):
        """
        生成加密后的url
        :return: 加密后的url,下面body中所需要的时间戳
        """
        time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        SigParameter=self.generic_sign(time)
        url=f"{self.BASE_URL}/2013-12-26/Accounts/{self.accountSid}/SMS/TemplateSMS?sig={SigParameter}"
        # 生成auth
        return url,time


    def send_template_sms(self,to,datas,template_id):
        """
        发送短信
        :param to:list          发送给谁
        :param datas:list       模板替换内容
        :param template_id:int  模板id
        :return:
        """
        url,time=self.generic_url()
        header=self.generic_header(time)
        body=self.generic_body(to,template_id,datas)
        res=requests.post(url=url,
                      json=body,
                      headers=header)
        return res

    def generic_body(self,to,template_id,datas):
        body={
            'to':to,
            'appId':self.appId,
            'templateId':template_id,
            'datas':datas
        }
        return body

    def generic_header(self,time):
        """
        生成请求头
        :param auth:加密的Token
        :return: 加工好的header
        """
        src = f'{self.accountSid}:{time}'
        auth = base64.b64encode(src.encode('utf8')).strip()
        header={'Authorization':auth,
                'Content-Type':'application/json;charset=utf-8',
                }
        return header


    def generic_sign(self,time):
        """
        加密url中的签名
        :param time: 时间戳
        :return: 加密后的url签名并且为全部大写
        """
        row_data=f'{self.accountSid}{self.accountToken}{time}'
        return hashlib.md5(row_data.encode()).hexdigest().upper()


# sendTemplateSMS(手机号码,内容数据,模板Id)
if __name__ == '__main__':

    url=CCP()
    res=url.send_template_sms("17635268013", ['1234', '5'],1)

    print(res.content.decode('utf8'))