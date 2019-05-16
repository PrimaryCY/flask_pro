# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/12 13:07
from flask import Flask, current_app, flash, render_template
from flask.signals import _signals

app = Flask(__name__)

# 自定义信号
xxxxx = _signals.signal('xxxxx')


def func(sender, *args, **kwargs):
    print(sender)
    return sender

# 自定义信号中注册函数
xxxxx.connect(func)


@app.route("/")
def index():
    # 触发信号
    res=xxxxx.send('123')
    print(res)
    return '212'


if __name__ == '__main__':
    app.run()
