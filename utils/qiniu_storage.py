# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/11 23:27
from qiniu import Auth, put_data, etag
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = '6sc9HBmQoZroHWcxQy-wOhmEW1Un7lSMz5n7fs0z'
secret_key = 'C1vIQ8aaEvrELpkqGkt4wLrWTs_x7bwp4Nlm4K5M'


def storage(file_data):
    """
    图片上传到七牛
    :param file_data: 图片二进制数据
    :return:
    """
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'panda-ihome'
    # 上传后保存的文件名
    # 不去指定则按七牛计算后的结果命名，以此解决重复文件问题
    # key = 'my-python-logo.png'
    # 生成上传 Token，可以指定过期时间等
    # token = q.upload_token(bucket_name, key, 3600)
    token = q.upload_token(bucket_name,None, 3600)
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    ret, info = put_data(token, None, file_data)
    print(ret)
    print(info)
    if info.status_code == 200:
        return ret.get('key')
    else:
        raise Exception('上传七牛失败')


    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)

if __name__ == '__main__':
    with open(r'D:\111.png','rb') as f:
        file_data = f.read()
        print(storage(file_data))