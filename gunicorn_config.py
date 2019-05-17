# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/17 17:18
import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count()
worker_class = 'gevent'

BASE_PATH = '/home/xtdev/zj_resource'
pythonpath = '/home/xtdev/zj_resource'

max_requests = 5000

timeout = 300

user = 'root'
group = 'root'

pidfile = '/tmp/flask_gunicorn.pid'
errorlog = '/home/log/flask_gunicorn.log'
